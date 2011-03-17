import os
from datetime import datetime
from traceback import format_exc

def write_trace(log, force=False):
    trace = False
    std_out = False

    if trace or force:
        if std_out:
            print log
        path = os.path.join(os.path.dirname(__file__), 'trace.txt')
        f = open(path, 'a')
        f.write(datetime.today().strftime('%c') + ': ' + log.encode('ascii', 'ignore') + '\n')

def write_error(error):
    std_out = False
    if std_out:
        print error
    #	f = open('error.txt', 'a')
    #	f.write(datetime.today().strftime('%c') + ': ' + error.encode('ascii', 'ignore') + '\n')
    raise error.encode('ascii', 'ignore')
