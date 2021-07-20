  
# A setup script to demonstrate the use of distutils
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

#from cx_Freeze import setup, Executable

#buildOptions = dict(zip_include_packages=["*"], zip_exclude_packages=[])
#executables = [Executable("main.py")]

#setup(name='main.py',
#      version='0.1',
#      description='cx_Freeze script to test distutils',
#      executables=executables,
#      options=dict(build_exe=buildOptions))

import cx_Freeze

# executables = [cx_Freeze.Executable("main3.py"),  cx_Freeze.Executable("main2_coop.py")]
executables = [cx_Freeze.Executable("../runGame.py")]

cx_Freeze.setup(
    name="A bit Racey",
    options={"build_exe": { "packages":["pygame"],
                          }},
    executables = executables

    )