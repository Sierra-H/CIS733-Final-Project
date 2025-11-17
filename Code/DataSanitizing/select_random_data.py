import sys
import os
import chardet
import random

def processFolder(idir,odir,n,target):
    # Source for tn :: https://pynative.com/python-count-number-of-files-in-a-directory/
    tn = len([x for x in os.listdir(idir) if os.path.isfile(os.path.join(idir,x))])
    print("Debug: TN == "+str(tn))
    sns = random.sample(range(1,tn),n)
    for x in sns:
        o = open(odir+target+str(x)+".txt","w")
        o.write(open(idir+target+str(x)+".txt","r").read())
        o.close()

if __name__ == '__main__':
    verbose = False
    if(len(sys.argv) != 5):
        print("Incorrect Syntax, Usage: python select_random_data.py number target path/to/folder path/to/outfolder")
        print("   Or: python margin.py help")
    else:
        idir = sys.argv[3]
        odir = sys.argv[4]
        n = int(sys.argv[1])
        t = sys.argv[2]
        if(not idir.endswith("/")):
            idir+="/"
        if(not odir.endswith("/")):
            odir+="/"
        processFolder(idir,odir,n,t)
