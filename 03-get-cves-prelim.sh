#!/bin/bash

source 00-defs.inc

# Run this to extract a preliminary list of CVEs and source packages that
# are affected for this particular distribution

# Leaves the list of CVEs and source packages in "cve-dist-prelim.csv"
# This file is tab-separated (between CVE ID and package list)

# Note that this processing is only at the USN granularity, and we discovered
# later that even if a USN says a distribution is affected, some of the
# individual CVEs may in fact NOT be relevant for this distribution. That's
# why this is a "preliminary" list, and can be refined/reduced later
# based on more specific information from the Ubuntu CVE tracker

declare -A cvepkgs

for i in extract/msg.* ; do
    if sed -n -e '/A security issue affects these/,/^Summary:/{p;}' $i | grep -q $relvers ; then
        clist=`sed -e 's/CVE-/\nCVE-/g' $i | grep '^CVE-' | sed -e 's/^\(CVE-[0-9][0-9][0-9][0-9]-[0-9A-Za-z]*\)[^0-9A-Za-z].*$/\1/'`

        plist=`grep 'launchpad.net/ubuntu/[+]source/' $i | sed -e 's/^.*\/[+]source\/\([^/]*\).*$/\1/' | tr '\n' ','`

	# Gather packages for each CVE - may be duplicates since a CVE could
	# be referenced in multiple USNs
	
	for c in $clist ; do
	    cvepkgs[$c]="${cvepkgs[$c]}${plist}"
	done
    fi
done

# Now go through and output one line per CVE, with list of source packages

for c in "${!cvepkgs[@]}" ; do
    plist=`echo -n ${cvepkgs[$c]} | tr ',' '\n' | sort -u | tr '\n' ','`
    echo -e "${c}\t${plist%,}"
done | sort -u >cve-dist-prelim.csv

