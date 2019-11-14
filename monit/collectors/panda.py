"""Grab resource information from the ATLAS workload managemen system PanDA

The information on virtual machines that are connected to ATLAS workload
management can be found on:
    https://bigpanda.cern.ch/wns/CERN-P1_UCORE/?hours=1&json
"""
import json
import requests
import time


def list_resources():
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


def main():
    """Execute this module as script to ease testing and developing
    """
    res = list_resources()
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
