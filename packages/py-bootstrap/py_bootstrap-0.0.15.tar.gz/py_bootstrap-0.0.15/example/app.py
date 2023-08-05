import sys
import os
sys.path.append(os.path.abspath(''))

from py_bootstrap import config,get_app_homepage

print(get_app_homepage('file'))