from setuptools import setup, find_packages
from distutils.extension import Extension
import sys
import os
import re
import pathlib


# >>>replace .pyx with .c or .cpp if we do not use cython for compilation
# https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#distributing-cython-modules
def no_cythonize(exts, **_ignore):
    for extension in exts:
        sources = []
        for sfile in extension.sources:
            path, ext = os.path.splitext(sfile)
            if ext in (".pyx", ".py"):
                if extension.language == "c++":
                    ext = ".cpp"
                else:
                    ext = ".c"
                sfile = path + ext
            sources.append(sfile)
        extension.sources[:] = sources
    return exts


# >>>determine if cython is available
try:
    from Cython.Build import cythonize
    from Cython.Distutils import build_ext

    CYTHON_IMPORT = True
except ImportError:
    cythonize = None
    build_ext = None
    CYTHON_IMPORT = False

# >>>define extensions
ext_dtoa = Extension("trapeza.arithmetics.dtoa",
                     sources=["trapeza/arithmetics/dtoa.pyx", "trapeza/src/ryu/d2s.c"],
                     include_dirs=["trapeza/src/emyg/"] + ["trapeza/src/ryu/"],
                     language='c')

ext_cdecimal = Extension("trapeza.arithmetics.cdecimal",
                         sources=["trapeza/arithmetics/cdecimal.pyx"],
                         language='c')

ext_cfloat = Extension("trapeza.arithmetics.cfloat",
                       sources=["trapeza/arithmetics/cfloat.pyx"],
                       language='c')

ext_arithmetics = Extension("trapeza.arithmetics.arithmetics",
                            sources=["trapeza/arithmetics/arithmetics.pyx"],
                            language='c')

ext_strategy = Extension("trapeza.strategy.fx_strategy", sources=["trapeza/strategy/fx_strategy.pyx"],
                         language='c++')

ext_account = Extension("trapeza.account.fx_account",
                        sources=["trapeza/account/fx_account.pyx"],
                        language='c++')

ext_execution_heap = Extension("trapeza.account.execution_heap",
                               sources=["trapeza/account/execution_heap.pyx"],
                               language='c++')

# >>>mpdecimal is platform dependent
if os.name == 'nt':
    # windows
    ext_libmpdec = Extension("trapeza.arithmetics.libmpdec",
                             sources=["trapeza/arithmetics/libmpdec.pyx"],
                             libraries=["libmpdec-2.5.1"],
                             library_dirs=["trapeza/src/win/mpdecimal-2.5.1/libmpdec/"],
                             include_dirs=["trapeza/src/"] + ["trapeza/src/win/mpdecimal-2.5.1/"] +
                                          ["trapeza/src/win/mpdecimal-2.5.1/libmpdec/"],
                             extra_objects=["trapeza/src/win/mpdecimal-2.5.1/libmpdec/libmpdec-2.5.1.dll.lib"],
                             language='c')
else:
    # linux or macOS
    ext_libmpdec = Extension("trapeza.arithmetics.libmpdec",
                             sources=["trapeza/arithmetics/libmpdec.pyx"],
                             library_dirs=["trapeza/src/linux/mpdecimal-2.5.1/libmpdec/"],
                             include_dirs=["trapeza/src/"] + ["trapeza/src/linux/mpdecimal-2.5.1/"] +
                                          ["trapeza/src/linux/mpdecimal-2.5.1/libmpdec/"],
                             language='c')

extensions = [ext_dtoa,
              ext_cdecimal,
              ext_cfloat,
              ext_libmpdec,
              ext_arithmetics,
              ext_strategy,
              ext_account,
              ext_execution_heap]

# >>>determine if user wants to use cython (if cython is available)
# we use --cython as command line argument
CYTHONIZE_ARG = False
if '--cython' in sys.argv:
    CYTHONIZE_ARG = True
    sys.argv.remove('--cython')

