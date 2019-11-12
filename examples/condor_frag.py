#!/usr/bin/env python
import argparse
import yaml
import requests
import htcondor
from functools import reduce


def utilization(m):
    # utilization of a machine is how many of the cpus are assigned work
    # or how much memory is assigned to work, whichever is greater.
    cpu_utilization = float(sum(m["ChildCpus"])) / float(m["DetectedCpus"])
    mem_utilization = float(sum(m["ChildMemory"])) / float(m["DetectedMemory"])
    return max(cpu_utilization, mem_utilization)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
            Collect HTCondor information and send this data to the
            Sim@P1 monitoring database.
            """)
    parser.add_argument('--influx', default='influx.yaml',
                        help='ini style influx file setting this script')
    args = parser.parse_args()

    try:
        with open(args.influx, 'r') as influx_file:
            influx = yaml.load(influx_file)
    except Exception:
        print('Could not read configuration')
        raise

    projection = ['Machine', 'DetectedCpus', 'DetectedMemory', 'ChildCpus',
                  'ChildMemory']
    constraint = 'regexp("vm-sp1-cn-[0-9]*.cern.ch",Machine)&&'
    constraint += 'PartitionableSlot==True'
    coll = htcondor.Collector('sp1-dev.cern.ch:20618')
    ads = coll.query(htcondor.AdTypes.Startd,
                     constraint=constraint,
                     projection=projection)

    # Rephrase ClassAd as a list of dictionaries
    data = [{key: ad[key] for key in ad if key in projection} for ad in ads]

    # Map to dict with Machine as key and utilization as value
    data = {d['Machine']: utilization(d) for d in data}
    data = ["condor,host={} utilization={}\n".format(u, data[u]) for u in data]
    data = reduce(lambda x, y: x+y, data)

    # https://dbod-adcccmon.cern.ch:8081/write?db=mydb
    response = requests.post(
        "https://{0}:{1}/write".format(influx['host'],
                                       influx['port']),
        params={
            'db': influx['database'],
            'u': influx['user'],
            'p': influx['password']},
        data=data,
        verify=False)
