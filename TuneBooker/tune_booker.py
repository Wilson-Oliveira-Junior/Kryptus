#!/usr/bin/env python3

from input_parser import *
import sys

def main():
    parser = create_parser()

    if len(sys.argv)==1:
        parser.print_usage(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)

if __name__ == "__main__":
    main()
