#!/usr/bin/env python
"""Get information on resources in our batch system

Returns:
    List if dictionaries. The dictionaries contain the hostname and stats about
    the host
"""
from htcondor import Collector, AdTypes
import json

def list_resources(pool="sp1-dev.cern.ch:20618"):
    projection = [
        'Machine',
        'DetectedCpus',
        'DetectedMemory',
        'ChildCpus',
        'ChildMemory',
        'TotalCondorLoadAvg']
    constraint = (
        'regexp("vm-sp1-cn-[0-9]*.cern.ch",Machine)&&'
        'PartitionableSlot==True')
    coll = Collector(pool)
    ads = coll.query(AdTypes.Startd,
                     constraint=constraint,
                     projection=projection)

    # Rephrase ClassAd as a list of dictionaries
    data = [{key: ad[key] for key in ad if key in projection} for ad in ads]
    return makeDict(data)

def makeDict(data):
    data_dict = {}
    for i in range(len(data)-1):
        data_dict[data[i]["Machine"][10:15]] = data[i]
    for i in data_dict:
        data_dict[i].pop('Machine')
    return data_dict

def main():
    #print(json.dumps(list_resources(), indent=2))
    data = makeDict()
    for i in data:
        print(i, end=":  ")
        print(data[i])

if __name__ == '__main__':
    main()
