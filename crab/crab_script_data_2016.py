#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.modules.ssww.sswwModule_copy import *
from  PhysicsTools.NanoAODTools.postprocessing.examples.countHistogramsModule import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
#from  PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *

p=PostProcessor(".",inputFiles(),None,"ssww_keep_and_drop_2016.txt",modules=[countHistogramsModule(),PrefCorr(),sswwModule2016()],provenance=True,justcount=False,noOut=False,fwkJobReport=True,outputbranchsel = "ssww_output_branch_selection_2016.txt")
p.run()

print "DONE"
os.system("ls -lR")

