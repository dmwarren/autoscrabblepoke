from . import conf
import logging
from logging import handlers
import sys

# m = main log
m = logging.getLogger('main')
m_handler = logging.FileHandler(filename=conf.c['log_file'])
m.setLevel(int(conf.c['log_level'])-1)
fmt = logging.Formatter(fmt='%(asctime)s %(message)s',
                        datefmt='%b %e %Y %H:%M:%S')
m_handler.setFormatter(fmt)
m.addHandler(m_handler)

# log to stdout, too
# hat tip: https://stackoverflow.com/a/14058475
cons = logging.StreamHandler(sys.stdout)
cons.setLevel(int(conf.c['log_level'])-1)
cons.setFormatter(fmt)
m.addHandler(cons)
