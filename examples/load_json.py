import json


def correlate(p1, condor, panda):
    print(p1)
    print(condor)
    print(panda)


def main():
    with open('p1_data.json', 'r') as f:
        p1_data = json.load(f)
    with open('condor_data.json', 'r') as f:
        condor_data = json.load(f)
    with open('panda_data.json', 'r') as f:
        panda_data = json.load(f)
    correlate(p1_data, condor_data, panda_data)

if __name__ == "__main__":
    main()
