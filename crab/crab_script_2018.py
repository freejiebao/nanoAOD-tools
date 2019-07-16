#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.modules.ssww.sswwModule_copy import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer_ssww import *
from  PhysicsTools.NanoAODTools.postprocessing.examples.countHistogramsModule import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
# from  PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *

p=PostProcessor(".",inputFiles(),None,"ssww_keep_and_drop_2018.txt",modules=[countHistogramsModule(),puWeight_2018(),PrefCorr(),sswwModule2018(),lepSF_2018()],provenance=True,justcount=False,noOut=False,fwkJobReport=True,outputbranchsel = "ssww_output_branch_selection_2018.txt")
p.run()

print "DONE"
os.system("ls -lR")

