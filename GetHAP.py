from __future__ import division, print_function
import os,sys
sys.path.insert(0,'C:/GSASii_Mar_2021/GSASII')
import GSASIIscriptable as G2sc

#   # Get phase Differences (comment out if hist differences are sought)
# gpx = G2sc.G2Project("C:/Users/Conrad Gillard/Documents/Programming/PythonGSASII/WorkFol/EBTL_Programmatic_Test.gpx")
# h = gpx.phases()[0]
# with open('before.txt', 'w') as f:
#     for h in h.getHAPentryList():
#         f.write(str(h))
#
# gpx = G2sc.G2Project("C:/Users/Conrad Gillard/Documents/Programming/PythonGSASII/WorkFol/EBTL_Programmatic_Test_Const.gpx")
# h = gpx.phases()[0]
# with open('after.txt', 'w') as f:
#     for h in h.getHAPentryList():
#         f.write(str(h))
#

#   # Get hist Differences (comment out if phase differences are sought)
gpx = G2sc.G2Project("C:/Users/Conrad Gillard/Documents/Programming/PythonGSASII/WorkFol/EBTL_Programmatic_Test.gpx")
h = gpx.histograms()[0]
with open('before.txt', 'w') as f:
    for h in h.getHistEntryList():
        f.write(str(h))

gpx = G2sc.G2Project("C:/Users/Conrad Gillard/Documents/Programming/PythonGSASII/WorkFol/EBTL_Programmatic_Test_Const.gpx")
h = gpx.histograms()[0]
with open('after.txt', 'w') as f:
    for h in h.getHistEntryList():
        f.write(str(h))
