#!/usr/bin/env python3
# George Nicol
# given an IP/ IP range and port, it checks to see if the port is open
# effective usage is something like: $> cat ips_available | xargs -n 1 -P 0 -I {} check_port.py -a {} -p 80
# which find all open port 80 in a hurry.

import socket
import argparse
import re, sys

class BadArgs(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

def usage():
  print("usage: {0} -a <ip address[-ending_quartet]> -p <port>".format(sys.argv[0]))
  sys.exit(1)

def connect(ipAddress,port,outputFile):
  try:
    mySock=socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket
    mySock.settimeout(3)
    connection=mySock.connect((ipAddress,port))
    print(ipAddress)
    mySock.close()
# if you want to write to an output file you can clean this up
#        fileOut=open("piratezPDX", "a")
#        fileOut.write(ipAddress + "\n")
#        fileOut.close()

  except socket.error as e:
    mySock.close()

#    if "timed out" in str(e):
#      pass
#    else:
#      print(e)
# you can filter on different errors if you don't want to fail silently.


parser = argparse.ArgumentParser(description="read in args, get ip addresses and ports")

parser.add_argument('-a', dest='address', action='store', nargs=1, required=True, help="ip or ip range as follows: 1.2.3.4-9")
parser.add_argument('-p', dest='port', action='store', nargs=1, required=True, help="port")
# note to self, using nargs makes list so you have args.item[0] additional args don't throw but are captured in unknown

args, unknown = parser.parse_known_args()
ipBase=''
ipStart=0
ipEnd=0

# parse dem args
try:
  if not (args.port[0]).isnumeric():
    raise BadArgs("not a valid port")
  if (int(args.port[0]) > 65535 or int(args.port[0]) < 0):
    raise BadArgs("not valid port")
  if not re.search("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",args.address[0]):
    raise BadArgs("not valid ip")
  if len(unknown):
    raise BadArgs("too many args provided")
  # if a range is provided, process the string accordingly, yeah this is messy and there is a better way to do it.
  if '-' in args.address[0]:
    args.address=args.address[0].split('-')
    temp=args.address[0].rsplit('.')
    ipBase=temp[0]+'.'+temp[1]+'.'+temp[2]+'.'
    ipStart=int(temp[3])
    ipEnd=int(args.address[1])
    if ipStart < 0 or ipStart > 255:
      raise BadArgs("not valid ip")
    if ipEnd < ipStart or ipEnd > 255:
      raise BadArgs("not valid range")

except BadArgs as e:
  print("{0}".format(e.value))
  usage()
except:
  usage()

outputFile=args.port[0]+".txt"

if ipStart == ipEnd:
  connect(args.address[0],int(args.port[0]),outputFile)
else:
  while ipStart <= ipEnd:
    ip=ipBase+str(ipStart)
    connect(ip,int(args.port[0]),outputFile)
    ipStart+=1


