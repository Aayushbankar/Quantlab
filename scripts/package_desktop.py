#!/usr/bin/env python3
"""Package Pramaan desktop executable, tarball, debian installer, and SHA256 checksums."""

import hashlib
import os
import shutil
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
SOURCE_BIN = ROOT / "frontend" / "src-tauri" / "target" / "release" / "pramaan-desktop"

def compute_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    DIST.mkdir(parents=True, exist_ok=True)
    assert SOURCE_BIN.exists(), f"Source binary not found at {SOURCE_BIN}"

    # 1. Copy and strip binary
    dest_bin = DIST / "pramaan-desktop"
    shutil.copy2(SOURCE_BIN, dest_bin)
    subprocess.run(["strip", str(dest_bin)], check=True)
    os.chmod(dest_bin, 0o755)
    print(f"[OK] Stripped binary: {dest_bin} ({dest_bin.stat().st_size / 1024 / 1024:.2f} MB)")

    # 2. Create standalone tarball
    tarball = DIST / "pramaan-desktop-linux-x86_64.tar.gz"
    with tarfile.open(tarball, "w:gz") as tar:
        tar.add(dest_bin, arcname="pramaan-desktop")
    print(f"[OK] Created tarball: {tarball} ({tarball.stat().st_size / 1024 / 1024:.2f} MB)")

    # 3. Create Debian package
    deb_dir = ROOT / "target" / "deb_build"
    if deb_dir.exists():
        shutil.rmtree(deb_dir)
    deb_dir.mkdir(parents=True, exist_ok=True)

    debian_bin_file = deb_dir / "debian-binary"
    debian_bin_file.write_text("2.0\n")

    # control.tar.gz
    control_content = """Package: pramaan-desktop
Version: 1.0.0
Section: finance
Priority: optional
Architecture: amd64
Maintainer: Aayush Bankar <aayushbankar42@gmail.com>
Depends: libwebkit2gtk-4.1-0 | libwebkit2gtk-4.0-37 | libc6 (>= 2.31)
Description: Pramaan - Event-driven backtesting engine & overfitting diagnostics
 Pramaan is an event-driven backtesting engine for Indian (NSE) equities
 enforcing zero look-ahead T+1 execution, statutory delivery costs (STT, GST,
 Stamp Duty, SEBI turnover), and Marcos López de Prado overfitting diagnostics
 (Deflated Sharpe Ratio, CPCV with embargo).
"""
    control_tar = deb_dir / "control.tar.gz"
    with tarfile.open(control_tar, "w:gz") as tar:
        ti = tarfile.TarInfo("control")
        ti.size = len(control_content.encode("utf-8"))
        ti.mode = 0o644
        ti.mtime = 0
        import io
        tar.addfile(ti, io.BytesIO(control_content.encode("utf-8")))

    # data.tar.gz
    data_tar = deb_dir / "data.tar.gz"
    desktop_entry = """[Desktop Entry]
Name=Pramaan
Comment=Honest Backtesting Engine for Indian Equities
Exec=pramaan-desktop
Icon=pramaan
Terminal=false
Type=Application
Categories=Finance;Education;Science;
"""
    icon_src = ROOT / "frontend" / "src-tauri" / "icons" / "128x128.png"

    with tarfile.open(data_tar, "w:gz") as tar:
        # usr/bin/pramaan-desktop
        ti = tarfile.TarInfo("usr/bin/pramaan-desktop")
        ti.size = dest_bin.stat().st_size
        ti.mode = 0o755
        ti.mtime = int(dest_bin.stat().st_mtime)
        with open(dest_bin, "rb") as bf:
            tar.addfile(ti, bf)

        # usr/share/applications/pramaan-desktop.desktop
        ti_desk = tarfile.TarInfo("usr/share/applications/pramaan-desktop.desktop")
        ti_desk.size = len(desktop_entry.encode("utf-8"))
        ti_desk.mode = 0o644
        ti_desk.mtime = 0
        tar.addfile(ti_desk, io.BytesIO(desktop_entry.encode("utf-8")))

        # usr/share/icons/hicolor/128x128/apps/pramaan.png
        if icon_src.exists():
            ti_icon = tarfile.TarInfo("usr/share/icons/hicolor/128x128/apps/pramaan.png")
            ti_icon.size = icon_src.stat().st_size
            ti_icon.mode = 0o644
            ti_icon.mtime = 0
            with open(icon_src, "rb") as ic:
                tar.addfile(ti_icon, ic)

    # Assemble deb with ar
    deb_out = DIST / "pramaan-desktop_1.0.0_amd64.deb"
    if deb_out.exists():
        deb_out.unlink()

    # Call ar rcs
    subprocess.run(
        ["ar", "rcs", str(deb_out), str(debian_bin_file), str(control_tar), str(data_tar)],
        check=True
    )
    print(f"[OK] Created Debian package: {deb_out} ({deb_out.stat().st_size / 1024 / 1024:.2f} MB)")

    # 4. Generate SHA256SUMS.txt
    artifacts = [
        DIST / "pramaan-desktop",
        DIST / "pramaan-desktop_1.0.0_amd64.deb",
        DIST / "pramaan-desktop-linux-x86_64.tar.gz",
        ROOT / "Pramaan_Presentation.pptx",
        ROOT / "Pramaan_Presentation.pdf",
        ROOT / "docs" / "Pramaan_Report_Team.pdf",
        ROOT / "docs" / "Pramaan_Report_Aayush_Avinash_Bankar.pdf",
        ROOT / "docs" / "Pramaan_Report_Meet_Jayeshbhai_Patel.pdf",
    ]

    manifest_lines = []
    for art in artifacts:
        if art.exists():
            digest = compute_sha256(art)
            manifest_lines.append(f"{digest}  {art.name}")
            print(f"  {digest}  {art.name}")

    sha_file = DIST / "SHA256SUMS.txt"
    sha_file.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    print(f"[OK] Wrote manifest to {sha_file}")

if __name__ == "__main__":
    main()
