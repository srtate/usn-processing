# Ubuntu Security Notice (USN) processing scripts

The scripts in his repository are research scripts used for extracting
information from Ubuntu Security Notices (USNs), and cross-referencing
that with information from the Ubuntu CVE Tracker and NIST's National
Vulnerability Database (NVD). While the scirpts should be reliable,
this is not intended to be polished software -- it takes quite a bit
of manual intervention to run them.

### Prerequisites

To run this software, the following Ubuntu packages must be installed:

* `procmail` (for the `formail` program)
* `python3`
* `wget`
* `git`

### Instructions

The following are step-by-step instructions on how to create a CSV
file (with a tab as a separator) that combines information from the
various sources listed above. This can be loaded into any spreadsheet
program for further processing.

1. Edit `00-defs.inc` to specify the release version and codename.

2. Download USNs you are interested in as monthly email archives from
   [`https://lists.ubuntu.com/archives/ubuntu-security-announce/`](https://lists.ubuntu.com/archives/ubuntu-security-announce/)

3. Uncompress the archives

4. If you are only interested in part of any month, edit the archive to
   delete the messages you are not interested in. For example, if you
   are only interested USNs through June 14, 2020, then you could edit
   2020-June.txt, find the first message dated after June 14, and
   delete from there to the end of the file.

5. Run "`cat 20*.txt | ./01-extract-usns.sh`"
   This creates an "extract" directory that includes the USNs into
   individual files. Note that for our project we're not interested in
   kernel USNs, so we move those to a subdirectory to get them out of
   the way.

6. Run "`./02-get-nvddb.sh`" to download and process the full NVD
   database, leaving a file `nvddb/allcveinfo.csv` that is used by
   later processing.

7. Run "`./03-get-cves-prelim.sh`" to extract CVEs with source package
   info from the USNs. Restricts the list at a high level to the
   proper Ubuntu release, but individual CVEs might still not be
   relevant for this distribution -- that's why this is "prelim."

8. Get the Ubuntu CVE Tracker information using
   "`git clone https://git.launchpad.net/ubuntu-cve-tracker`"

9. Run "`./04-get-cves-from-tracker.sh`" to get the final CVE
   information, using info from the "prelim" list (for source package
   names), from the CVE-tracker (to get just the actual relevant
   CVEs), and the NVDDB (for severity scores and CWEs). The final
   information is left in the file `cveinfo-dist.csv`.  Various
   intermediate results are also left in files -- see the script
   source if you are interested.



