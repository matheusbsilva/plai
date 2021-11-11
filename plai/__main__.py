import signal
import sys
import argparse

from .environment import env
from .interpreter import run
from .interpreter import eval
from .parser import parse


def signal_handler(sig, frame):
    print('Exiting..')
    sys.exit(0)


def parse_cli():
    description = """\
    plAI programming language to easily build machine learning pipelines\
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('file', nargs='?',
                        type=argparse.FileType('r'),
                        default=None, help='.plai file to be executed')

    return parser


def main():
    parser = parse_cli()
    args = parser.parse_args()
    file = args.file

    e = env()

    if file:
        src = file.read()
        res = None

        if src:
            ast = parse(src)
            res = eval(ast, e)

        print(res)

        return 0

    while True:
        # Exit on ctrl + C
        signal.signal(signal.SIGINT, signal_handler)
        src = input('plai >>> ')

        res = run(src, e)
        print(res)


if __name__ == '__main__':
    main()
