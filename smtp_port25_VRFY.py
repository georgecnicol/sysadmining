#!/usr/bin/env python3
# George Nicol
# use with xargs for best results
# checks to see if VRFY accepted on port 25.
# That feature will allow brute force enumeration of users
# Best used with xargs and multithread.

import socket
import sys, re

def usage():
  print("Usage: {0} <ip> <username>".format(sys.argv[0]))
  sys.exit(0)


if len(sys.argv) != 2:
  usage()

ipAddress=sys.argv[1]

pattern=re.compile("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}")
pattern2=re.compile("200*")
pattern3=re.compile("550*")
if not pattern.match(ipAddress):
  usage()
try:
  s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket
  s.settimeout(3)                             # 3 seconds timeout
  connect=s.connect((ipAddress,25))           # connect to port 25 of the IP
  banner=s.recv(1024)                         # receive the banner
  s.send(bytes('VRFY foo \r\n', 'UTF-8'))     # verify that a user exists
  result=s.recv(1024)
  if pattern2.match(result.decode("utf-8")) or pattern3.match(result.decode("utf-8")):
    print(ipAddress)
  s.close()
except socket.error as e:
  #print("error")
  s.close()

