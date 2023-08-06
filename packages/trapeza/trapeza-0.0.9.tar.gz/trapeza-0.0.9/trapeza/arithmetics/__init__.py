import ctypes
import pathlib
import os


if os.name == 'nt':
    ctypes.CDLL(str(pathlib.Path(__file__).parents[1] / 'src/win/mpdecimal-2.5.1/libmpdec/libmpdec-2.5.1.dll'))


from trapeza.arithmetics.dtoa import py_dtoa_ryu
