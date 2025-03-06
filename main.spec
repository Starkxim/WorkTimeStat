# -*- mode: python ; coding: utf-8 -*-

import datetime

# 获取当前日期和时间，并格式化为字符串
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M")

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
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
    [],
    exclude_binaries=True,
    name='WorkTimeStat',
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
    version='version-file.txt',  # 添加版本信息文件
    icon='WorkTimeIcon.jpg',  # 添加图标文件
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=f'WTS_{current_time}',  # 使用当前日期和时间作为输出目录的名称
)
