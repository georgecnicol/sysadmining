#!/bin/bash
# George Nicol
# As part of processing ports and services for CIP CVAs, I wrote this tool
# to assist on making CSV files from udp nmap results on the targets.

# important for arrays n things.
IFS=$(echo -en "\n\r")

usage()
{
  echo "usage $0 <input filename> <output file>"
  exit
}


if [[ $# -ne 2 ]]; then
  usage
fi

if ! [[ -e ${1} ]]; then
  usage
fi

# find all the IPs with ports open and put those IPs in an array.

validIPs=( $(grep -B2 "Not shown" "$1" | sort -u | sed 's/\-\-//' \
  | grep -v "Host is" | grep -v "Not shown" | awk  '{print $5}') )


# now go through the array, grab the ports and services, format them
# and write them into a file to be imported later. 7 lines was sufficient based on
# some preliminary scouting of the results.

for ((i=0; i<${#validIPs[@]}; i++)); do
  grep -A7 "report for ${validIPs[i]}$" "$2" | grep "/" \
    | sed 's/^/A\/B,udp,/g' | sed 's/\/udp open  /,/g' > "${validIPs[i]}".importme.csv

done



