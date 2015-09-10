#!/bin/bash
# George Nicol
# Check to see if a port on the list is tied to the service indicated and report discrepancies.
# Expects 3 files, the generated csv list of ports and services, the socket list, and the original ports.

if [[ $# -ne 3 ]]; then
  echo "usage: $0 file.csv rmsock.txt host.txt"
  exit
fi


IFS=$'\n'
inputFile=$1
rmsockFile=$2
hostFile=$3
flag=0

while read line; do

  port=`echo $line | awk -F',' '{print$3}'`
  srvc=`echo $line | awk -F',' '{print$4}'`

  portResults=( $(grep ."$port" $hostFile) )
  if [[ ${#portResults[@]} -eq 0 ]]; then
    echo "port $port not found in host file $hostFile"
    flag=1
  fi

  srvcResults=( $(grep "$srvc" $rmsockFile) )
  if [[ $srvc == "" ]]; then
    echo "in $inputFile at port $port a blank entry for service was encountered"
    flag=1
  elif [[ ${#srvcResults[@]} -eq 0 ]]; then
    echo "srvc $srvc not found in rmsock file $rmsockFile at $port"
    flag=1
  fi

  if [[ $flag -eq 0 ]]; then  #so far so good otherwise bypass looking for something that doesn't exist
    for(( i=0; i<${#srvcResults[@]}; i++ )); do
      # does the memory bit found in the rmsock (corresponding to a service) match a port memory bit anywhere?
      memb=`echo ${srvcResults[i]} | awk -F":" '{print$1}'`
      if echo $srvcResults | grep -q $memb; then
        flag=1
        break
      fi
    done
  fi

  if [[ $flag -eq 0 ]]; then
     echo "NO MATCH BETWEEN PORT $port and SERVICE $srvc with $hostFile and $rmsockFile"
  fi

done < $inputFile
