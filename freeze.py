from cx_Freeze import setup, Executable
import sys

TARGET = 'nerissimo'
EXCLUDE = []
PACKAGES = []
INCLUDE_FILES = ['resources']

# Dependencies are automatically detected, but it might need
# fine tuning.
# Optimize = 1 keeps docstrings, unfortunately it is required by numpy
# which would crash without them (unknown reason
build_options = {'packages': PACKAGES, 'excludes': EXCLUDE, 'optimize': 1,
                 'include_files': INCLUDE_FILES, 'include_msvcr': True}

base = 'gui' if sys.platform == 'win32' else None

executables = [
    Executable('desktop_main.py', base=base, target_name=TARGET),
]

setup(name='Nerissimo',
      version='1.0',
      description='',
      options={'build_exe': build_options},
      executables=executables)
