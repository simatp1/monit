import json



def main():
    with open('condor_data.json', 'r') as f:
        condor_data = json.load(f)
    calc(condor_data)
    print(json.dumps(condor_data, indent = 2))


def calc(condor_data):
    for i in condor_data:
        detCPU = condor_data[i]["DetectedCpus"]
        DetectedMemory = condor_data[i]["DetectedMemory"]
        CCPU = sum(condor_data[i]["ChildCpus"])
        CMemory = sum(condor_data[i]["ChildMemory"])

        condor_data[i]["UsageCpus"] = float(float(CCPU) / float(detCPU))
        condor_data[i]["UsageMemory"]= float(float(CMemory) / float(DetectedMemory))
        condor_data[i]["ChildCpus"] = CCPU
        condor_data[i]["ChildMemory"] = CMemory
        condor_data[i]["Utilization"] = max(condor_data[i]["UsageCpus"] , condor_data[i]["UsageMemory"])
        condor_data[i]["PerCPULoad"] = float(float(condor_data[i]["TotalCondorLoadAvg"]) / float(detCPU))


    return(condor_data)





if __name__ == "__main__":
    main()
