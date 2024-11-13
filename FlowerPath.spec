# -*- mode: python ; coding: utf-8 -*-
# .Spec Generation file: pyinstaller --onefile --windowed --icon="images/flower_icon.ico" --add-data "images;images" --add-data "placeholders_assets;placeholder_assets" --name FlowerPath main.py
# Regenerate .exe: pyinstaller FlowerPath.spec     

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('images', 'images'), ('placeholders_assets', 'placeholder_assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FlowerPath',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['images\\flower_icon.ico'],
)
