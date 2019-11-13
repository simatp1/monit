#!/usr/bin/env python3

import args


def main():
    ARGS = args.parse_args()

    if ARGS.version:
        print("not defined yet")

    if ARGS.cmd == 'resources':
        print('monitor resources')
    elif ARGS.cmd == 'jobs':
        print('job monitoring not implemented yet')


if __name__ == "__main__":
    main()
