#!/bin/bash

red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`
bold=`tput bold`

# Pulling Reported Vulnerbilities from OpenBugBounty Community.
	read -p "$bold$green[+] - Please Provide filename: $reset" fname

	for domain in $(cat $fname); do 
	   echo "$bold$green[+] - Looking for Reports in OpenBugBounty for $domain$reset"
	   echo "   $bold$domain$reset" 
	   curl -s 'https://www.openbugbounty.org/search/?search=$domain' | grep $domain >> /tmp/raw_response.txt
	   sleep 3; 
	done

	grep -Eo "/reports/[[:digit:]]{1,9}/" /tmp/raw_response.txt|sed -e 's/^/https:\/\/openbugbounty.org/' |sed 's,.*,\x1B[31m&\x1B[0m,' >> OpenBugBounty_Reports.txt
	echo "$bold$green[+] - Results saved in OpenBugBounty_Reports.txt$reset"
