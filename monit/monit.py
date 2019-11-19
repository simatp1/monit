#!/usr/bin/env python3

import args
from collectors import condor, p1, panda
from mappers.correlator import correlate
from reporters import influx, table


def main():
    ARGS = args.parse_args()

    if ARGS.version:
        print("not defined yet")

    if ARGS.cmd == 'resources':
        results = monitor_resources(ARGS)
    elif ARGS.cmd == 'jobs':
        print('job monitoring not implemented yet')

    if ARGS.out == 'table':
        table.report(results)
    elif ARGS.out == 'influx':
        try:
            influx.report(results, ARGS.dbhost, ARGS.dbuser, ARGS.dbpasswd)
        except AttributeError as e:
            print("Output to influx reuqires a database host and password\n", e)
            exit(1)


def monitor_resources(arguments):
    # manages information flow for resources monitoring
    available_hosts, time = p1.list_resources()
    condor_hosts = condor.list_resources(
        arguments.pool)
    panda_hosts = panda.list_resources()

    return correlate(available_hosts, condor_hosts, panda_hosts)


if __name__ == "__main__":
    main()
