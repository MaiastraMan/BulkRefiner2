'''Sample script to demonstrate use of GSASIIscriptable to duplicate the
tutorial found here:
https://subversion.xray.aps.anl.gov/pyGSAS/Tutorials/CWCombined/Combined%20refinement.htm

This script is described in this tutorial: 
https://subversion.xray.aps.anl.gov/pyGSAS/Tutorials/PythonScript/Scripting.htm
'''

import os,sys, glob

#import GSASii_Mar_2021.GSASII.GSASII

sys.path.insert(0,'C:/GSASii_Mar_2021/GSASII')
import GSASIIscriptable as G2sc
import G2compare as G2comp
#import G2compare.loadFile  doesn't work
from G2compare import MakeTopWindow
import GSASII as G2
import GSASIIdataGUI as G2dG
import GSASIIIO as G2IO
from GSASIIIO import ProjFileOpen
import subprocess
#subprocess.call([r'C:\Users\Conrad Gillard\Documents\Programming\PythonGSASII\Matrix.bat']) # works


workdir = "C:/Users/Conrad Gillard/Documents/Programming/PythonGSASII/WorkFol"
datadir = "C:/Users/Conrad Gillard/Documents/Programming/PythonGSASII"

def HistStats(gpx):
    '''prints profile rfactors for all histograms'''
    print(u"*** profile Rwp, "+os.path.split(gpx.filename)[1])
    for hist in gpx.histograms():
        print("\t{:20s}: {:.2f}".format(hist.name,hist.get_wR()))
    print("")
    gpx.save()

# Load project with background already specified
gpx = G2sc.G2Project('EBTL31_BackgroundOnly.gpx')
# Immediately save project so that starting file is not modified by autosave on refinement
gpx.save('EBTL31_InitialSave.gpx')

# Step 1: Assign histogram to a variable, for future use in this program
hist1 = gpx.histogram(0)

# Step 2: Add phases and link  to the histogram
phase0 = gpx.add_phase(os.path.join(datadir,"Bi_EntryWithCollCode64703.cif"),
                      phasename="Bi",
                      histograms=[hist1])

phase1 = gpx.add_phase(os.path.join(datadir,"BiLi_EntryWithCollCode58796.cif"),
                      phasename="LiBi",
                      histograms=[hist1])

phase2 = gpx.add_phase(os.path.join(datadir,"Li2Te_EntryWithCollCode60434.cif"),
                      phasename="Li2Te",
                      histograms=[hist1])


#h.setHistEntryValue(['Sample Parameters', 'Type'], 'Bragg-Brentano')

# Increase number of cycles to improve convergence
gpx.data['Controls']['data']['max cyc'] = 8 # not in API

# Do Initial Refinement (keep background refining off)
refdict0 = {}
gpx.save('EBTL31_Phases.gpx')
gpx.do_refinements([refdict0])
HistStats(gpx)

# Refine Phase fractions (follow process in 15.4 of following page to do so: https://gsas-ii.readthedocs.io/en/latest/GSASIIscriptable.html#hap-parameters-table)
#phase0.setPhaseEntryValue(['PWDR EBTL31.xy', 'Scale'], [1.0, True])
#phase0.setPhaseEntryValue([hist1, 'Scale'], [1.0, True])
#print(phase0.getPhaseEntryList())

#print(hist1.getHistEntryList())
# Their example p.getHAPentryList(0,'Scale')


#gpx.add_EqnConstr(1.0,(phase0.scale,phase1.scale, phase2.scale))
#gpx.add_EqnConstr(1.0,(phase0.getHAPvalues('Scale'),phase1.getHAPvalues('Scale'), phase2.getHAPvalues('Scale')))
#gpx.add_EqnConstr(1.0,(phase0.getPhaseEntryValue(['Histograms', 'PWDR EBTL31.xy', 'Scale']),phase1.getPhaseEntryValue(['Histograms', 'PWDR EBTL31.xy', 'Scale']), phase2.getPhaseEntryValue(['Histograms', 'PWDR EBTL31.xy', 'Scale'])))
gpx.add_EqnConstr(1.0,('0:0:Scale', '1:0:Scale', '2:0:Scale'))

phase0.setPhaseEntryValue(['Histograms', 'PWDR EBTL31.xy', 'Scale'], [1.0, True])
phase1.setPhaseEntryValue(['Histograms', 'PWDR EBTL31.xy', 'Scale'], [1.0, True])
phase2.setPhaseEntryValue(['Histograms', 'PWDR EBTL31.xy', 'Scale'], [1.0, True])

#phase1
#phase2
# tutorial step 5: add unit cell refinement (Phase)
gpx.save('EBTL_Programmatic_Test.gpx')
refdict1 = {"set": {"Cell": True}} # set the cell flag (for all phases)
gpx.set_refinement(refdict1)
gpx.do_refinements([{}])
HistStats(gpx)

# tutorial step 6: add Dij terms (HAP) for histogram 1 only
gpx.save('step6.gpx')
refdict2 = {"set": {"HStrain": True}} # set HAP parameters
gpx.set_refinement(refdict2,phase=phase0,histogram=[hist1])
gpx.do_refinements([{}]) # refine after setting
HistStats(gpx)

# tutorial step 7: add size & strain broadening (HAP) for histogram 1 only 
gpx.save('step7.gpx')
refdict2 = {"set": {"Mustrain": {"type":"isotropic","refine":True},
                    "Size":{"type":"isotropic","refine":True},
                    }}
gpx.set_refinement(refdict2,phase=phase0,histogram=[hist1])
gpx.do_refinements([{}]) # refine after setting
HistStats(gpx)

# tutorial step 8: add sample parameters & set radius (Hist); refine atom parameters (phase)
gpx.save('step8.gpx')
hist1.set_refinements({'Sample Parameters': ['Shift']})
hist2.set_refinements({'Sample Parameters': ['DisplaceX', 'DisplaceY']})
hist2.data['Sample Parameters']['Gonio. radius'] = 650. # not in API
phase0.set_refinements({"Atoms":{"all":"XU"}})
gpx.do_refinements([{}]) # refine after setting
HistStats(gpx)

# tutorial step 9: change data limits & inst. parm refinements (Hist) 
gpx.save('step9.gpx')
hist1.set_refinements({'Limits': [16.,158.4]})
hist2.set_refinements({'Limits': [19.,153.]})
gpx.do_refinements([{"set": {'Instrument Parameters': ['U', 'V', 'W']}}])
HistStats(gpx)
