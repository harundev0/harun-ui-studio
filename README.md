# Harun UI Studio

Skill pribadi untuk UI/UX design, frontend development, dan frontend integration. Prioritasnya memahami struktur proyek, menggunakan kembali yang sudah ada, menjaga kerapihan kode, serta menyerahkan hasil yang dapat ditinjau melalui tautan dan bukti pengujian.

## Lokasi dan penggunaan

Source skill: `harun-ui-studio/SKILL.md`.

Instalasi global OpenCode V2: `~/.config/opencode/skills/harun-ui-studio/`.

Mulai sesi baru bila katalog skill belum diperbarui. Gunakan `/harun-ui-studio` jika tersedia di menu skill, atau tulis:

```text
Gunakan skill harun-ui-studio untuk merapikan halaman Orders.
Pelajari struktur proyek terlebih dahulu. Gunakan komponen, token, dan
integrasi yang sudah ada. API yang belum tersedia memakai fixture frontend.
Berikan link aplikasi, artifact review, flow akses, perubahan per file,
hasil pengujian, dan handoff backend. Jangan commit atau push.
```

Skill tidak mensyaratkan stack tertentu. React, Next.js, Vue, native, maupun stack lain mengikuti struktur yang benar-benar ditemukan. Integrasi backend hanya dikonsumsi dari frontend; backend tetap menjadi tanggung jawab pemilik backend.

## Flow pengerjaan

1. **Inspeksi:** baca instruksi proyek, manifest, route, imports/callers, komponen, tokens, font, styles, client, hooks, contracts, mocks, dan perubahan pengguna.
2. **Pemetaan reuse:** catat path yang sudah ada serta keputusan reuse/compose/extend. Komponen baru membutuhkan alasan konkret setelah pencarian.
3. **Penentuan scope:** refine, redesign, atau new surface; klasifikasikan kebutuhan marketing, product UI, reading, atau portfolio.
4. **Implementasi:** kerjakan irisan kecil end-to-end di frontend. Ikuti penamaan, folder, state ownership, dependency, dan library yang ada.
5. **Data:** gunakan integrasi existing jika tersedia. Jika belum, gunakan fixture deterministik, opt-in, dan tidak aktif pada produksi. Jangan membuat server/API palsu.
6. **Pengujian:** jalankan pemeriksaan frontend yang relevan, lalu Playwright pada aplikasi sebenarnya. Periksa desktop/mobile, keyboard, flow utama, state, serta error console/network.
7. **Perbaikan:** perbaiki temuan dalam satu batch dan konfirmasi. Hindari pengulangan polish tanpa temuan konkret.
8. **Penyerahan:** status, link aplikasi dan artifact, langkah akses, perubahan setiap file, bukti pengujian, keterbatasan, dan handoff backend.
9. **Review pengguna:** source dan artifact tetap tersedia. Review bukan perintah Git.
10. **Cleanup:** hanya setelah instruksi penghapusan. Utility memeriksa manifest dan hash agar tidak menghapus file yang berubah atau tidak dimilikinya.

## Isi paket

| File | Fungsi |
| --- | --- |
| `harun-ui-studio/SKILL.md` | Aturan inti yang dimuat saat aktivasi |
| `references/workflow.md` | Struktur kode, reuse, visual quality, accessibility, dan verifikasi |
| `references/skill-routing.md` | Pemilihan skill desain/ECC sesuai kebutuhan dan penyelesaian konflik |
| `references/integration.md` | Fixture, batas frontend/backend, dan format handoff |
| `references/delivery.md` | Link, flow akses, perubahan per file, artifact, dan cleanup |
| `scripts/artifact.py` | Generator, server lokal, dan penghapusan report dengan pemeriksaan kepemilikan |
| `tests/test_artifact.py` | Tes perilaku utility artifact |

Path pada tabel setelah baris pertama berada di dalam `harun-ui-studio/`.

## Skill pendukung

