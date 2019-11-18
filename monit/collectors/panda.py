"""Grab resource information from the ATLAS workload managemen system PanDA

The information on virtual machines that are connected to ATLAS workload
management can be found on:
    https://bigpanda.cern.ch/wns/CERN-P1_UCORE/?hours=1&json
"""
import json
import requests
import time


def get_data():
    params = {
        'nhours': '1',
        'json': 1}
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    while True:
        try:
            response = requests.get(
                'http://bigpanda.cern.ch/wns/CERN-P1_UCORE/',
                params=params,
                headers=headers)
            # This fails sometimes cause bigpanda is obtuse
        except requests.ConnectionError:
            # If it fails, try and try again
            print("BigPanDA query failed, retrying in 5 seconds")
            time.sleep(5)
            continue
        break
    data = json.loads(response.text)
    return data


def list_resources():
    #a function to find the relevant info, the machine name and the pctfail value, out of the data structure
    machines = {}
    data = get_data()
    for machine in data["summary"]:
        if "vm-sp1-cn-" in machine["name"]:
            machines[machine["name"][10:15]] = machine["pctfail"]
    return machines


def main():
    """Execute this module as script to ease testing and developing
    """
    #res = list_resources()
    #print(json.dumps(res, indent=2))
    out = list_resources()
    for n in out:
        print(n, end="  ")
        print(out[n])

if __name__ == "__main__":
    main()
