# -*- coding: utf-8 -*-

# A very simple setup script to create a single executable built from a module
# which includes an executable section protected by "if __name__ == '__main__'
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from cx_Freeze import setup, Executable

executables = [
    Executable('Login.py', base = "Win32GUI"),
]

setup(name='Login',
      version='0.1.1',
      description='Log into TF',
      options = {"build_exe": {"packages":["idna","Tkinter", "requests"]}},
      executables=executables
      )

build_exe_options = {"packages": ["os", "idna", "idnadata"]}
packages = ['idna', 'idnadata']
