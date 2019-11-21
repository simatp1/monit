"""Send gathered data to influx database
"""
import requests


def format_data(key, value):
    """Format dictionary data into InfluxDB string for upload
    """
    value['host'] = key
    event = (
        "{measurement},InPanda={InPanda},InCondor={InCondor},Host={Host},"
        "Outlier={Outlier} "
        "Machine={Host},"
        "DetectedCpus={DetectedCpus},"
        "DetectedMemory={DetectedMemory},"
        "ChildCpus={ChildCpus},"
        "ChildMemory={ChildMemory},"
        "TotalCondorLoadAvg={TotalCondorLoadAvg},"
        "PctFail={PctFail},"
        "UsageCpus={UsageCpus},"
        "UsageMemory={UsageMemory},"
        "Utilization={Utilization},"
        "PerCpuLoad={PerCpuLoad}").format(
            measurement='resources',
            Host=str(key),
            InPanda=str(value['InPanda']),
            InCondor=str(value['InCondor']),
            Outlier=str(value['outlier']),
            DetectedCpus=int(value['DetectedCpus']),
            DetectedMemory=float(value['DetectedMemory']),
            ChildCpus=int(value['ChildCpus']),
            ChildMemory=float(value['ChildMemory']),
            TotalCondorLoadAvg=float(value['TotalCondorLoadAvg']),
            PctFail=int(value['pctfail']),
            UsageCpus=float(value['UsageCpus']),
            UsageMemory=float(value['UsageMemory']),
            Utilization=float(value['Utilization']),
            PerCpuLoad=float(value['PerCpuLoad']))
    return event


def report(data, host, user, passwd, port=8081, dbname='test'):
    """Report information gathered about Sim@P1 to InfluxDB
    """
    events = [format_data(k, v) for k, v in data.items()]
    for event in events:
        requests.post(
            "https://{host}:{port}/write".format(
                host=host,
                port=port),
            params={
                'db': dbname,
                'u': user,
                'p': passwd},
            data=event,
            verify=False)
