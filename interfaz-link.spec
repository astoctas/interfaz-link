# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['src/main/python/main.py'],
             pathex=['.'],
             binaries=[],
             datas=[
                ('src/main/python/mainwindow.ui', '.'),
                ('src/main/python/icons/base/64.png', './icons/base/'),
                ('src/main/python/modules', 'modules'),
                ('src/main/python/templates/index.html', 'templates'),
                ('src/main/python/templates/socket.io.min.js', 'templates')
              ],
             hiddenimports=['engineio.async_drivers.threading'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='interfaz-link',
    debug=False,
    strip=False,
    upx=False,
    console=False,
    runtime_tmpdir="."
)