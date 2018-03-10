import os
from sys import version_info

if version_info[0] < 3:
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser

tmp_conf = ConfigParser()
tmp_path = os.path.dirname(os.path.abspath(__file__))  # /base/lib/here
tmp_path = tmp_path.split('/')
conf_path = '/'.join(tmp_path[0:-1])   # /base/lib
tmp_conf.read(conf_path+'/scrabblepoke.conf')
c = {}
c.update(tmp_conf.items('default'))
