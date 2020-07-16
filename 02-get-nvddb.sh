#!/bin/bash

rm -rf nvddb
mkdir nvddb

cd nvddb

# This has "extra years" in it (2000, 2001, and after 2020) that don't
# exist while this is being written. This is to hopefully allow for some
# expansion -- they'll just quietly fail for now. To do better would
# require parsing the actual NVD data feed page, which seems far more
# work than it's worth...

for i in {2000..2023} ; do
    wget https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-$i.json.gz
done

echo
echo "Processing NVD files...."
echo

for f in nvdc*.json.gz ; do
    gunzip -c $f >tmp.json
    ../12-nvdproc.py tmp.json
    rm tmp.json
done | sort -u >allcveinfo.csv


