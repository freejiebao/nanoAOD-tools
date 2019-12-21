import ROOT

from math import cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi

class wgFakeLeptonProducer(Module):
    def __init__(self, sortkey=lambda x: x.pt, reverse=True, selector=None, year='2016'):
        self.sortkey = lambda (obj, j, i): sortkey(obj)
        self.reverse = reverse
        self.selector = [(selector[coll] if coll in selector else (lambda x: True)) for coll in self.input] if selector else None  # pass dict([(collection_name,lambda obj : selection(obj)])
        self.year = year
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("run",  "i")
        self.out.branch("lumi",  "i")
        self.out.branch("event",  "l")
        self.out.branch("met",  "F")
        self.out.branch("mt",  "F")
        self.out.branch("lepton_idx", "I", lenVar="nlepton")
        self.out.branch("lepton_pdg_id",  "I", lenVar="nlepton")
        self.out.branch("lepton_tight", "B", lenVar="nlepton")
        self.out.branch("lepton_fakeable", "B", lenVar="nlepton")
        self.out.branch("lepton_pt", "F", lenVar="nlepton")
        self.out.branch("lepton_eta", "F", lenVar="nlepton")
        self.out.branch("lepton_phi", "F", lenVar="nlepton")
        self.out.branch("lepton_mass", "F", lenVar="nlepton")
        self.out.branch("lepton_mishits", "I", lenVar="nlepton")
        self.out.branch("lepton_tkIsoId", "I", lenVar="nlepton")
        self.out.branch("lepton_real", "B", lenVar="nlepton")
        self.out.branch("gen_weight", "F")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def muonID(self, lep):

        is_fakeable_id = False
        is_tight_id = False

        # loose muon: nanoAOD after basic selection (pt > 3 && track.isNonnull && isLooseMuon)
        # is_loose_id = True

        if self.year == '2016':
            # fakeable muon
            #if leptons[idx][0].tightId and leptons[idx][0].pfRelIso04_all < 0.4 and leptons[idx][0].tkIsoId > 0:
            if lep.tightId and lep.pfRelIso04_all < 0.4:
                is_fakeable_id = True

            # tight muon
            if lep.tightId and lep.pfRelIso04_all < 0.15 and lep.dxy < 0.2 and lep.dz < 0.5:
                is_tight_id = True

        elif self.year == '2017':
            # fakeable muon
            #if leptons[idx][0].tightId and leptons[idx][0].pfRelIso04_all < 0.4 and leptons[idx][0].tkIsoId > 0:
            if lep.tightId and lep.pfRelIso04_all < 0.4:
                is_fakeable_id = True

            # tight muon
            if lep.mvaId >= 3 and lep.miniIsoId >= 3:
                # if leptons[idx][0].tightId and leptons[idx][0].miniIsoId > 2:
                is_tight_id = True

        elif self.year == '2018':
            # fakeable muon
            #if leptons[idx][0].tightId and leptons[idx][0].pfRelIso04_all < 0.4 and leptons[idx][0].tkIsoId > 0:
            if lep.tightId and lep.pfRelIso04_all < 0.4:
                is_fakeable_id = True

            # tight muon
            if lep.tightId and lep.miniIsoId >= 3 and lep.dxy < 0.2 and lep.dz < 0.5:
                is_tight_id = True

        # if this muon is just loose, then drop this event
        if is_fakeable_id or is_tight_id:
            store = True
        else:
            store = False
        return store, is_fakeable_id, is_tight_id

    def electronID(self, lep):

        is_fakeable_id = False
        is_tight_id = False

        if self.year == '2016':

            # fakeable electron
            # print leptons[i][0].pdgId, leptons[i][0].cutBased_HLTPreSel, leptons[i][0].mvaFall17V2Iso_WP80, leptons[i][0].tightCharge,leptons[i][0].eta
            if lep.cutBased_HLTPreSel >= 1: # quite important '>=': cutBased_HLTPreSel: 0, fail; 1 loose; 2 tight
                is_fakeable_id = True

            # tight electron
            if lep.mvaFall17V2Iso_WP80 and lep.tightCharge == 2:
                # if leptons[i][0].cutBased > 3 and leptons[i][0].tightCharge == 2:
                is_tight_id = True

        elif self.year == '2017':

            # fakeable electron
            if lep.cutBased >= 2 and (abs(lep.eta) <= 1.479 or (abs(lep.eta) > 1.479 and lep.sieie < 0.03 and lep.eInvMinusPInv < 0.014)):
                #if lep.cutBased >= 1:
                is_fakeable_id = True

            # tight electron
            if lep.cutBased >= 4 and lep.tightCharge == 2:
                is_tight_id = True

        elif self.year == '2018':

            # fakeable electron
            if lep.cutBased >= 2 and (abs(lep.eta) <= 1.479 or (abs(lep.eta) > 1.479 and lep.sieie < 0.03 and lep.eInvMinusPInv < 0.014)):
                #if lep.cutBased >= 1:
                is_fakeable_id = True

            # tight electron
            if lep.mvaFall17V2Iso_WP80 and lep.tightCharge == 2:
                # if leptons[i][0].cutBased > 3 and leptons[i][0].tightCharge == 2:
                is_tight_id = True

        # if this electron is just loose, then drop this event
        if is_fakeable_id or is_tight_id:
            store = True
        else:
            store = False

        return store, is_fakeable_id, is_tight_id

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        input = ["Electron", "Muon"]
        coll = [Collection(event, x) for x in input]
        # merge muon and electron collections together, and ordered according pt
        leptons = [(coll[j][i], j, i) for j in xrange(len(input)) for i in xrange(len(coll[j]))]
        if self.selector: leptons = filter(lambda (obj, j, i): self.selector[j](obj), leptons)
        leptons.sort(key=self.sortkey, reverse=self.reverse)

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")

        is_fakeable=[]
        is_tight=[]
        loose_leptons=[]



        for i in range(0,len(leptons)):

            if abs(leptons[i][0].pdgId) == 13:
                if leptons[i][0].pt < 10:
                    continue
                if abs(leptons[i][0].eta) > 2.4:
                    continue
                store, is_fakeable_id, is_tight_id = self.muonID(leptons[i][0]) # is this muon fakeable or tight

                if store:
                    is_fakeable.append(is_fakeable_id)
                    is_tight.append(is_tight_id)
                    loose_leptons.append(i)
                    if len(loose_leptons) > 1:
                        return False
                else:
                    continue
            elif abs(leptons[i][0].pdgId) == 11:
                if leptons[i][0].pt < 10:
                    continue
                if abs(leptons[i][0].eta + leptons[i][0].deltaEtaSC) > 2.5:
                    continue
                if (abs(leptons[i][0].eta + leptons[i][0].deltaEtaSC) <= 1.479 and abs(leptons[i][0].dz) < 0.1 and abs(leptons[i][0].dxy) < 0.05) or (abs(leptons[i][0].eta + leptons[i][0].deltaEtaSC) > 1.479 and abs(leptons[i][0].dz) < 0.2 and abs(leptons[i][0].dxy) < 0.1):
                    # loose electron
                    if leptons[i][0].cutBased >= 1:
                        is_loose_id = True
                    else:
                        is_loose_id = False
                    store, is_fakeable_id, is_tight_id = self.electronID(leptons[i][0])
                    if store:
                        is_fakeable.append(is_fakeable_id)
                        is_tight.append(is_tight_id)
                        loose_leptons.append(i)
                        if len(loose_leptons) > 1:
                            return False
                    # if is_loose_id is true, there will be additional loose leptons, so this event will be dropped
                    elif is_loose_id:
                        return False
                    # if is_loose_id is false, just skip this lepton
                    else:
                        continue

        lepton_mishits=[-9999]
        lepton_tkIsoId=[-9999]
        if len(loose_leptons)==1:
            if abs(leptons[loose_leptons[0]][0].pdgId)==13:
                if not (event.HLT_Mu17_TrkIsoVVL or event.HLT_Mu8):
                    return False
                lepton_tkIsoId[0]=leptons[loose_leptons[0]][0].tkIsoId
            elif abs(leptons[loose_leptons[0]][0].pdgId)==11:
                if not (event.HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30):
                    return False
                lepton_mishits[0]=leptons[loose_leptons[0]][0].lostHits
        else:
            return False



        found_other_jet = False

        for i in range(0,len(jets)):

            if jets[i].pt < 20:
                continue

            if abs(jets[i].eta) > 4.7:
                continue

            if not jets[i].jetId & (1 << 0):
                continue

            if deltaR(leptons[loose_leptons[0]][0].eta,leptons[loose_leptons[0]][0].phi,jets[i].eta,jets[i].phi) > 0.3:
                found_other_jet = True

        if not found_other_jet:
            return False

        lepton_idx=[loose_leptons[0]]
        lepton_pdg_id=[leptons[loose_leptons[0]][0].pdgId]
        lepton_tight=[is_tight[0]]
        lepton_fakeable=[is_fakeable[0]]
        lepton_pt=[leptons[loose_leptons[0]][0].pt]
        lepton_eta=[leptons[loose_leptons[0]][0].eta]
        lepton_phi=[leptons[loose_leptons[0]][0].phi]
        lepton_mass=[leptons[loose_leptons[0]][0].mass]

        lepton_real=[False]
        if hasattr(event, 'nGenPart'):
            genparts = Collection(event, "GenPart")
            try:
                for j in range(0, len(genparts)):
                    if genparts[j].pt > 5 and abs(genparts[j].pdgId) == abs(leptons[loose_leptons[0]][0].pdgId) and ((genparts[j].statusFlags >> 0 & 1) or (genparts[j].statusFlags >> 5 & 1)) and deltaR(leptons[loose_leptons[0]][0].eta, leptons[loose_leptons[0]][0].phi, genparts[j].eta, genparts[j].phi) < 0.3:
                        lepton_real[0]=True
                        break
            except:
                pass

        self.out.fillBranch("run",event.run)
        self.out.fillBranch("lumi",event.luminosityBlock)
        self.out.fillBranch("event",event.event)
        self.out.fillBranch("met",event.MET_pt)
        self.out.fillBranch("mt",sqrt(2*leptons[loose_leptons[0]][0].pt*event.MET_pt*(1 - cos(event.MET_phi - leptons[loose_leptons[0]][0].phi))))
        self.out.fillBranch("lepton_idx",lepton_idx)
        self.out.fillBranch("lepton_pdg_id",lepton_pdg_id)
        self.out.fillBranch("lepton_tight",lepton_tight)
        self.out.fillBranch("lepton_fakeable",lepton_fakeable)
        self.out.fillBranch("lepton_pt",lepton_pt)
        self.out.fillBranch("lepton_eta",lepton_eta)
        self.out.fillBranch("lepton_phi",lepton_phi)
        self.out.fillBranch("lepton_mass",lepton_mass)
        self.out.fillBranch("lepton_mishits",lepton_mishits)
        self.out.fillBranch("lepton_tkIsoId",lepton_tkIsoId)
        self.out.fillBranch("lepton_real",lepton_real)
        if hasattr(event,'Generator_weight'):
            self.out.fillBranch("gen_weight",event.Generator_weight)

        return True

wgFakeLeptonModule2016 = lambda : wgFakeLeptonProducer(year='2016')