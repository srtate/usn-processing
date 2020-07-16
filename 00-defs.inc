
# relvers is the numeric release number -- it is used as a regex, so the
# dot must be escaped (as below)

relvers='20\.04'

# relname is the code name of the release (bionic, focal, etc.)

relname='focal'

# cvetdir is the directory where the Ubuntu CVE tracker is loaded
# If you do "git clone https://git.launchpad.net/ubuntu-cve-tracker"
# it will create a subdirectory here named "ubuntu-cve-tracker" and
# the default will work.

cvetdir=ubuntu-cve-tracker

# Don't change this -- needs to be basic and predictable so sort/join
# work correctly

export LC_ALL=C

