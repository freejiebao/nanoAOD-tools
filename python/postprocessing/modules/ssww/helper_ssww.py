import ROOT

from math import cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi


class sswwProducer(Module):
    def __init__(self, thoeretic=False):
        self.thoeretic = thoeretic
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("QCD_unc", "F")
        self.out.branch("SCALE_unc", "F")
        self.out.branch("xsweight", "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def theory_unc(self, event):
        #df = ROOT.ROOT.RDataFrame("Events", files)
        sum=0.
        sum_squre=0.
        if event.hasattr('nLHEPdfWeight'):
            for i in range(0,event.nLHEPdfWeight):
                sum+=event.LHEPdfWeight[i]
                sum_squre+=event.LHEPdfWeight[i]*event.LHEPdfWeight[i]
            mean=sum/event.nLHEPdfWeight
            QCD_unc=sqrt((sum_squre- event.nLHEPdfWeight*mean*mean)/(event.nLHEPdfWeight-1))
        else:
            QCD_unc=0

        if event.hasattr('nLHEScaleWeight'):
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
        else:
            SCALE_unc = 0

        return QCD_unc,SCALE_unc

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        # refer to: https://github.com/cms-nanoAOD/nanoAOD-tools/blob/b20be01e2087412051abb5d5b59d0a3d07835207/python/postprocessing/modules/common/collectionMerger.py#L56-L60
        # merge Electron and Muon to Lepton
        QCD_unc, SCALE_unc=self.theory_unc(event)
        self.out.fillBranch("QCD_unc", QCD_unc)
        self.out.fillBranch("SCALE_unc", SCALE_unc)
        return True


helper_thoeretic = lambda: sswwProducer(thoeretic=True)

# python scripts/nano_postproc.py . 2016_DoubleEG_nanoAOD.root -I PhysicsTools.NanoAODTools.postprocessing.examples.sswwModule_copy sswwModule2016 --bi crab/ssww_keep_and_drop_2016.txt --bo crab/ssww_output_branch_selection_2016.txt
