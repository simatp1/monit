#!/usr/bin/env python
"""Get information on resources in our batch system

Returns:
    List if dictionaries. The dictionaries contain the hostname and stats about
    the host
"""
from htcondor import Collector, AdTypes


def list_resources():
    projection = [
        'Machine',
        'DetectedCpus',
        'DetectedMemory',
        'ChildCpus',
        'ChildMemory']
    constraint = (
        'regexp("vm-sp1-cn-[0-9]*.cern.ch",Machine)&&'
        'PartitionableSlot==True')
    coll = Collector('sp1-dev.cern.ch:20618')
    ads = coll.query(AdTypes.Startd,
                     constraint=constraint,
                     projection=projection)

    # Rephrase ClassAd as a list of dictionaries
    data = [{key: ad[key] for key in ad if key in projection} for ad in ads]
    return data


def main():
    print(list_resources())

if __name__ == '__main__':
    main()
