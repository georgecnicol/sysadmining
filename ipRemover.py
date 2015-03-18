#!/usr/bin/python3
# George Nicol
# remove ips found in argv[1] from argv[2]
# argv[2]--> argv[2].old
# results of exclusion in argv[2]

# you should be able to exclude more than just ips with this, despite its name.

import sys
import shutil
import argparse


parser = argparse.ArgumentParser(description="read in args, get file names for incoming data")

parser.add_argument('-f', dest='path', action='store', default=list(), nargs=2, required=True,
    help="two paths to files containing data. Path 1 contains list of IPs to be excluded from path 2.")

args, unknown = parser.parse_known_args()

try:
  exclusions=open(args.path[0], 'r')
  masterList=open(args.path[1], 'r')
  fileOut=open('piratezPDX', 'w')

  exclusionList=exclusions.read()

  for address in masterList:
    if address not in exclusionList:
      fileOut.write(address)

  exclusions.close()
  masterList.close()
  fileOut.close()

  shutil.copy(args.path[1], args.path[1]+"old")
  shutil.move('piratezPDX', args.path[1])

except OSError as e:
  print(e)



