#!/usr/bin/env python3
import argparse
import json
import requests
import yaml
from functools import reduce
import time



def format_panda_summary_for_influx( summary ):
    """summary is a list of dictionaries looking like this:
     {
      "comment": "no active blacklisting rules defined",
      "atlas_site": "CERN-P1",
      "closed": 0,
      "cloud": "CERN",
      "status": "online",
      "cancelled": 0,
      "corecount": 1,
      "merging": 0,
      "failed": 0,
      "holding": 0,
      "waiting": 0,
      "throttled": 0,
      "transferring": 1,
      "assigned": 0,
      "defined": 0,
      "finished": 0,
      "computingsite": "CERN-P1", <- aka PanDA qeue
      "mcp_cloud": "CERN, WORLD",
      "starting": 1,
      "running": 0,
      "activated": 6,
      "sent": 0,
      "pending": 0
    }, ... ]

    This formats into something like:

    panda,queue=CERN-P1 jobs.assigned=summary["assigned"]
    panda,queue=CERN-P1 jobs.finished=summary["finished"]
    panda,queue=CERN-P1_DYNAMIC_SCORE jobs.running=summary["running"]
    """
    result = ""
    job_states = ["closed", "cancelled", "merging", "failed", "holding", "waiting",
        "throttled", "transferring", "assigned", "defined", "finished", "starting",
        "running", "activated", "sent", "pending"]
    for queue in summary:
        strings = ["panda,queue={0} jobs.{1}={2}\n".format(queue['computingsite'], state, queue[state]) for state in job_states]
        result += reduce(lambda x, y: x+y, strings)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = """
        Collect PanDA information in Sim@P1 from the CERN-P1 site table. Send this data to the
        Sim@P1 monitoring database.
        """)
    parser.add_argument('--config', default='bigpanda.yaml', help='ini style config file setting this script')
    args = parser.parse_args()

    try:
        with open(args.config, 'r') as config_file:
            config = yaml.load(config_file)
    except Exception:
        print('Could not read configuration')
        raise

    #print(json.dumps(config, indent=2))

    # Ask BigPanDA What's Up, e.g.
    # curl -v -H 'Accept: application/json' -H 'Content-Type: application/json' "http://bigpanda.cern.ch/status_summary/?computingsite=CERN-P1&nhours=2&json=1"
    params = {
        'computingsite': config['panda']['site'],
        'nhours': config['panda']['nhours'],
        'json': 1 } # <-- json slug lets you get by SSO
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    while True:
        try:
            # This fails sometimes cause bigpanda is obtuse
            response = requests.get(config['panda']['host'], params=params,  headers=headers)
        except ConnectionError:
            # If it fails, retry
            print("BigPanDA query failed, retrying in 5 seconds")
            time.sleep(5)
            continue
        break
    data = json.loads(response.text)['data']



    #print(json.dumps(data, indent=2))

    data = format_panda_summary_for_influx(data)
    #print(data)
    #https://dbod-adcccmon.cern.ch:8081/write?db=mydb
    response = requests.post("https://{0}:{1}/write".format(config['influx']['host'], config['influx']['port']),
                             params = {'db': config['influx']['database'],
                                       'u': config['influx']['user'],
                                       'p': config['influx']['password']},
                             data = data,
                             verify=False)
    print(response.text)
