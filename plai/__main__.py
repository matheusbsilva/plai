import signal
import sys

from .environment import env
from .interpreter import run


def signal_handler(sig, frame):
    print('Exiting..')
    sys.exit(0)


def main():
    # Exit on ctrl + C
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        src = input('plai >>> ')

        e = env()
        res = run(src, e)

        # print AST for debugging
        print(res)


if __name__ == '__main__':
    main()
