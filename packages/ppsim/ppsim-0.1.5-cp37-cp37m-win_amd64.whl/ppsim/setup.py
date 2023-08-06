from distutils.core import setup
from Cython.Build import cythonize
import numpy as np
from os.path import join
from setuptools.extension import Extension


inc_path = np.get_include()
lib_path = join(np.get_include(), '..', '..', 'random', 'lib')

distributions = Extension("simulator",
                          sources=[join('', 'simulator.pyx')],
                          include_dirs=[inc_path],
                          library_dirs=[lib_path],
                          libraries=['npyrandom']
                          )


setup(
    ext_modules=cythonize(distributions, compiler_directives={'language_level': "3"})
)
