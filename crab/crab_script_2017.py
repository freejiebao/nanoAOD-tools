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

p=PostProcessor(".",inputFiles(),None,"%s/src/PhysicsTools/NanoAODTools/scripts/ssww_keep_and_drop_2017.txt",modules=[countHistogramsModule(),puWeight_2017(),PrefCorr(),sswwModule2017(),lepSF_2017()],provenance=True,justcount=False,noOut=False,fwkJobReport=True,outputbranchsel = "%s/src/PhysicsTools/NanoAODTools/scripts/ssww_output_branch_selection_2017.txt") %(os.environ['CMSSW_BASE'],os.environ['CMSSW_BASE'])
p.run()

print "DONE"
os.system("ls -lR")

