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
        'hours': '48',
        'json': 1}
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    while True:
        try:
            response = requests.get(
                'http://bigpanda.cern.ch/wns/CERN-P1/',
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
    """find the relevant inforomation for systems in PanDA
    Returns dictionary with:
       machine name:
       - pctfail: int[0-100]
       - outlier: str[HighFail,LowFinished,etc]
    """
    machines = {}
    data = get_data()
    for machine in data["summary"]:
        if "vm-sp1-cn-" in machine["name"]:
            i = str(machine["name"]).strip()
            if i.endswith('.cern.ch'):
                i = i[:-8]
            machines[i] = {}
            machines[i]["pctfail"] = machine["pctfail"]
            outlier = str(machine["outlier"]).strip()
            if outlier == "":
                outlier = "False"
            machines[i]["outlier"] = outlier
    return machines


def main():
    """Execute this module as script to ease testing and developing
    """
    out = list_resources()
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
