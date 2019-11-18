"""Send gathered data to influx database
"""
from influxdb import InfluxDBClient
from time import gmtime, strftime

def format_data(key, value, t):
    value['host'] = key
    event = {
        "measurement": "resources",
        "tags": { 
            'InPanda': str(value.pop('InPanda')),
            'InCondor': str(value.pop('InCondor'))
            },
        "time": t,
        "fields": value
        }
    return event

def report(data, host, user, passwd, port=8081, dbname='test'):
    t = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    events = [format_data(k, v, t) for k, v in data.items()]
    client = InfluxDBClient(host=host, port=port, username=user, password=passwd, database=dbname, ssl=True, verify_ssl=False)
    client.write_points(events)
