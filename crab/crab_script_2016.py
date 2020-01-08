#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.modules.ssww.sswwModule_copy import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.ssww.helper_ssww import *
#from  PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer_ssww import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr_ssww import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer_ssww import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties_ssww import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer_ssww import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2_ssww import *  ##new way of using jme uncertainty

jmeCorrections = createJMECorrector(True, "2016", "B", "Total", True, "AK4PFchs", False)

#p=PostProcessor(".",inputFiles(),None,os.environ['CMSSW_BASE']+"/python/PhysicsTools/NanoAODTools/postprocessing/scripts/ssww_keep_and_drop_2016.txt",modules=[countHistogramsModule(),PrefCorr_2016(),sswwModule2016(),muonScaleRes2016(),puWeight_2016(),jmeCorrections(),btagSF2016(),lepSF_2016()],provenance=True,justcount=False,noOut=False,fwkJobReport=True,outputbranchsel = os.environ['CMSSW_BASE']+"/python/PhysicsTools/NanoAODTools/postprocessing/scripts/ssww_output_branch_selection_2016.txt")
p=PostProcessor(".",inputFiles(),None,os.environ['CMSSW_BASE']+"/python/PhysicsTools/NanoAODTools/postprocessing/scripts/ssww_keep_and_drop_2016.txt",modules=[countHistogramsModule(),puWeight_2016(),PrefCorr_2016(),jmeCorrections(),sswwModule2016(),muonScaleRes2016(),btagSF2016()],provenance=True,justcount=False,noOut=False,fwkJobReport=True,outputbranchsel = os.environ['CMSSW_BASE']+"/python/PhysicsTools/NanoAODTools/postprocessing/scripts/ssww_output_branch_selection_2016.txt")
p.run()

print "DONE"
os.system("ls -lR")

