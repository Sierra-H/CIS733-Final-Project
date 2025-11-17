import sys
import os
import chardet


def processEmail(fdir,odir,i):
    #name = "ling"
    #target = "Subject:"
    name = sys.argv[1]
    target = sys.argv[2]
    print("PE("+fdir+") "+str(i))
    with open(fdir, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encode = (result['encoding'])
    f = open(fdir,"r",encoding = encode)
    o = open(odir+name+"_"+str(i)+".txt","w")
    reading = True
    skipNext = False
    for l in f:
        if(skipNext):
            skipNext = False
        else:
            if(l.startswith(target) and reading):
                skipNext = True
                reading = False
            elif(not reading):
                o.write(l)
    if(reading):
        o.write(open(fdir,"r").read())
    o.close()
    f.close()

def processFolder(idir,odir,i,t):
    print("PF("+idir+")")
    for loc in os.listdir(idir):
        loc = idir + loc
        if loc.endswith(t):
            i = i + 1
            processEmail(loc,odir,i)
        else:
            if (not loc.endswith("/")):
                loc = loc + "/"
            i = processFolder(loc,odir,i,t)
    return i

if __name__ == '__main__':
    verbose = False
    if(len(sys.argv) != 3):
        print("Incorrect Syntax, Usage: python name target fileExtension enron_remove_metadata.py path/to/folder path/to/outfolder")
        print("   Or: python margin.py help")
    else:
        #name = sys.argv[1]
        #target = sys.argv[2]
        fileExt = sys.argv[3]
        idir = sys.argv[4]
        odir = sys.argv[5]

        if(not idir.endswith("/")):
            idir+="/"
        if(not odir.endswith("/")):
            odir+="/"
        processFolder(idir,odir,0,fileExt)
