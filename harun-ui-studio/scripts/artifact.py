"""Create and serve a factual review report; clean only unchanged owned files."""

import argparse
from datetime import datetime, timezone
from functools import partial
from hashlib import sha256
from html import escape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import shutil
from urllib.parse import urlsplit


OWNER = "harun-ui-studio/artifact-v1"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def location(base, name):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("Artifact ID must use lowercase letters, numbers, and hyphens")
    base = Path(base).absolute()
    if any(p.is_symlink() for p in (base, *base.parents)):
        raise ValueError("Artifact base must not contain symlinks")
    target = base / name
    if target.is_symlink():
        raise ValueError("Artifact directory must not be a symlink")
    return target


def text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Expected a nonempty text field")
    return escape(value, quote=True)


def validate(report):
    for key in ("title", "status", "data_mode", "summary", "backend"):
        text(report.get(key))
    if report["status"] not in ("READY FOR REVIEW", "BLOCKED", "PARTIAL"):
        raise ValueError("Invalid report status")
    for key in ("changes", "flows", "checks", "limitations", "screenshots"):
        if not isinstance(report.get(key), list):
            raise ValueError(f"Missing list: {key}")
    if "app_url" not in report:
        raise ValueError("Missing app_url; use null if unavailable")
    url = report["app_url"]
    if url is not None:
        if not isinstance(url, str) or any(c.isspace() for c in url):
            raise ValueError("Invalid application URL")
        parsed = urlsplit(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("Application URL must be HTTP(S) without credentials")
    for item in report["checks"]:
        if item.get("status") not in ("PASS", "FAIL", "BLOCKED", "NOT RUN"):
            raise ValueError("Invalid check status")


def render(report, captures, created):
    def rows(items, fields):
        return "".join("<tr>" + "".join(f"<td>{text(i[f])}</td>" for f in fields) + "</tr>" for i in items)

    flows = []
    for flow in report["flows"]:
        if not isinstance(flow.get("steps"), list) or not flow["steps"]:
            raise ValueError("Each flow needs at least one step")
        steps = "".join(f"<li>{text(step)}</li>" for step in flow["steps"])
        flows.append(f"<h3>{text(flow['name'])}</h3><p>Precondition: {text(flow['precondition'])}</p><ol>{steps}</ol><p>Expected: {text(flow['expected'])}</p>")
    link = (f'<a href="{text(report["app_url"])}" target="_blank" rel="noopener noreferrer">Open the actual application</a>'
            if report["app_url"] else "Application preview unavailable. See limitations.")
    shots = "".join(f'<figure><img src="{text(name)}" alt="{text(caption)}" style="max-width:100%;height:auto"><figcaption>{text(caption)}</figcaption></figure>' for name, caption in captures)
    limits = "".join(f"<li>{text(item)}</li>" for item in report["limitations"])
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark"><link rel="icon" href="data:,"><title>{text(report['title'])}</title></head>
<body><main style="max-width:80rem;margin:auto;padding:1rem;overflow-wrap:anywhere">
<h1>{text(report['title'])}</h1><p><strong>{text(report['status'])}</strong></p>
<p>{text(report['summary'])}</p><p>Data mode: {text(report['data_mode'])}</p>
<p>Report created: {text(created)}</p><p>{link}</p>
<p>This is a review report, not a separately rendered copy of the application. Captures are static evidence.</p>
<h2>Access flows</h2>{''.join(flows)}
<h2>Changes</h2><table><thead><tr><th scope="col">File</th><th scope="col">Change and reason</th></tr></thead><tbody>{rows(report['changes'], ('path', 'change'))}</tbody></table>
<h2>Verification</h2><table><thead><tr><th scope="col">Check</th><th scope="col">Status</th><th scope="col">Evidence</th></tr></thead><tbody>{rows(report['checks'], ('name', 'status', 'evidence'))}</tbody></table>
<h2>Backend handoff</h2><p>{text(report['backend'])}</p>
<h2>Limitations</h2><ul>{limits}</ul>
<h2>Current captures</h2>{shots or '<p>No screenshots supplied.</p>'}
<h2>Retention</h2><p>Retained until explicit cleanup. Review approval does not authorize deletion, commit, or push.</p>
</main></body></html>'''


def create(base, name, report):
    target = location(base, name)
    if target.exists():
        raise FileExistsError(f"Artifact already exists: {target}")
    validate(report)
    created = datetime.now(timezone.utc).isoformat()
    captures = []
    sources = []
    for i, shot in enumerate(report["screenshots"]):
        source = Path(shot["path"])
        if not source.is_absolute() or source.is_symlink() or not source.is_file():
            raise ValueError("Screenshot must be an existing absolute regular file")
        if source.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
            raise ValueError("Only PNG, JPEG, and WebP captures are accepted")
        filename = f"capture-{i + 1}{source.suffix.lower()}"
        captures.append((filename, shot["caption"]))
        sources.append(source)
    html = render(report, captures, created)
    target.mkdir(parents=True, exist_ok=False)
    (target / "index.html").write_text(html, encoding="utf-8")
    stored = {**report, "screenshots": [{"path": n, "caption": c} for n, c in captures]}
    (target / "report.json").write_text(json.dumps(stored, indent=2, ensure_ascii=False), encoding="utf-8")
    for source, (filename, _) in zip(sources, captures):
        shutil.copyfile(source, target / filename)
    manifest = {"owner": OWNER, "id": name, "created": created,
                "files": {p.name: digest(p) for p in target.iterdir()}}
    (target / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return target


def owned(base, name):
    target = location(base, name)
    manifest_path = target / "manifest.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise ValueError("Missing regular ownership manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("owner") != OWNER or manifest.get("id") != name:
        raise ValueError("Artifact ownership mismatch")
    files = manifest.get("files")
    if not isinstance(files, dict) or not {"index.html", "report.json"}.issubset(files):
        raise ValueError("Invalid owned file list")
    for filename in files:
        if not re.fullmatch(r"(?:index\.html|report\.json|capture-[0-9]+\.(?:png|jpe?g|webp))", filename):
            raise ValueError("Unexpected manifest path")
    if {p.name for p in target.iterdir()} != set(files) | {"manifest.json"}:
        raise ValueError("Untracked artifact files; inspect before cleanup")
    for filename, expected in files.items():
        path = target / filename
        if path.is_symlink() or not path.is_file() or digest(path) != expected:
            raise ValueError(f"Modified or unsafe artifact file: {filename}")
    return target, files


def clean(base, name, confirmation):
    if confirmation != name:
        raise ValueError("Cleanup requires the exact artifact ID as confirmation")
    target, files = owned(base, name)
    for filename in files:
        (target / filename).unlink()
    (target / "manifest.json").unlink()
    target.rmdir()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("create", "serve", "clean"))
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--id", required=True)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--confirm")
    args = parser.parse_args()
    try:
        if args.action == "create":
            if not args.report:
                raise ValueError("create requires --report")
            report = json.loads(args.report.read_text(encoding="utf-8"))
            print(create(args.base, args.id, report) / "index.html")
        elif args.action == "clean":
            clean(args.base, args.id, args.confirm)
            print(f"Removed owned artifact: {args.id}")
        else:
            target, _ = owned(args.base, args.id)
            handler = partial(SimpleHTTPRequestHandler, directory=str(target))
            with ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
                print(f"http://127.0.0.1:{server.server_port}/", flush=True)
                server.serve_forever()
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Artifact error: {error}\n")


if __name__ == "__main__":
    main()
