import gooey
gooey_root = os.path.dirname(gooey.__file__)

block_cipher = None

a = Analysis(['AI_Clerk_helper.py'],  # replace me with the main entry point
             pathex=['./AI_Clerk_helper.py'], # replace me with the appropriate path
             binaries=[],
             datas=[],
             hiddenimports=['pkg_resources.py2_warn'],
             hookspath=['./hooks'],
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
          name='AI_Clerk_helper_v0.8.2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=['vcruntime140.dll', 'python36.dll'],
          runtime_tmpdir=None,
          console=False,
          icon=os.path.join(gooey_root, 'images', 'program_icon.ico'))


