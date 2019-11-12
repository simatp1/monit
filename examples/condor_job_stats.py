#!/usr/bin/env python
import argparse
import htcondor
# import requests
import yaml


def status_name(status):
    status_name = ['idle', 'running', 'unknown', 'completed', 'held']
    return status_name[status - 1]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
            Collect HTCondor Job Information and publish it to InfluxDB
            """)
    parser.add_argument('--influx', default='influx.yaml',
                        help='yaml describing how to connect to influx')

    args = parser.parse_args()

    try:
        with open(args.influx, 'r') as influx_file:
            influx = yaml.load(influx_file)
    except Exception:
        print('Could not load influxuration')
        raise

    # JobStatus 1: idle, 2: running, 3: , 4: complete, 5: held
    job_status = [1, 2, 4, 5]
    schedds = {schedd_ad['Name']: htcondor.Schedd(schedd_ad)
               for schedd_ad in
               htcondor.Collector('sp1-dev.cern.ch:20618').locateAll(htcondor.DaemonTypes.Schedd)}
    lines = []
    for name, sched in schedds.iteritems():
        for status in job_status:
            lines += [
                'condor jobs.{}.{}={}\n'.format(
                    name[:15],
                    status_name(status),
                    sum(1 for _ in sched.xquery(requirements='JobStatus=={}'.format(status), projection=['ClusterID'])))]
    data = reduce(lambda x, y: x + y, lines)
    # response = requests.post(
    #                 "https://{0}:{1}/write".format(influx['host'],
    #                                                influx['port']),
    #                 params={
    #                     'db': influx['database'],
    #                     'u': influx['user'],
    #                     'p': influx['password']},
    #                 data=data,
    #                 verify='/etc/grid-security/certificates/')
