import json

def main():
    with open('../../examples/p1_data.json', 'r') as f:
        p1_data = json.load(f)
    with open('../../examples/condor_data.json', 'r') as f:
        condor_data = json.load(f)
    with open('../../examples/panda_data.json', 'r') as f:
        panda_data = json.load(f)
    output = correlate(p1_data, condor_data, panda_data)
    n = 0
    for i in output:
        if output[i]["InPanda"] == False or output[i]["InCondor"] == False:
            print(i, end="  ")
            print(output[i])
            n += 1
    print(n)

def correlate(p1, condor, panda):
    output = {}
    for i in p1:
        in_condor = False  #checks wether or not the machine is in the condor and panda resource lists
        in_panda = False
        if i in condor.keys():
            in_condor = True
        if i in panda.keys():
            in_panda = True
        if in_condor == True:
            output[i] = condor[i]  #if machine is found in condor, copies information to output dict
        else:
            output[i] = {"DetectedCpus":0, #if machine not found, information in output dict is set to 0
                         "DetectedMemory":0,
                         "ChildCpus":0,
                         "ChildMemory":0,
                         "TotalCondorLoadAvg":0.0,
                         "UsageCpus":0.0,
                         "UsageMemory":0.0,
                         "PerCpuLoad":0.0}
        if in_panda == True:
            output[i]["pctfail"] = panda[i] #pctfail from pand copied if present, else set to 0
        else:
            output[i]["pctfail"] = 0
        output[i]["InPanda"] = in_panda  #bools of in panda and in condor included for case differenciation
        output[i]["InCondor"] = in_condor
    return output

if __name__ == "__main__":
    main()
