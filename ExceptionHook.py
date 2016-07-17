from datetime import datetime
import sys
import threading
import traceback as TB
from util import FileIO


def install_thread_excepthook():
    """
    Workaround for sys.excepthook thread bug
    (https://sourceforge.net/tracker/?func=detail&atid=105470&aid=1230540&group_id=5470).
    Call once from __main__ before creating any threads.
    If using psyco, call psyco.cannotcompile(threading.Thread.run)
    since this replaces a new-style class method.
    """
    run_old = threading.Thread.run

    def run(*args, **kwargs):
        try:
            run_old(*args, **kwargs)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            sys.excepthook(*sys.exc_info())

    threading.Thread.run = run


def uncaught_exception(exception_type, exception, traceback):
    if issubclass(exception_type, KeyboardInterrupt):
        print()
        sys.exit('Exited')
    else:
        time = str(datetime.now())
        print()
        traceback_str = ''.join(TB.format_tb(traceback))
        print(traceback_str)
        print(exception_type.__name__)
        log = '[' + time + ']\n'
        log += 'Exception Type: ' + exception_type.__name__ + '\n'
        log += 'Traceback:\n'
        log += traceback_str
        log += '\n\n\n'
        FileIO.append('error.log', log)
