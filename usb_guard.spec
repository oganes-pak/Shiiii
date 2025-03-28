# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['usb_guard.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\WINDOWS\\system32\\venv\\Lib\\site-packages\\kivy', './kivy'), ('C:\\WINDOWS\\system32\\venv\\Lib\\site-packages\\kivy\\data', './kivy_install/data'), ('C:\\WINDOWS\\system32\\venv\\share\\sdl2\\bin', './'), ('C:\\WINDOWS\\system32\\venv\\share\\glew\\bin', './'), ('C:\\WINDOWS\\system32\\venv\\share\\angle\\bin', './')],
    hiddenimports=['kivy'],
    hookspath=['.'],
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
    name='usb_guard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
