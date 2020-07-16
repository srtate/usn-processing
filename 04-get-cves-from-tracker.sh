#!/bin/bash

source 00-defs.inc

grep "^${relname}_" $cvetdir/active/CVE* $cvetdir/retired/CVE* | egrep -v ': (DNE|not-affected|ignored)' | sed -e "s,^.*/\\(CVE[^:]*\\):${relname}_\\([^:]*\\).*\$,\1," | sort -u >cves-for-dist.csv

join -t $'\t' cve-dist-prelim.csv cves-for-dist.csv >cve-dist-final.csv

join -t $'\t' -a 1 cve-dist-final.csv nvddb/allcveinfo.csv >cveinfo-dist.csv
