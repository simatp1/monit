hit1 = "prod" #
hit2 = "simp1"
output = open("/home/lars/Desktop/Output.txt", "w")
arrOutput = []

#with open("/home/lars/Desktop/TXT.txt", "r") as file:
def ReadTXT():

    with open("/home/lars/Desktop/TXT.txt") as input:
        linecount = 1
        for line in input:
            if hit1 in line and hit2 in line:
                line = str(line)
                output.write(line[11:16] + "\n")
                arrOutput.append(line[11:16])
            if linecount <  3:
                output.write(line)
                linecount = linecount + 1
        output.close()


ReadTXT()
print(arrOutput)
