import os
import subprocess

import os
path = os.path.join(os.path.join(os.path.expanduser('~')), '.bash_profile')
def config_dir():
    with open(path,'a') as file:
        file.write('export PATTOO_CONFIGDIR=~/opt/Calico/config')


config_dir()
    