# >>>if we use cython to compile, then do some set up for cython compilation
compiler_directives = {'language_level': 3, 'embedsignature': False}
#                       'binding': False, 'cdivision': False, 'initializedcheck': False}
if CYTHONIZE_ARG:
    if CYTHON_IMPORT is False:
        raise RuntimeError('Cannot use --cython. Cython not installed/ not available! Please make sure Cython is '
                           'installed properly in your environment.')
    compile_extensions = cythonize(extensions, compiler_directives=compiler_directives, annotate=False,
                                   compile_time_env={'USE_LIBMPDEC': True})
    cmdclass = {'build_ext': build_ext}
else:
    compile_extensions = no_cythonize(extensions)
    cmdclass = {}

# >>>get requirements
with open('requirements.txt') as req:
    install_requires = req.read().strip().split('\n')

# >>>get version info
with open('trapeza/_version.py', 'rt') as ver:
    ver_str = ver.read()
    ver_search = r"^__version__ = ['\"]([^'\"]*)['\"]"
    m = re.search(ver_search, ver_str, re.M)
    if m:
        ver_str = m.group(1)
    else:
        raise RuntimeError('Unable to find version string.')


# >>>wrap setup()
def setup_call(_extensions, _install_requires, _cmdclass, _ver_str):
    setup(ext_modules=_extensions,
          install_requires=_install_requires,
          cmdclass=_cmdclass,
          packages=find_packages(exclude=('tests', 'profiling',)),
          data_files=[('trapeza/arithmetics', ['trapeza/src/win/mpdecimal-2.5.1/libmpdec/libmpdec-2.5.1.dll'])],
          include_package_data=True,
          name='trapeza',
          version=_ver_str,
          description='Backtesting and Simulation package for financial transactions and trading',
          long_description=(pathlib.Path(__file__).parent / 'README.md').read_text(),
          long_description_content_type='text/markdown',
          license='MIT',
          author='Louis Huebser',
          url='https://gitlab.com/LHuebser/trapeza.git',
          classifiers=[
              'Development Status :: 4 - Beta',
              'License :: OSI Approved :: MIT License',
              'Intended Audience :: Financial and Insurance Industry',
              'Intended Audience :: Science/Research',
              'Topic :: Scientific/Engineering',
              'Topic :: Scientific/Engineering :: Mathematics',
              'Topic :: Office/Business :: Financial :: Investment',
              'Operating System :: OS Independent',
              'Programming Language :: C',
              'Programming Language :: C++',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3 :: Only',
              'Programming Language :: Python :: Implementation :: CPython'],
          platforms='any',
          package_data={'trapeza/arithmetics': ['*.pxd']},
          zip_safe=False)


# >>>action, go!
# >>try to build package which might only work on windows due to libmpdec, which needs to be re-compiled on possix
try:
    setup_call(compile_extensions, install_requires, cmdclass, ver_str)
except Exception as e:
    # >>we're probably on possix and mpdecimal has not been compiled from source, so we try to build trapeza without
    #   libmpdec.pyx
    # noinspection PyTypeChecker
    print(e)
    print('Ooooppppsss something went wrong!')

    if CYTHON_IMPORT is False:
        raise RuntimeError('Cython not available. Cannot re-compile with cythonizing extensions. Please install '
                           'cython prior to installing trapeza.')

    print('Trying to cythonize and build without mpdecimal. mpdecimal probably needs to be re-compiled from '
          'source (e.g. on Possix). Continue building without mpdecimal. LIBMPDEC and LIBMPDEC_FAST will not '
          'be available for this build (DECIMAL as fallback). Consider re-building package from source. See '
          'Docs for instructions on how to build from source.')

    ref_extensions = [ext_dtoa,
                      ext_cdecimal,
                      ext_cfloat,
                      ext_arithmetics,
                      ext_strategy,
                      ext_account,
                      ext_execution_heap]

    ref_extensions = cythonize(ref_extensions, compiler_directives=compiler_directives, annotate=False,
                               compile_time_env={'USE_LIBMPDEC': False})
    cmdclass = {'build_ext': build_ext}

    setup_call(ref_extensions, install_requires, cmdclass, ver_str)
