"""Get reports on the status of the hardware at P1 from webserver, e.g.

example input file is in examples/resources.txt

The same file sits on the webserver http://squid.cern.ch/resources.txt

Returns:
    list of hostnames of the resources that should be available to do work, e.g.
    ['vm-sp1-cn-00001', 'vm-sp1-cn-00002', ..., 'vm-sp1-cn-94042']
"""
def main():
    list_resources()

def list_resources():
    incDevNam = False # when true ignors, when false adds the vm-sp1-cn- prefix
    buff_file = "servers.txt" #intermidiate storage of list from web for farther processing
    url = "http://squid.cern.ch/resources.txt" #url at wich to find the file
    retrieve_File(url,buff_file) #copies the file in to a file saved at the location indicated by buff_file(a .txt file)
    list, epochTime = find_resources_and_date(buff_file) #farther processes the file at buff_file location
    return list, epochTime

def retrieve_File(url, toText):
    #gets the file from url -The location on the web- and saves it to toText -a user specified location- for
    #farther processing
    import urllib.request
    import shutil
    with urllib.request.urlopen(url) as response, open(toText, 'wb') as outFile:
        shutil.copyfileobj(response, outFile)

def find_resources_and_date(file_name):
    # 1. grab list from file or webserver
    # 2. drop everything that is no "prod simp1"
    # 3. take the remaining hostnames and turn them into a list of strings
    toKeep = []
    # opens the file from IT, Computer resources
    list = open(file_name, "r")
    #initiats contents with first line of file
    contents = list.readline()
    contents = list.readline() #gets the epoch time stamp from the second line of the file
    epochTime = contents.split(' ') # ----
    epochTime = epochTime[len(epochTime)-1] # -----
    epochTime = epochTime.strip("\n") #checks to see if the timestamp ends in a "\n", if so it deletes "\n"
    while contents[len(contents) - 1] == "\n":
        #to do, Check the lines
        contents = contents.strip("\n")
        prospect = contents.split(' ')
        if(len(prospect) >= 3):  #confirms that prospect is a relevant entry, to avoid index out of range errors when looking at a.g. empty lines

        #if "prod" in contents and "simp1" in contents:
            if prospect[1] == "prod" and prospect[2] == "simp1":
                #tests to see if line with len 0, sign of end of file
                toKeep.append(prospect[0][11:16])
        contents = list.readline()
        if len(contents) == 0:
            break
    #returns creatime(time the file was Generated) and toKeep, a list of all relevant servers
    return toKeep, epochTime
    #return ['stuff', 'more stuff']

if __name__ == "__main__":
    main()
