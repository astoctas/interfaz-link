# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['src/main/python/main.py'],
             pathex=['/home/alejandro/Documentos/Interfaz2.0/Software/Python/interfaz-link'],
             binaries=[],
             datas=[('src/main/python/mainwindow.ui', '.')],
             hiddenimports=[],
             hookspath=[],
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
          name='interfaz-link',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
