import ROOT
import os
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


def mk_safe(fct, *args):
    try:
        return fct(*args)
    except Exception as e:
        if any('Error in function boost::math::erf_inv' in arg for arg in e.args):
            print 'WARNING: catching exception and returning -1. Exception arguments: %s' % e.args
            return -1.
        else:
            raise e


class muonScaleResProducer(Module):
    def __init__(self, rc_dir, rc_corrections, dataYear):
        p_postproc = '%s/python/PhysicsTools/NanoAODTools/postprocessing' % os.environ['CMSSW_BASE']
        p_roccor = p_postproc + '/data/' + rc_dir
        if "/RoccoR_cc.so" not in ROOT.gSystem.GetLibraries():
            p_helper = '%s/RoccoR.cc' % p_roccor
            print 'Loading C++ helper from ' + p_helper
            ROOT.gROOT.ProcessLine('.L ' + p_helper)
        self._roccor = ROOT.RoccoR(p_roccor + '/' + rc_corrections)

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("lepton_corrected_pt", "F", lenVar="nlepton")
        self.out.branch("lepton_correctedUp_pt", "F", lenVar="nlepton")
        self.out.branch("lepton_correctedDown_pt", "F", lenVar="nlepton")
        self.is_mc = bool(inputTree.GetBranch("GenJet_pt"))

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        muons = Collection(event, "lepton")
        electrons = Collection(event, "Electron")
        if self.is_mc:
            genparticles = Collection(event, "GenPart")
        roccor = self._roccor
        if self.is_mc:
            pt_corr=[]
            pt_err=[]
            for mu in muons:
                if abs(mu.pdgId) == 13:
                    genIdx = mu.genPartIdx
                    if genIdx >= 0 and genIdx < len(genparticles):
                        genMu = genparticles[genIdx]
                        pt_corr.append(mu.pt * mk_safe(roccor.kSpreadMC, mu.charge, mu.pt, mu.eta, mu.phi, genMu.pt))
                        pt_err.append(mu.pt*mk_safe(roccor.kSpreadMCerror, mu.charge, mu.pt, mu.eta, mu.phi, genMu.pt))
                    else:
                        u1 = random.uniform(0.0, 1.0)
                        pt_corr.append(mu.pt*mk_safe(roccor.kSmearMC, mu.charge, mu.pt, mu.eta, mu.phi, mu.nTrackerLayers, u1))
                        pt_err.append(mu.pt*mk_safe(roccor.kSmearMCerror, mu.charge, mu.pt, mu.eta, mu.phi, mu.nTrackerLayers, u1))
                elif abs(mu.pdgId) == 11:
                    try:
                        pt_corr.append(mu.pt/electrons[mu.idx].eCorr)
                    except ZeroDivisionError:
                        pt_corr.append(-9999.)
                    pt_err.append(electrons[mu.idx].energyErr)
                else:
                    continue
        else:
            pt_corr=[]
            pt_err=[]
            for mu in muons:
                if abs(mu.pdgId) == 13:
                    pt_corr.append(mu.pt * mk_safe(roccor.kScaleDT,mu.charge, mu.pt, mu.eta, mu.phi))
                    pt_err.append(mu.pt * mk_safe(roccor.kScaleDTerror,mu.charge, mu.pt, mu.eta, mu.phi))
                elif abs(mu.pdgId) == 11:
                    try:
                        pt_corr.append(mu.pt/electrons[mu.idx].eCorr)
                    except ZeroDivisionError:
                        pt_corr.append(-9999.)
                    pt_err.append(electrons[mu.idx].energyErr)
                else:
                    continue


        self.out.fillBranch("lepton_corrected_pt", pt_corr)
        pt_corr_up = list( max(pt_corr[imu]+pt_err[imu], 0.0) for imu,mu in enumerate(muons) )
        pt_corr_down = list( max(pt_corr[imu]-pt_err[imu], 0.0) for imu,mu in enumerate(muons) )
        self.out.fillBranch("lepton_correctedUp_pt",  pt_corr_up)
        self.out.fillBranch("lepton_correctedDown_pt",  pt_corr_down)
        return True


muonScaleRes2016 = lambda : muonScaleResProducer('roccor.Run2.v3', 'RoccoR2016.txt', 2016)
muonScaleRes2017 = lambda : muonScaleResProducer('roccor.Run2.v3', 'RoccoR2017.txt', 2017)
muonScaleRes2018 = lambda : muonScaleResProducer('roccor.Run2.v3', 'RoccoR2018.txt', 2018)
