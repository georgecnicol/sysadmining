#!/usr/bin/env python3
# George Nicol

import re, sys, socket

#------------------------------------------------------
# I can haz instructions

def usage():
  print("usage: {0} <IP> <PORT>".format(sys.argv[0]))
  sys.exit(0)


#------------------------------------------------------
# checking args

if len(sys.argv) != 3:
  usage()

IP=sys.argv[1]
PORT=sys.argv[2]

#------------------------------------------------------
# minimal check for format, but garbage in -> garbage out
basicIP=re.compile("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}")
basicPort=re.compile("[0-9].*")

if not ( basicIP.match(IP) and basicPort.match(PORT) ):
  usuage()

#------------------------------------------------------
# fuzzer set up

inputString="A"
count=1
user=bytes('USER jiang\r\n', 'UTF-8')
quit=bytes('QUIT\r\n','UTF-8')
PORT=int(PORT)


#------------------------------------------------------
# main event

try:
  while count < 31:
    print("Fuzzing PASS with {0} bytes.".format(str(len(inputString))))
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(40)
    connect=s.connect((IP,PORT))
    s.recv(1024)
    s.send(user)
    s.recv(1024)
    s.send(bytes(inputString + '\r\n', 'UTF-8'))
    s.recv(1024)
    s.send(quit)
    s.close()
    inputString+=("A"*197)
    count+=1

  print("Completed, no luck. Try Harder")
except socket.error as e:
  print(e + "...socket error")
  sys.exit(0)

