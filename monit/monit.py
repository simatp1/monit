#!/usr/bin/env python3

import args
from collectors import p1, condor


def main():
    ARGS = args.parse_args()

    if ARGS.version:
        print("not defined yet")

    if ARGS.cmd == 'resources':
        monitor_resources(ARGS)
    elif ARGS.cmd == 'jobs':
        print('job monitoring not implemented yet')


def monitor_resources(arguments):
    # manages information flow for resources monitoring
    available_hosts = p1.list_resources()
    condor_resources = condor.list_resources()

    print(available_hosts)
    print(condor_resources)


if __name__ == "__main__":
    main()
