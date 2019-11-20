import signal
import sys

from .parser import parse

def signal_handler(sig, frame):
    print('Exiting..')
    sys.exit(0)


def main():
    # Exit on ctrl + C
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        src = input('plai >>> ')
        ast = parse(src)

        # print AST for debugging
        print(ast.pretty())


if __name__ == '__main__':
    main()
