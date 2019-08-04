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
    def __init__(self, rc_dir, rc_corrections, dataYear,sortkey=lambda x: x.pt,reverse=True):
        p_postproc = '%s/python/PhysicsTools/NanoAODTools/postprocessing' % os.environ['CMSSW_BASE']
        p_roccor = p_postproc + '/data/' + rc_dir
        if "/RoccoR_cc.so" not in ROOT.gSystem.GetLibraries():
            p_helper = '%s/RoccoR.cc' % p_roccor
            print 'Loading C++ helper from ' + p_helper
            ROOT.gROOT.ProcessLine('.L ' + p_helper)
        self._roccor = ROOT.RoccoR(p_roccor + '/' + rc_corrections)
        self.sortkey = lambda (obj, j, i): sortkey(obj)
        self.reverse = reverse

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
        leptons = Collection(event, "lepton")
        input = ["Electron", "Muon"]
        coll = [Collection(event, x) for x in input]
        merge = [(coll[j][i], j, i) for j in xrange(len(input)) for i in xrange(len(coll[j]))]
        merge.sort(key=self.sortkey, reverse=self.reverse)
        if self.is_mc:
            genparticles = Collection(event, "GenPart")
        roccor = self._roccor
        if self.is_mc:
            pt_corr=[]
            pt_err=[]
            for lep in leptons:
                if abs(lep.pdg_id) == 13:
                    genIdx = merge[lep.idx][0].genPartIdx
                    if genIdx >= 0 and genIdx < len(genparticles):
                        genMu = genparticles[genIdx]
                        pt_corr.append(lep.pt * mk_safe(roccor.kSpreadMC, merge[lep.idx][0].charge, lep.pt, lep.eta, lep.phi, genMu.pt))
                        pt_err.append(lep.pt*mk_safe(roccor.kSpreadMCerror, merge[lep.idx][0].charge, lep.pt, lep.eta, lep.phi, genMu.pt))
                    else:
                        u1 = random.uniform(0.0, 1.0)
                        pt_corr.append(lep.pt*mk_safe(roccor.kSmearMC, merge[lep.idx][0].charge, lep.pt, lep.eta, lep.phi, merge[lep.idx][0].nTrackerLayers, u1))
                        pt_err.append(lep.pt*mk_safe(roccor.kSmearMCerror, merge[lep.idx][0].charge, lep.pt, lep.eta, lep.phi, merge[lep.idx][0].nTrackerLayers, u1))
                elif abs(lep.pdg_id) == 11:
                    try:
                        pt_corr.append(lep.pt/merge[lep.idx][0].eCorr)
                    except:
                        pt_corr.append(lep.pt)
                    pt_err.append(merge[lep.idx][0].energyErr)
                else:
                    continue
        else:
            pt_corr=[]
            pt_err=[]
            for lep in leptons:
                if abs(lep.pdg_id) == 13:
                    pt_corr.append(lep.pt * mk_safe(roccor.kScaleDT,merge[lep.idx][0].charge, lep.pt, lep.eta, lep.phi))
                    pt_err.append(lep.pt * mk_safe(roccor.kScaleDTerror,merge[lep.idx][0].charge, lep.pt, lep.eta, lep.phi))
                elif abs(lep.pdg_id) == 11:
                    try:
                        pt_corr.append(lep.pt/merge[lep.idx][0].eCorr)
                    except:
                        pt_corr.append(lep.pt)
                    pt_err.append(merge[lep.idx][0].energyErr)
                else:
                    continue


        self.out.fillBranch("lepton_corrected_pt", pt_corr)
        pt_corr_up = list( max(pt_corr[ilep]+pt_err[ilep], 0.0) for ilep,lep in enumerate(leptons) )
        pt_corr_down = list( max(pt_corr[ilep]-pt_err[ilep], 0.0) for ilep,lep in enumerate(leptons) )
        self.out.fillBranch("lepton_correctedUp_pt",  pt_corr_up)
        self.out.fillBranch("lepton_correctedDown_pt",  pt_corr_down)
        return True

muonScaleRes2016 = lambda : muonScaleResProducer(rc_dir = 'roccor.Run2.v3', rc_corrections = 'RoccoR2016.txt', dataYear = 2016)
muonScaleRes2017 = lambda : muonScaleResProducer(rc_dir = 'roccor.Run2.v3', rc_corrections = 'RoccoR2017.txt', dataYear = 2017)
muonScaleRes2018 = lambda : muonScaleResProducer(rc_dir = 'roccor.Run2.v3', rc_corrections = 'RoccoR2018.txt', dataYear = 2018)
