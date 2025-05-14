# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

# Hidden imports from external libraries
hiddenimports = [
    'sqlite3', 'tkinter', 'tkinter.filedialog', 'tkinter.ttk',
]
hiddenimports += collect_submodules('transformers')
hiddenimports += collect_submodules('sentencepiece')
hiddenimports += collect_submodules('torch')

a = Analysis(
    ['main.py'],
    pathex=['/Users/simoneich/Desktop/Projects/Code/Python/Automation/Language Learn-App/language_learn'],
    binaries=[],
    datas=[
        ('gui/', 'gui'),
        ('data/', 'data'),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Spanish',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name='Spanish',
)

app = BUNDLE(
    coll,
    name='Spanish.app',
    icon=None,
    bundle_identifier='com.example.spanish',
)
