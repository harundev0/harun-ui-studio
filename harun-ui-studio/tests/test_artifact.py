"""Run: python3 -m unittest discover -s harun-ui-studio/tests -v."""

import importlib.util
import base64
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "artifact.py"
spec = importlib.util.spec_from_file_location("artifact", SCRIPT)
artifact = importlib.util.module_from_spec(spec)
spec.loader.exec_module(artifact)


class ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.report = {
            "title": "Orders <script>alert(1)</script>",
            "status": "READY FOR REVIEW",
            "app_url": "http://localhost:3000/orders?mode=demo&state=empty",
            "data_mode": "Frontend fixtures; no backend requests",
            "summary": "Reused the existing table.",
            "changes": [{"path": "src/orders.tsx", "change": "Reused Button"}],
            "flows": [{"name": "Review orders", "precondition": "Demo mode", "steps": ["Open Orders", "Select a row"], "expected": "Details open"}],
            "checks": [{"name": "Build", "status": "PASS", "evidence": "npm run build, exit 0"}],
            "backend": "Endpoint pending; see handoff.md.",
            "limitations": ["Real integration is not verified."],
            "screenshots": [],
        }

    def create(self):
        return artifact.create(self.root, "orders-review", self.report)

    def test_report_escapes_content_and_links_actual_app(self):
        folder = self.create()
        html = (folder / "index.html").read_text()
        self.assertNotIn("<script>alert", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn("http://localhost:3000/orders?mode=demo&amp;state=empty", html)
        self.assertNotIn("<iframe", html)
        self.assertIn("Real integration is not verified.", html)

    def test_cleanup_needs_exact_confirmation_and_preserves_source(self):
        source = self.root / "src.tsx"
        source.write_text("user code")
        folder = self.create()
        with self.assertRaises(ValueError):
            artifact.clean(self.root, "orders-review", "yes")
        self.assertTrue(folder.exists())
        artifact.clean(self.root, "orders-review", "orders-review")
        self.assertFalse(folder.exists())
        self.assertEqual(source.read_text(), "user code")

    def test_refuses_overwrite_and_untracked_cleanup(self):
        folder = self.create()
        with self.assertRaises(FileExistsError):
            self.create()
        extra = folder / "user-note.md"
        extra.write_text("keep")
        with self.assertRaises(ValueError):
            artifact.clean(self.root, "orders-review", "orders-review")
        self.assertTrue(extra.exists())

    def test_refuses_path_escape_and_symlink(self):
        for name in ("../src", "/tmp/foo", "a/b", "..", ""):
            with self.subTest(name=name), self.assertRaises(ValueError):
                artifact.create(self.root, name, self.report)
        outside = self.root / "outside"
        outside.mkdir()
        (self.root / "linked").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            artifact.create(self.root, "linked", self.report)

    def test_rejects_unsafe_urls_and_missing_delivery_sections(self):
        for url in ("javascript:alert(1)", "file:///sample/local/data.txt", "//example.com", "https://user:secret@example.com"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                artifact.create(self.root, "unsafe", {**self.report, "app_url": url})
        for key in ("flows", "changes", "checks", "backend", "limitations", "data_mode"):
            bad = dict(self.report)
            del bad[key]
            with self.subTest(key=key), self.assertRaises(ValueError):
                artifact.create(self.root, "missing", bad)

    def test_refuses_modified_or_forged_manifest(self):
        folder = self.create()
        (folder / "index.html").write_text("user edited this")
        with self.assertRaises(ValueError):
            artifact.clean(self.root, "orders-review", "orders-review")
        manifest = folder / "manifest.json"
        data = json.loads(manifest.read_text())
        data["files"]["../src.tsx"] = "bad"
        manifest.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            artifact.clean(self.root, "orders-review", "orders-review")

    def test_rejects_symlinked_artifact_base(self):
        outside = self.root / "outside"
        outside.mkdir()
        linked = self.root / "artifacts"
        linked.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            artifact.create(linked, "review", self.report)

    def test_capture_is_copied_and_source_survives_cleanup(self):
        source = self.root / "capture.png"
        source.write_bytes(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aL1kAAAAASUVORK5CYII="))
        self.report["screenshots"] = [{"path": str(source), "caption": "Current test capture, 1x1, fixture"}]
        folder = self.create()
        self.assertEqual((folder / "capture-1.png").read_bytes(), source.read_bytes())
        stored = json.loads((folder / "report.json").read_text())
        self.assertEqual(stored["screenshots"][0]["path"], "capture-1.png")
        artifact.clean(self.root, "orders-review", "orders-review")
        self.assertTrue(source.exists())

    def test_blocked_preview_omits_application_link(self):
        self.report.update(status="BLOCKED", app_url=None)
        folder = self.create()
        html = (folder / "index.html").read_text()
        self.assertIn("Application preview unavailable", html)
        self.assertNotIn("Open the actual application", html)


if __name__ == "__main__":
    unittest.main()
