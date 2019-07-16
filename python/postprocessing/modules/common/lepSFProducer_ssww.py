import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class lepSFProducer(Module):
    def __init__(self, year):
        if year=='2016':
            mu_f_tight= ["combine_SF_ID.root","combine_SF_ISO_tight.root"]
            mu_h_tight = ["pt_abseta_ratio", "pt_abseta_ratio"]
            mu_f_loose= ["combine_SF_ID.root","combine_SF_ISO_loose.root"]
            mu_h_loose = ["pt_abseta_ratio", "pt_abseta_ratio"]
            el_f_low = ["2016LegacyReReco_ElectronMVA80_Fall17V2.root","EGM2D_BtoH_low_RecoSF_Legacy2016.root"]
            el_h_low = ["EGamma_SF2D", "EGamma_SF2D"]
            el_f_high = ["2016LegacyReReco_ElectronMVA80_Fall17V2.root","EGM2D_BtoH_GT20GeV_RecoSF_Legacy2016.root"]
            el_h_high = ["EGamma_SF2D", "EGamma_SF2D"]

        elif year=='2017':
            mu_f_tight= ["RunBCDEF_SF_ID_syst.root","RunBCDEF_SF_ISO_syst_tight.root"]
            mu_h_tight = ["NUM_TightID_DEN_genTracks_pt_abseta", "NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta"]
            mu_f_loose= ["RunBCDEF_SF_ID_syst.root","RunBCDEF_SF_ISO_syst_loose.root"]
            mu_h_loose = ["NUM_TightID_DEN_genTracks_pt_abseta", "NUM_LooseRelIso_DEN_TightIDandIPCut_pt_abseta"]
            el_f_low = ["2017_ElectronTight.root","egammaEffi.txt_EGM2D_runBCDEF_passingRECO_lowEt.root"]
            el_h_low = ["EGamma_SF2D", "EGamma_SF2D"]
            el_f_high = ["2017_ElectronTight.root","egammaEffi.txt_EGM2D_runBCDEF_passingRECO.root"]
            el_h_high = ["EGamma_SF2D", "EGamma_SF2D"]

        elif year=='2018':
            mu_f_tight= ["RunABCD_SF_ID.root","RunABCD_SF_ISO_tight.root"]
            mu_h_tight = ["NUM_TightID_DEN_genTracks_pt_abseta", "NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta"]
            mu_f_loose= ["RunABCD_SF_ID.root","RunABCD_SF_ISO_loose.root"]
            mu_h_loose = ["NUM_TightID_DEN_genTracks_pt_abseta", "NUM_LooseRelIso_DEN_TightIDandIPCut_pt_abseta"]
            el_f_low = ["2018_ElectronMVA80.root","egammaEffi.txt_EGM2D_updatedAll.root"]
            el_h_low = ["EGamma_SF2D", "EGamma_SF2D"]
            el_f_high = ["2018_ElectronMVA80.root","egammaEffi.txt_EGM2D_updatedAll.root"]
            el_h_high = ["EGamma_SF2D", "EGamma_SF2D"]

        else:
            return

        mu_f_tight = ["%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/leptonSF/%s/muon/" % (os.environ['CMSSW_BASE'],year) + f for f in mu_f_tight]
        mu_f_loose = ["%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/leptonSF/%s/muon/" % (os.environ['CMSSW_BASE'],year) + f for f in mu_f_loose]
        el_f_low = ["%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/leptonSF/%s/electron/" % (os.environ['CMSSW_BASE'],year) + f for f in el_f_low]
        el_f_high = ["%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/leptonSF/%s/electron/" % (os.environ['CMSSW_BASE'],year) + f for f in el_f_high]

        self.mu_f_tight = ROOT.std.vector(str)(len(mu_f_tight))
        self.mu_h_tight = ROOT.std.vector(str)(len(mu_f_tight))
        for i in range(len(mu_f_tight)): self.mu_f_tight[i] = mu_f_tight[i]; self.mu_h_tight[i] = mu_h_tight[i];

        self.mu_f_loose = ROOT.std.vector(str)(len(mu_f_loose))
        self.mu_h_loose = ROOT.std.vector(str)(len(mu_f_loose))
        for i in range(len(mu_f_loose)): self.mu_f_loose[i] = mu_f_loose[i]; self.mu_h_loose[i] = mu_h_loose[i];

        self.el_f_low = ROOT.std.vector(str)(len(el_f_low))
        self.el_h_low = ROOT.std.vector(str)(len(el_h_low))
        for i in range(len(el_f_low)): self.el_f_low[i] = el_f_low[i]; self.el_h_low[i] = el_h_low[i];

        self.el_f_high = ROOT.std.vector(str)(len(el_f_high))
        self.el_h_high = ROOT.std.vector(str)(len(el_f_high))
        for i in range(len(el_f_high)): self.el_f_high[i] = el_f_high[i]; self.el_h_high[i] = el_h_high[i];

        if "/LeptonEfficiencyCorrector_cc.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ Worker"
            ROOT.gROOT.ProcessLine(".L %s/src/PhysicsTools/NanoAODTools/python/postprocessing/helpers/LeptonEfficiencyCorrector.cc+" % os.environ['CMSSW_BASE'])
    def beginJob(self):
        self._worker_mu_tight = ROOT.LeptonEfficiencyCorrector(self.mu_f_tight,self.mu_h_tight)
        self._worker_mu_loose = ROOT.LeptonEfficiencyCorrector(self.mu_f_loose,self.mu_h_loose)
        self._worker_el_low = ROOT.LeptonEfficiencyCorrector(self.el_f_low,self.el_h_low)
        self._worker_el_high = ROOT.LeptonEfficiencyCorrector(self.el_f_high,self.el_h_high)
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("lepton_effsf", "F", lenVar="nlepton")
        self.out.branch("lepton_effsferr", "F", lenVar="nlepton")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        lep = Collection(event, "lepton")
        sf = []
        sf_err = []
        for i in range(0,len(lep)):
            # print ("lepton_pdg_id:    "+str(lep[i].pdg_id) + "    lepton_pt:    "+str(lep[i].pt))
            if abs(event.lepton_pdg_id[i]) == 11:
                if event.lepton_pt[i] < 20.:
                    sf.append(self._worker_el_low.getSF(lep[i].pdg_id, lep[i].pt, lep[i].eta))
                    sf_err.append(self._worker_el_low.getSFErr(lep[i].pdg_id, lep[i].pt, lep[i].eta))
                else:
                    sf.append(self._worker_el_low.getSF(lep[i].pdg_id, lep[i].pt, lep[i].eta))
                    sf_err.append(self._worker_el_low.getSFErr(lep[i].pdg_id, lep[i].pt, lep[i].eta))
            elif abs(event.lepton_pdg_id[i]) == 13:
                if event.lepton_tight[i]:
                    sf.append(self._worker_el_low.getSF(lep[i].pdg_id, lep[i].pt, lep[i].eta))
                    sf_err.append(self._worker_el_low.getSFErr(lep[i].pdg_id, lep[i].pt, lep[i].eta))
                else:
                    sf.append(self._worker_mu_loose.getSF(lep[i].pdg_id, lep[i].pt, lep[i].eta))
                    sf_err.append(self._worker_mu_loose.getSFErr(lep[i].pdg_id, lep[i].pt, lep[i].eta))

        self.out.fillBranch("lepton_effsf", sf)
        self.out.fillBranch("lepton_effsferr", sf_err)
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

lepSF_2016 = lambda : lepSFProducer('2016')
lepSF_2017 = lambda : lepSFProducer('2017')
lepSF_2018 = lambda : lepSFProducer('2018')

