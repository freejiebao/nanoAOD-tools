#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.modules.ssww.sswwModule_copy import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer_ssww import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer_ssww import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties_ssww import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer_ssww import *

p=PostProcessor(".",inputFiles(),None,os.environ['CMSSW_BASE']+"/python/PhysicsTools/NanoAODTools/postprocessing/scripts/ssww_keep_and_drop_2017.txt",modules=[countHistogramsModule(),PrefCorr_2017(),sswwModule2017(),muonScaleRes2017(),puWeight_2017(),jetmetUncertainties2017(),btagSF2017(),lepSF_2017()],provenance=True,justcount=False,noOut=False,fwkJobReport=True,outputbranchsel = os.environ['CMSSW_BASE']+"/python/PhysicsTools/NanoAODTools/postprocessing/scripts/ssww_output_branch_selection_2017.txt")
p.run()

print "DONE"
os.system("ls -lR")

