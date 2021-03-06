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
# from  PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *

p=PostProcessor(".",inputFiles(),None,os.environ['CMSSW_BASE']+"/python/PhysicsTools/NanoAODTools/postprocessing/scripts/ssww_keep_and_drop_2018.txt",modules=[countHistogramsModule(),sswwModule2018(),muonScaleRes2018()],provenance=True,justcount=False,noOut=False,fwkJobReport=True,jsonInput=os.environ['CMSSW_BASE']+'/python/PhysicsTools/NanoAODTools/postprocessing/scripts/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt',outputbranchsel = os.environ['CMSSW_BASE']+"/python/PhysicsTools/NanoAODTools/postprocessing/scripts/ssww_output_branch_selection_2018.txt")
p.run()

print "DONE"
os.system("ls -lR")

