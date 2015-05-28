#!/bin/bash
# George Nicol
# 5/27/2015
#
# For NERC CIP CVAs some clients will supply us with nmap scans as their "assessment" for ports and services
# This script will take an nmap scan text file of the following format:
#
#Nmap 6.47 scan initiated Tue May 19 07:09:05 2015 as: nmap -v -n -T4 --version-light -p 1-65535 -oA xxx.xxx.xx.x_TCP xxx.xxx.xx.x
#Nmap scan report for xxx.xxx.xx.x
#Host is up (0.0010s latency).
#Not shown: 65517 closed ports
#PORT      STATE SERVICE
#21/tcp    open  ftp
#23/tcp    open  telnet
#102/tcp   open  iso-tsap
#
# and convert it as follows:
#
# tcp,21,ftp,ip
# tcp,23,telnet,ip
# tcp,102,iso-tsap,ip
#
# Which is the expected format in our current suite of tools.
# Notice that expectation is: PROTOCOL,PORT,SERVICE,IP_ADDRESS
# We also expect that each of the file names contains the ip address

usage()
{
  echo "${0} path/to/nmap_result"
}


if [[ $# -ne 1 ]]; then
  usage
  exit
fi

if ! [[ -e ${1} ]]; then
  usage
  exit
fi
ipAddress=''
fileName=${1}
echo $fileName

# trim both sides of the filename
# grab things that are numbers
# strip out the white space and the trailing period
# you should be left with a valid ip address. There is always some crazy bastard who may do something like
# my.file.123.22.12.4.2nd.version in which case you have to use the grey matter in between your ears

fileName=`echo $fileName | sed  's/^[^0-9]*//' | sed 's/[^0-9]*$//'`
ipAddress+=`echo $fileName | awk -F "." '{ for (i = 1; i <= NF; i++){ if ( $i<256 && $i>=0) {print $i"."} } }'`
ipAddress=`echo $ipAddress | sed 's/\.$//' | sed 's/\ //g'`

echo $ipAddress

while read line; do
  port=`echo $line | awk '{print $1}' | sed 's/\/.*$//'`
  #before processing more data, ensure we have input we care about
  if [[ $port =~ [0-9]+ ]]; then
    protocol=`echo $line | awk '{print $1}' | sed 's/^.*\///'`
#    service=`echo $line | cut -d' ' -f 3-`        # print everything else on the line as the service
   service=`echo $line | awk '{print $3}'`
    echo "$protocol,$port,$service,$ipAddress"
  fi

done<$1



