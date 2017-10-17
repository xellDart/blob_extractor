# Script to automate generation of vendor blob makefiles
# for custom Android ROMs

from sys import argv
from os import walk, getcwd
from os.path import join
from datetime import date

header = """# Copyright (C) %i The CyanogenMod Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

PRODUCT_COPY_FILES += \\""" % date.today().year

blobnames = []
exemptions = []

try:
    android_mk = open("Android.mk", 'r')
except:
    android_mk = None
if android_mk is not None:
    for line in android_mk.readlines():
        if not line.startswith("LOCAL_SRC_FILES"): continue
        fname = line.split(" ")[-1][12:].rstrip()
        exemptions.append(fname)
    android_mk.close()

root = "proprietary"
freechars = len(root) + 1
for path, subdirs, files in walk(root):
    for name in files:
        blob = join(path, name)[freechars:]
        if blob.endswith(".jar") or blob.endswith(".apk"): continue
        if blob in exemptions: continue
        blobnames.append(blob)

blobnames.sort(key=str.lower)

devname = getcwd().split("/")[-1].split("_")[-1]

try:
    mfg = getcwd().split("/")[-1].split("_")[-2]
except IndexError:
    mfg = getcwd().split("/")[-2]

prefix1 = "vendor/" + mfg + "/" + devname + "/proprietary/"
prefix2 = "system/"

outfile = open(devname + "-vendor-blobs.mk", "w")

print(header, file=outfile)

for n, blob in enumerate(blobnames):
    ls = blob.strip()
    s1 = prefix1 + ls
    s2 = prefix2 + ls
    if n == len(blobnames) - 1:
        print("    %s:%s" % (s1, s2), file=outfile)
    else:
        print("    %s:%s \\" % (s1, s2), file=outfile)
