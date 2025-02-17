# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['.', './ui', './DataProcess'],  # 添加相关路径
    binaries=[],
    datas=[
        ('ui/', 'ui/'),  # 添加ui文件夹
        ('DataProcess/', 'DataProcess/'),  # 添加DataProcess文件夹
        ('HolidayData/', 'HolidayData/'),  # 假设有一个HolidayData文件夹
        ('tests/', 'tests/'),  # 添加tests文件夹
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['hook.py'],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
