import warnings
from distutils.core import setup
from Cython.Build import cythonize

warnings.filterwarnings("ignore", category=FutureWarning)

setup(
    ext_modules=cythonize("libc.pyx"),
)
