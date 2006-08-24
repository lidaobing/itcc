import sys
import os.path
import distutils.util

path = os.path.abspath('../build/lib.%s-%s' %
                         (distutils.util.get_platform(), sys.version[0:3]))
if not os.path.exists(path):
    sys.stderr.write('please build first\n')
    sys.exit(1)

sys.path.insert(0, path)
