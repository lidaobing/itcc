import sys
import os.path
import distutils.util

sys.path.insert(0,
                os.path.abspath('../build/lib.%s-%s' %
                    (distutils.util.get_platform(), sys.version[0:3])))
