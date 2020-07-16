#!/usr/bin/python3

# Extract CWE info from NVD JSON-format downloads. Outputs a CSV file
# (using a semicolon for a column separator) in which the columns are:
#   CVE id; CVSSV3 score; CVSSV2 score; raw CWE list; bucketed CWE list

# The NVD JSON downloads are one year at a time, so you can get a complete
# list using a shell command like:
#    for f in nvdc*.json ; do ./nvdproc.py $f ; done >allcveinfo.csv

# NVD downloads are available at https://nvd.nist.gov/vuln/data-feeds

import json
import sys
import locale

if len(sys.argv) != 2:
   print("Must provide a single argument, the json filename", file=sys.stderr)
   sys.exit(1)

locale.setlocale(locale.LC_ALL, ('C', 'UTF-8') )

try:
   with open(sys.argv[1]) as f:
      data = json.load(f)
except:
   print("Invalid filename", file=sys.stderr)
   sys.exit(1)
   
cwetypetbl = {
   'CWE-1': 'CWE-1',
   'CWE-16': 'CWE-16',
   'CWE-17': 'CWE-17',
   'CWE-18': 'CWE-17',
   'CWE-19': 'CWE-19',
   'CWE-20': 'CWE-20',
   'CWE-21': 'CWE-21',
   'CWE-22': 'CWE-21',
   'CWE-59': 'CWE-21',
   'CWE-74': 'CWE-20',
   'CWE-77': 'CWE-20',
   'CWE-78': 'CWE-20',
   'CWE-79': 'CWE-20',
   'CWE-88': 'CWE-20',
   'CWE-89': 'CWE-20',
   'CWE-90': 'CWE-20',
   'CWE-91': 'CWE-20',
   'CWE-93': 'CWE-20',
   'CWE-94': 'CWE-20',
   'CWE-99': 'CWE-20',
   'CWE-113': 'CWE-20',
   'CWE-116': 'CWE-172',
   'CWE-118': 'CWE-119',
   'CWE-119': 'CWE-119',
   'CWE-122': 'CWE-119',
   'CWE-123': 'CWE-119',
   'CWE-125': 'CWE-119',
   'CWE-126': 'CWE-119',
   'CWE-129': 'CWE-119',
   'CWE-134': 'CWE-20',
   'CWE-171': 'CWE-171',
   'CWE-172': 'CWE-172',
   'CWE-184': 'CWE-693',
   'CWE-185': 'CWE-185',
   'CWE-189': 'CWE-189',
   'CWE-190': 'CWE-682',
   'CWE-191': 'CWE-682',
   'CWE-199': 'CWE-19',
   'CWE-200': 'CWE-668',
   'CWE-216': 'CWE-216',
   'CWE-254': 'CWE-254',
   'CWE-255': 'CWE-255',
   'CWE-264': 'CWE-264',
   'CWE-275': 'CWE-275',
   'CWE-284': 'CWE-264',
   'CWE-285': 'CWE-264',
   'CWE-287': 'CWE-264',
   'CWE-295': 'CWE-310',
   'CWE-297': 'CWE-310',
   'CWE-306': 'CWE-264',
   'CWE-310': 'CWE-310',
   'CWE-320': 'CWE-310',
   'CWE-326': 'CWE-310',
   'CWE-327': 'CWE-310',
   'CWE-330': 'CWE-330',
   'CWE-331': 'CWE-330',
   'CWE-332': 'CWE-330',
   'CWE-338': 'CWE-330',
   'CWE-339': 'CWE-330',
   'CWE-345': 'CWE-345',
   'CWE-346': 'CWE-264',
   'CWE-347': 'CWE-310',
   'CWE-352': 'CWE-442',
   'CWE-358': 'CWE-358',
   'CWE-361': 'CWE-361',
   'CWE-362': 'CWE-362',
   'CWE-369': 'CWE-682',
   'CWE-371': 'CWE-361',
   'CWE-384': 'CWE-264',
   'CWE-388': 'CWE-388',
   'CWE-398': 'CWE-17',
   'CWE-399': 'CWE-399',
   'CWE-400': 'CWE-400',
   'CWE-404': 'CWE-399',
   'CWE-405': 'CWE-664',
   'CWE-407': 'CWE-407',
   'CWE-415': 'CWE-465',
   'CWE-416': 'CWE-465',
   'CWE-417': 'CWE-417',
   'CWE-426': 'CWE-417',
   'CWE-427': 'CWE-417',
   'CWE-428': 'CWE-417',
   'CWE-434': 'CWE-669',
   'CWE-441': 'CWE-441',
   'CWE-442': 'CWE-442',
   'CWE-444': 'CWE-442',
   'CWE-452': 'CWE-452',
   'CWE-465': 'CWE-465',
   'CWE-471': 'CWE-471',
   'CWE-476': 'CWE-465',
   'CWE-485': 'CWE-485',
   'CWE-502': 'CWE-399',
   'CWE-532': 'CWE-538',
   'CWE-534': 'CWE-538',
   'CWE-538': 'CWE-538',
   'CWE-552': 'CWE-668',
   'CWE-601': 'CWE-442',
   'CWE-610': 'CWE-610',
   'CWE-611': 'CWE-610',
   'CWE-613': 'CWE-264',
   'CWE-640': 'CWE-264',
   'CWE-642': 'CWE-668',
   'CWE-664': 'CWE-664',
   'CWE-665': 'CWE-452',
   'CWE-668': 'CWE-668',
   'CWE-669': 'CWE-669',
   'CWE-682': 'CWE-682',
   'CWE-693': 'CWE-693',
   'CWE-703': 'CWE-703',
   'CWE-704': 'CWE-704',
   'CWE-707': 'CWE-171',
   'CWE-749': 'CWE-264',
   'CWE-754': 'CWE-703',
   'CWE-769': 'CWE-399',
   'CWE-774': 'CWE-400',
   'CWE-775': 'CWE-399',
   'CWE-787': 'CWE-119',
   'CWE-798': 'CWE-255',
   'CWE-824': 'CWE-465',
   'CWE-825': 'CWE-465',
   'CWE-834': 'CWE-834',
   'CWE-835': 'CWE-834',
   'CWE-913': 'CWE-399',
   'CWE-915': 'CWE-399',
   'CWE-918': 'CWE-441',
   'CWE-943': 'CWE-20',
   'NVD-CWE-Other': 'noclass',
   'NVD-CWE-noinfo': 'noclass',
   }
   
def cwetype(cwe):
   if cwe in cwetypetbl:
      return cwetypetbl[cwe]
   else:
      return "unknown"

for d in data["CVE_Items"]:
    os1=d["cve"]["CVE_data_meta"]["ID"]

    try:
        os2=d["impact"]["baseMetricV3"]["cvssV3"]["baseScore"]
    except:
        os2="None"

    try:
        os3=d["impact"]["baseMetricV2"]["cvssV2"]["baseScore"]
    except:
        os3="None"

    os4=""
    os5=""
    try:
        t = d["cve"]["problemtype"]["problemtype_data"]
        cwelist = [ y["value"] for tt in t for y in tt["description"] ]
        os4=','.join(cwelist)
        classset = set([ cwetype(x) for x in cwelist ])
        classset.discard('noclass')
        os5=','.join(classset)
    except:
        os4=""
        os5=""
        
    print(os1+"\t"+str(os2)+"\t"+str(os3)+"\t"+str(os4)+"\t"+str(os5))
    

