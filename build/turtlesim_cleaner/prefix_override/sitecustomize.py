import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/muhie/Desktop/dev_ps/install/turtlesim_cleaner'
