#!/usr/bin/python
# piratezpdx - George Nicol - 12/24/2014
# Computer Action Team
# Checking to see if the backup was completed. We want to see if disklist contents
# were indeed backed up by checking the logs (amflush and/ or amdump).
# Specifically:
# Looks for the occurence of (every line in file1 && "finished-cmd") within file2.
# Any failure of that condition writes the failed line into an outputfile.



import sys

argc=len(sys.argv)
backedup="finished-cmd"

# ----- Function -------------------------------------------
# error message/ instructions
#-----------------------------------------------------------
def usage():
    print("use: {0} fileOfPathsToCheck fileOfDumpsCompleted".format(sys.argv[0]))
    print("example: {0} disklist logs/amdump.1".format(sys.argv[0]))


# ----- Function -------------------------------------------
# look for backed up path and successfully backed up in
# completed dumps file. return whether or not completed.
#-----------------------------------------------------------
def isFound(fqdn_path):
    try:
        f = open(sys.argv[2])
        for line in f:
            if backedup in line:
                if fqdn_path in line:
                    f.close()
                    return True
        f.close()
        return False

    except EnvironmentError as err:
        print(err)
        exit(0)


# ----- Function -------------------------------------------
# iterate through the paths in the file checking for their
# existence. If they don't, write them to the output file.
#-----------------------------------------------------------
def outerloop(writeout):
    try:
        for line in open(sys.argv[1]):
            searchTerms = line.split(" ")
            fqdnpath=searchTerms[0]+":"
            for part in searchTerms[2:-2]:
                if part !="":
                    fqdnpath+=part
            # above we sucked out a fqdn and path
            # if we don't find that thing was backed
            # up then we put the original line back
            # into the new disklist file.
            if not isFound(fqdnpath):
                writeout.write(line)

    except EnvironmentError as err:
        print(err)
        exit(0)


# ----- Function -------------------------------------------
#       M A I N
#-----------------------------------------------------------

try:
    if argc != 3:
        usage()
    else:
        fileOut = open("TheNewDisklist.TXT", "w") #, encoding="utf8")
        outerloop(fileOut)
        fileOut.close()
except EnvironmentError as err:
    print(err)
except ValueError:
    usage()



