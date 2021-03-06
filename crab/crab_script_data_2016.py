#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.modules.ssww.sswwModule_copy import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr_ssww import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer_ssww import *
#from  PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *

p=PostProcessor(".",inputFiles(),None,os.environ['CMSSW_BASE']+"/python/PhysicsTools/NanoAODTools/postprocessing/scripts/ssww_keep_and_drop_2016.txt",modules=[countHistogramsModule(),PrefCorr_2016(),sswwModule2016(),muonScaleRes2016()],jsonInput=os.environ['CMSSW_BASE']+'/python/PhysicsTools/NanoAODTools/postprocessing/scripts/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt',provenance=True,justcount=False,noOut=False,fwkJobReport=True,outputbranchsel = os.environ['CMSSW_BASE']+"/python/PhysicsTools/NanoAODTools/postprocessing/scripts/ssww_output_branch_selection_2016_data.txt")
p.run()

print "DONE"
