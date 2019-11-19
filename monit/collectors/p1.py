"""Get reports on the status of the hardware at P1 from webserver, e.g.

example input file is in examples/resources.txt
The same file sits on the webserver http://squid.cern.ch/resources.txt

Returns:
    list of hostnames of the resources that should be available to do work, e.g.
    ['vm-sp1-cn-00001', 'vm-sp1-cn-00002', ..., 'vm-sp1-cn-94042']
"""
import urllib.request
import requests


def main():
    l, epochTime = list_resources()
    print(epochTime)
    for i in range(len(l)):
        print(l[i])


def list_resources():
    incDevNam = True # when true ignors, when false adds the vm-sp1-cn- prefix
    url = "https://pc-atlas-www.cern.ch/sp1/TPU_status.txt" #url at wich to find the file
    info = retrieve_File(url) #passes the list to find_resources_and_date in info variable
    list, epochTime = find_resources_and_date(info, incDevNam) #farther processes the file at buff_file location
    return list, epochTime


def retrieve_File(url):
    # gets the file from url -The location on the web- and saves it to toText
    # -a user specified location for farther processing
    proxies = {
        'http': 'http://atlasgw.cern.ch:3128',
        'https': 'https://atlasgw.cern.ch:3128'}
    capath = '/etc/grid-security/certificates'
    r = requests.get(url, proxies=proxies, verify=capath)
    return r.text


def find_resources_and_date(info, incDevNam):
    # 1. grab list from file or webserver
    # 2. drop everything that is no "prod simp1"
    # 3. take the remaining hostnames and turn them into a list of strings
    toKeep = []
    epochTime = 0
    # initiats contents with first line of file
    contents = info.split('\n')
    i = 0
    while contents[i][0] == "#":
        if "time:" in contents[i]:
            epochTime = contents[i].split(' ')
            epochTime = epochTime[len(epochTime)-1]
            epochTime = epochTime.strip('\n')
        i += 1

    while i < len(contents):
        #to do, Check the lines
        prospect = contents[i].split(' ')
        if(len(prospect) >= 3):  #confirms that prospect is a relevant entry, to avoid index out of range errors when looking at a.g. empty lines

        #if "prod" in contents and "simp1" in contents:
            if prospect[1] == "prod" and prospect[2] == "simp1":
                #tests to see if line with len 0, sign of end of file
                if incDevNam == False:
                    toKeep.append(prospect[0][11:16])
                elif incDevNam == True:
                    toKeep.append("vm-sp1-cn-"+prospect[0][11:16])
        i += 1
    toKeep = ["vm-sp1-cn-"+i for i in toKeep]
    #returns creatime(time the file was Generated) and toKeep, a list of all relevant servers
    return toKeep, epochTime
    #return ['stuff', 'more stuff']

if __name__ == "__main__":
    main()