Sumber desain: `ui-ux-pro-max`, `emil-design-eng`, `design-taste-frontend`, `impeccable`, `caveman`, dan `ponytail`. `design-taste-frontend-v1` hanya untuk permintaan kompatibilitas legacy; tidak ditumpuk dengan v2.

Dukungan ECC yang dirutekan sesuai kebutuhan: `frontend-patterns`, `react-patterns`, `frontend-a11y`, `react-performance`, `react-testing`, `e2e-testing`, `contract-first`, dan `coding-standards`. Skill framework lain mengikuti stack proyek.

Tidak semua skill dimuat sekaligus. Misalnya, perbaikan spacing tidak perlu memuat seluruh panduan animasi, integrasi, dan React performance. Aturan inti mempertahankan hasil yang harus dipenuhi; referensi dibaca sesuai tahap pekerjaan.

## Aturan penting

- Komponen, warna, typography, icon family, client, dan hooks existing menjadi sumber utama.
- Tidak ada pekerjaan API handler, server action, database, migration, auth service, atau infrastructure.
- Tidak ada automatic stage, commit, push, deployment, atau PR.
- Copy bahasa Inggris memakai grammar yang benar dan sentence case, mengikuti proper nouns serta konvensi produk.
- Chat ringkas; flow akses dan handoff tetap lengkap.
- Status frontend-ready berbeda dari integrasi real yang sudah terverifikasi.
- Artifact adalah report dengan akses ke implementasi aktual dan capture terbaru, bukan duplikat desain HTML yang bisa berbeda dari web asli.
- Server preview lokal hanya alat review. Tidak ada publikasi atau tunnel otomatis.

## Mengakses artifact pembuatan skill ini

Report: `http://127.0.0.1:8765/` selama proses report berjalan pada komputer ini.

Folder: `.ui-artifacts/skill-review/` pada workspace ini. Report ini menjelaskan skill dan hasil uji; workspace awal kosong sehingga tidak ada aplikasi produk yang didesain ulang pada tugas ini.

Langkah review:

1. Buka URL report.
2. Baca **Access flows** untuk penggunaan skill dan cleanup.
3. Baca **Changes** untuk tanggung jawab masing-masing file.
4. Baca **Verification** dan **Limitations** untuk cakupan yang benar-benar diuji.
5. Buka `harun-ui-studio/SKILL.md` untuk aturan lengkap, atau `TEST-REPORT.md` untuk detail evaluasi.
6. Gunakan skill di proyek frontend nyata melalui prompt contoh di atas.

Untuk menyalakan kembali report dari workspace ini:

```bash
python3 harun-ui-studio/scripts/artifact.py serve \
  --base "$PWD/.ui-artifacts" --id skill-review --port 8765
```

`127.0.0.1` hanya dapat diakses dari komputer yang menjalankan server. File report dapat dibuka langsung melalui `.ui-artifacts/skill-review/index.html` jika server berhenti.

## Menghapus artifact

Katakan: **“Sudah, hapus artifact skill-review.”**

“Sudah bagus” saja diperlakukan sebagai acknowledgment review, bukan instruksi menghapus file. Jika ingin menghapus manual setelah review:

```bash
python3 harun-ui-studio/scripts/artifact.py clean \
  --base "$PWD/.ui-artifacts" --id skill-review --confirm skill-review
```

Hentikan proses server report milik task tersebut saja. Jangan hentikan server aplikasi bersama. Penghapusan artifact tidak menghapus skill, source frontend, atau dokumentasi handoff. File yang berubah atau tidak terdaftar membuat cleanup ditolak agar dapat diperiksa terlebih dahulu.

## Menjalankan tes

```bash
python3 -m unittest discover -s harun-ui-studio/tests -v
```

Rincian hasil ada di `TEST-REPORT.md`. Tes lokal dan simulasi perilaku bukan bukti kesempurnaan atau kesetaraan semua model. Skill mengurangi ruang improvisasi melalui reuse map, output wajib, fixture deterministik, dan acceptance gates; evaluasi lintas model murah/mahal belum dilakukan.
