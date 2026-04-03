# InkNote.spec

import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

hiddenimports = collect_submodules("ttkbootstrap")

version_file = "version.txt" if os.path.exists("version.txt") else None

a = Analysis(
    ["src/inknote/main.py"],
    pathex=["src"],
    binaries=[],
    datas=[],
    hiddenimport=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    )

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="InkNote",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="assets/inknote.ico",
    version=version_file,
    )

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="InkNote",
    )

