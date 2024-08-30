# -*- mode: python ; coding: utf-8 -*-

import os

# Get the absolute path of the current directory
spec_root = os.path.abspath(os.getcwd())

block_cipher = None

a = Analysis(['main.py'],
             pathex=[spec_root],
             binaries=[],
             datas=[('icons', 'icons')],  # Include the entire icons folder
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='RNGwall',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='icons\\RNGwall.ico' )