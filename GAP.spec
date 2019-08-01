# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['GAP.py'],
             pathex=['D:\\Coding\\AnalysisPrograms2013\\Fossil\\working\\common', 'D:\\Coding\\AnalysisPrograms2013\\Fossil\\working\\libraries', 'D:\\Coding\\AnalysisPrograms2013\\Fossil\\working\\Geoduck'],
             binaries=[],
             datas=[],
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
          name='GAP',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
