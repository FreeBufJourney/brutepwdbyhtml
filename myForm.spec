# -*- mode: python -*-

block_cipher = None


a = Analysis(['myForm.py'],
             pathex=['C:\\Users\\Aaron\\Desktop\\new\\weakpasswordcheck'],
             binaries=None,
             datas=[('WIFI_CHEAT.ico',''),('C:\\Users\\Aaron\\Desktop\\new\\weakpasswordcheck\\WIFI_CHEAT.ico',''),],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='myForm',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='WIFI_CHEAT.ico')
