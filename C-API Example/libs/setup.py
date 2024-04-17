

# Script para compilar o código C

def run():
    from distutils.core import setup, Extension
    from os import path, listdir, removedirs
    from shutil import move, rmtree
    import numpy as np
    curFolder = path.dirname(path.abspath(__file__))

    ext = [
        Extension(
            name= 'fft_c',
            sources=[path.join(curFolder, 'fft_c.cpp')],
            include_dirs=[np.get_include()],
        ),
    ]
    setup(
        name='ffc_c',
        ext_modules=ext,
        script_args=["build_ext", "-b", "build", "-if"]
    )
    # Clean up
    for _file in listdir():
        if _file.endswith('.pyd'):
            move(_file, path.join(curFolder, _file))
    rmtree('build')

if __name__ == '__main__':
    run()
