#!/bin/bash

# This extracts individual USN messages from monthly digests, and separates
# out those that are for kernel issues.

# Prerequisites:

# 1. Must get security notices first -- monthly archives are available at
#    https://lists.ubuntu.com/archives/ubuntu-security-announce/

# 2. Must have "formail" installed (Ubuntu package procmail)

# To use: Pipe all messages into this (e.g., cat 2018*.txt | ./01-extract.sh )

# Note: You should not have anything named "extract" or "tmp" in this directory
# when you run this command, because they'll get destroyed!

rm -rf extract tmp
mkdir extract tmp

cat - >tmp/cmd.sh <<EOF
#!/bin/bash

cat - >extract/msg.\$FILENO
EOF

chmod a+x tmp/cmd.sh

formail -s tmp/cmd.sh

rm -rf tmp

# Next: Move USNs about the kernel to a subdirectory to separate them

mkdir extract/kernel

if grep -q '^  linux-image' extract/msg.* ; then
  mv `grep -l '^  linux-image' extract/msg.*` extract/kernel
fi

# Some don't list the linux-image package for some reason...

if grep -q 'linux: Linux kernel' extract/msg.* ; then
  mv `grep -l 'linux: Linux kernel' extract/msg.*` extract/kernel
fi



