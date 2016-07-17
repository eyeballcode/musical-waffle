#!/usr/bin/env python
from chatbot import login
import sys
import ExceptionHook

ExceptionHook.install_thread_excepthook()
sys.excepthook = ExceptionHook.uncaught_exception


def main():
    bot = None
    room = 0
    if login.can_login_from_config():
        print('Logging in from config')
        bot, room = login.login_from_config()
    elif login.can_login_from_env():
        print('Logging in using environment variables')
        bot, room = login.login_from_env()
    elif login.can_login_from_args():
        print('Logging in using args')
        bot, room = login.login_from_args()
    else:
        print('Logging in...')
        login.login_on_the_spot()


if __name__ == '__main__':
    main()
