import ROOT

from math import cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi


class sswwProducer(Module):
    def __init__(self, thoeretic=False, fakelepton=False):
        self.thoeretic = thoeretic
        self.fakelepton = fakelepton
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        if self.thoeretic:
            self.out.branch("QCD_unc", "F")
            self.out.branch("SCALE_unc", "F")
        if self.fakelepton:
            self.out.branch("lepton_fake_weight","nlepton")
            self.out.branch("lepton_fake_weight_up","nlepton")
            self.out.branch("lepton_fake_weight_down","nlepton")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def theory_unc(self, event):
        #df = ROOT.ROOT.RDataFrame("Events", files)
        sum=0.
        sum_squre=0.
        QCD_unc=0
        if hasattr(event,'nLHEPdfWeight'):
            if event.nLHEPdfWeight > 1:
                for i in range(0,event.nLHEPdfWeight):
                    sum+=event.LHEPdfWeight[i]
                    sum_squre+=event.LHEPdfWeight[i]*event.LHEPdfWeight[i]
                mean=sum/event.nLHEPdfWeight
                QCD_unc=sqrt((sum_squre- event.nLHEPdfWeight*mean*mean)/(event.nLHEPdfWeight-1))

        SCALE_unc = 0
        if hasattr(event,'nLHEScaleWeight'):
            if event.nLHEScaleWeight > 1:
                Max=event.LHEScaleWeight[0]
                Min=event.LHEScaleWeight[0]
                Cen=event.LHEScaleWeight[4]
                for i in range(0,event.nLHEScaleWeight):
                    if (not i==2) or (not i==6):
                        if Max<event.LHEScaleWeight[i]:
                            Max=event.LHEScaleWeight[i]
                        if Min>event.LHEScaleWeight[i]:
                            Min=event.LHEScaleWeight[i]
                SCALE_unc = max(abs(Max-Cen),abs(Min-Cen))/Cen

        return QCD_unc,SCALE_unc

    def fake_muon_event_weight(eta,pt,histo):

        myeta  = min(abs(eta),2.4999)
        mypt   = min(pt,44.999)

        etabin = histo.GetXaxis().FindFixBin(myeta)
        ptbin = histo.GetYaxis().FindFixBin(mypt)

        prob = histo.GetBinContent(etabin,ptbin)
        up=prob+histo.GetBinError(etabin,ptbin)
        down=prob-histo.GetBinError(etabin,ptbin)

        return prob/(1-prob),up/(1-up),down/(1-down)

    def fake_electron_event_weight(eta,pt,histo):

        myeta  = min(abs(eta),2.4999)
        mypt   = min(pt,44.999)

        etabin = histo.GetXaxis().FindFixBin(myeta)
        ptbin = histo.GetYaxis().FindFixBin(mypt)

        prob = histo.GetBinContent(etabin,ptbin)
        up=prob+histo.GetBinError(etabin,ptbin)
        down=prob-histo.GetBinError(etabin,ptbin)

        return prob/(1-prob),up/(1-up),down/(1-down)

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        # refer to: https://github.com/cms-nanoAOD/nanoAOD-tools/blob/b20be01e2087412051abb5d5b59d0a3d07835207/python/postprocessing/modules/common/collectionMerger.py#L56-L60
        # merge Electron and Muon to Lepton
        if self.thoeretic:
            QCD_unc, SCALE_unc=self.theory_unc(event)
            self.out.fillBranch("QCD_unc", QCD_unc)
            self.out.fillBranch("SCALE_unc", SCALE_unc)
        if self.fakelepton:
            muon_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/wg/2016/muon_frs_data_subtract_wjets_zjets.root")
            electron_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/wg/2016/electron_frs_data_subtract_wjets_zjets.root")

            muon_fr_hist=muon_fr_file.Get("muon_frs")
            electron_fr_hist=electron_fr_file.Get("electron_frs")

            lepton_fake_weight = []
            lepton_fake_weight_up = []
            lepton_fake_weight_down = []

            leptons = Collection(event, "lepton")
            for lep in leptons:
                if abs(lep.pdg_id)==11:
                    nominal,up,down=self.fake_electron_event_weight(lep.eta,lep.pt,electron_fr_hist)
                elif abs(lep.pdg_id)==13:
                    nominal,up,down=self.fake_muon_event_weight(lep.eta,lep.pt,muon_fr_hist)
                else:
                    return False
                lepton_fake_weight.append(nominal)
                lepton_fake_weight_up.append(up)
                lepton_fake_weight_down.append(down)

            self.out.fillBranch("lepton_fake_weight", lepton_fake_weight)
            self.out.fillBranch("lepton_fake_weight_up", lepton_fake_weight_up)
            self.out.fillBranch("lepton_fake_weight_down", lepton_fake_weight_down)
        return True


helper_thoeretic = lambda: sswwProducer(thoeretic=True)
helper_fakelepton = lambda: sswwProducer(fakelepton=True)

# python scripts/nano_postproc.py . 2016_DoubleEG_nanoAOD.root -I PhysicsTools.NanoAODTools.postprocessing.examples.sswwModule_copy sswwModule2016 --bi crab/ssww_keep_and_drop_2016.txt --bo crab/ssww_output_branch_selection_2016.txt
