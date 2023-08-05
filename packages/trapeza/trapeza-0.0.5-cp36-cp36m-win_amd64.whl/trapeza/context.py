# 'FLOAT', 'DECIMAL', 'LIBMPDEC_FAST' (uses ryu dtoa), 'LIBMPDEC' (uses dtoa of Cpython)
ARITHMETICS = 'LIBMPDEC_FAST'

# precision (total number of significant digits in number representation) when ARITHMETICS is set to
#   'DECIMAL', 'LIBMPDEC_FAST', 'LIBMPDEC'
ARBITRARY_DECIMAL_PRECISION = 28

# maximum number of decimal places after radix point to restrict precision inflation during e.g. multiplication
#   when ARITHMETICS is set to 'DECIMAL', 'LIBMPDEC_FAST', 'LIBMPDEC'
ARBITRARY_QUANTIZE_SIZE = 10    # int

# todo fixed point size not implemented yet
# FIXED_POINT_SIZE = 6

# ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_EVEN, ROUND_HALF_TOWARDS_ZERO, ROUND_HALF_AWAY_FROM_ZERO
# ROUND_UP, ROUND_DOWN, ROUND_05UP: only for DECIMAL and LIBMPDEC
ROUNDING = 'ROUND_HALF_EVEN'
