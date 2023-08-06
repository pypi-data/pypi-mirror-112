import sys, os
try:
    import oss2
except ModuleNotFoundError:
    os.system(f'{sys.executable} -m pip install oss2')
    import oss2

