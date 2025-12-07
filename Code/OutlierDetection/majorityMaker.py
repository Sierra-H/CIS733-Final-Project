import numpy as np
import sys
import random

errorOutNumArgs = "Incorrect Number of Args.\nSyntax\npython majorityMaker.py inputFile legitMajorityOutFile phishingMajorityOutFile"
targetNumArgs = 4
minoritySize = 50

if(len(sys.argv) != targetNumArgs):
    print(errorOutNumArgs)
else:
    inputFile = open(sys.argv[1],"r")
    labels = inputFile.readline()
    legitOut = open(sys.argv[2],"w")
    legitOut.write(labels)
    phishingOut = open(sys.argv[3],"w")
    phishingOut.write(labels)

    line = inputFile.readline()
    legits = []
    phishings = []
    lines = []
    count = 0
    while line:
        lines.append(line)
        entries = line.split(",")
        print(entries[0]+" "+entries[1])
        if(entries[1]=="0"):#legit
            legits.append(count)
        elif(entries[1]=="1"):
            phishings.append(count)
        else:
            print("ERROR")
        line = inputFile.readline()
        count = count + 1
    inputFile.close()

    legitMinorityIndices = random.sample(legits,minoritySize)
    phishingMinorityIndices = random.sample(phishings,minoritySize)

    for m in phishingMinorityIndices:
        legitOut.write(lines[m])

    for m in legitMinorityIndices:
        phishingOut.write(lines[m])

    for x in legits:
        legitOut.write(lines[x])

    for x in phishings:
        phishingOut.write(lines[x])

    legitOut.close()
    phishingOut.close()

