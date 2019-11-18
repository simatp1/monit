#!/usr/bin/env python3

import args
from collectors import condor, p1, panda


def main():
    ARGS = args.parse_args()

    if ARGS.version:
        print("not defined yet")

    if ARGS.cmd == 'resources':
        results = monitor_resources(ARGS)
    elif ARGS.cmd == 'jobs':
        print('job monitoring not implemented yet')

    if ARGS.out == 'table':
        from reporters import table
        table.report(results)
    elif ARGS.out == 'influx':
        try:
            from reporters import influx
            influx.report(results, ARGS.host, ARGS.passwd)
        except AttributeError as e:
            print("Output to influx reuqires a database host and password", e)
            exit(1)


def monitor_resources(arguments):
    # manages information flow for resources monitoring
    available_hosts, time = p1.list_resources()
    condor_resources = condor.list_resources(
        arguments.pool)
    panda.list_resources()

    return condor_resources


if __name__ == "__main__":
    main()
