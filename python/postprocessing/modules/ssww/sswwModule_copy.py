import ROOT

from math import cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi


class sswwProducer(Module):
    def __init__(self, sortkey=lambda x: x.pt, reverse=True, selector=None, minObjects=None, maxObjects=None, preSel=False, year='2016'):
        self.sortkey = lambda (obj, j, i): sortkey(obj)
        self.reverse = reverse
        self.selector = [(selector[coll] if coll in selector else (lambda x: True)) for coll in self.input] if selector else None  # pass dict([(collection_name,lambda obj : selection(obj)])
        self.minObjects = minObjects  # save only the first maxObjects objects passing the selection in the merged collection
        self.maxObjects = maxObjects  # save only the first maxObjects objects passing the selection in the merged collection
        self.preSel = preSel
        self.year = year
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("run", "i")
        self.out.branch("lumi", "i")
        self.out.branch("event", "l")
        self.out.branch("npu", "I")
        self.out.branch("ntruepu", "F")
        self.out.branch("npvs", "I")
        self.out.branch("gen_weight", "F")
        # tau tag
        #self.out.branch("tauTag", "B")
        self.out.branch("tauTagVVVLooseVSe", "B")
        self.out.branch("tauTagVVLooseVSe", "B")
        self.out.branch("tauTagVLooseVSe", "B")
        self.out.branch("tauTagLooseVSe", "B")
        self.out.branch("tauTagMediumVSe", "B")
        self.out.branch("tauTagTightVSe", "B")
        self.out.branch("tauTagVTightVSe", "B")
        self.out.branch("tauTagVVTightVSe", "B")

        self.out.branch("tauTagVVVLooseVSjet", "B")
        self.out.branch("tauTagVVLooseVSjet", "B")
        self.out.branch("tauTagVLooseVSjet", "B")
        self.out.branch("tauTagLooseVSjet", "B")
        self.out.branch("tauTagMediumVSjet", "B")
        self.out.branch("tauTagTightVSjet", "B")
        self.out.branch("tauTagVTightVSjet", "B")
        self.out.branch("tauTagVVTightVSjet", "B")

        self.out.branch("tauTagVLooseVSmu", "B")
        self.out.branch("tauTagLooseVSmu", "B")
        self.out.branch("tauTagMediumVSmu", "B")
        self.out.branch("tauTagTightVSmu", "B")

        self.out.branch("softmuonTag", "B")
        self.out.branch("n_tight_leptons", "I")
        self.out.branch("n_fakeable_leptons", "I")
        self.out.branch("lepton_idx", "I", lenVar="nlepton")
        self.out.branch("lepton_pdgId", "I", lenVar="nlepton")
        self.out.branch("lepton_tight", "B", lenVar="nlepton")
        self.out.branch("lepton_fakeable", "B", lenVar="nlepton")
        self.out.branch("lepton_pt", "F", lenVar="nlepton")
        self.out.branch("lepton_eta", "F", lenVar="nlepton")
        self.out.branch("lepton_phi", "F", lenVar="nlepton")
        self.out.branch("lepton_mass", "F", lenVar="nlepton")
        self.out.branch("lepton_real", "B", lenVar="nlepton")
        self.out.branch("lepton_mishits", "I", lenVar="nlepton")
        self.out.branch("lepton_tkIsoId", "I", lenVar="nlepton")
        self.out.branch("lepton_softmu", "B", lenVar="nlepton")
        self.out.branch("lepton_zep", "F", lenVar="nlepton")
        self.out.branch("mll", "F")
        '''
        self.out.branch("mll02", "F")
        self.out.branch("mll12", "F")
        self.out.branch("mlll", "F")
        self.out.branch("mll_z0", "F")
        self.out.branch("mll_z1", "F")
        self.out.branch("mllll", "F")
        '''
        self.out.branch("detajj", "F")
        self.out.branch("jet_idx", "I", lenVar="njet")
        self.out.branch("jet_jetId", "I", lenVar="njet")
        self.out.branch("jet_puId", "I", lenVar="njet")
        self.out.branch("jet_pt", "F", lenVar="njet")
        self.out.branch("jet_eta", "F", lenVar="njet")
        self.out.branch("jet_phi", "F", lenVar="njet")
        self.out.branch("jet_mass", "F", lenVar="njet")
        self.out.branch("jet_btagCSVV2", "F", lenVar="njet")
        self.out.branch("jet_btagDeepB", "F", lenVar="njet")
        self.out.branch("jet_hadronFlavour", "I", lenVar="njet")
        self.out.branch("jet_partonFlavour", "I", lenVar="njet")
        # b tag
        self.out.branch("btagCSVV2Loose", "B")
        self.out.branch("btagCSVV2Medium", "B")
        self.out.branch("btagCSVV2Tight", "B")

        self.out.branch("btagDeepBLoose", "B")
        self.out.branch("btagDeepBMedium", "B")
        self.out.branch("btagDeepBTight", "B")

        self.out.branch("mjj", "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def muonID(self, lep, n_fakeable_leptons, n_tight_leptons):

        is_fakeable_id = False
        is_tight_id = False

        # loose muon: nanoAOD after basic selection (pt > 3 && track.isNonnull && isLooseMuon)
        # is_loose_id = True

        if self.year == '2016':
            # fakeable muon
            #if leptons[idx][0].tightId and leptons[idx][0].pfRelIso04_all < 0.4 and leptons[idx][0].tkIsoId > 0:
            if lep.tightId and lep.pfRelIso04_all < 0.4:
                is_fakeable_id = True
                n_fakeable_leptons += 1

            # tight muon
            if lep.tightId and lep.pfRelIso04_all < 0.15 and lep.dxy < 0.2 and lep.dz < 0.5:
                is_tight_id = True
                n_tight_leptons += 1

        elif self.year == '2017':
            # fakeable muon
            #if leptons[idx][0].tightId and leptons[idx][0].pfRelIso04_all < 0.4 and leptons[idx][0].tkIsoId > 0:
            if lep.tightId and lep.pfRelIso04_all < 0.4:
                is_fakeable_id = True
                n_fakeable_leptons += 1

            # tight muon
            if lep.mvaId >= 3 and lep.miniIsoId >= 3:
                # if leptons[idx][0].tightId and leptons[idx][0].miniIsoId > 2:
                is_tight_id = True
                n_tight_leptons += 1

        elif self.year == '2018':
            # fakeable muon
            #if leptons[idx][0].tightId and leptons[idx][0].pfRelIso04_all < 0.4 and leptons[idx][0].tkIsoId > 0:
            if lep.tightId and lep.pfRelIso04_all < 0.4:
                is_fakeable_id = True
                n_fakeable_leptons += 1

            # tight muon
            if lep.tightId and lep.miniIsoId >= 3 and lep.dxy < 0.2 and lep.dz < 0.5:
                is_tight_id = True
                n_tight_leptons += 1

        # if this muon is just loose, then drop this event
        if is_fakeable_id or is_tight_id:
            store = True
        else:
            store = False
        return store, is_fakeable_id, is_tight_id, n_fakeable_leptons, n_tight_leptons

    def electronID(self, lep, n_fakeable_leptons, n_tight_leptons):

        is_fakeable_id = False
        is_tight_id = False

        if self.year == '2016':

            # fakeable electron
            # print leptons[i][0].pdgId, leptons[i][0].cutBased_HLTPreSel, leptons[i][0].mvaFall17V2Iso_WP80, leptons[i][0].tightCharge,leptons[i][0].eta
            if lep.cutBased_HLTPreSel >= 1: # quite important '>=': cutBased_HLTPreSel: 0, fail; 1 loose; 2 tight
                is_fakeable_id = True
                n_fakeable_leptons += 1

            # tight electron
            if lep.mvaFall17V2Iso_WP80 and lep.tightCharge == 2:
                # if leptons[i][0].cutBased > 3 and leptons[i][0].tightCharge == 2:
                is_tight_id = True
                n_tight_leptons += 1

        elif self.year == '2017':

            # fakeable electron
            if lep.cutBased >= 2 and (abs(lep.eta) <= 1.479 or (abs(lep.eta) > 1.479 and lep.sieie < 0.03 and lep.eInvMinusPInv < 0.014)):
            #if lep.cutBased >= 1:
                is_fakeable_id = True
                n_fakeable_leptons += 1

            # tight electron
            if lep.cutBased >= 4 and lep.tightCharge == 2:
                is_tight_id = True
                n_tight_leptons += 1

        elif self.year == '2018':

            # fakeable electron
            if lep.cutBased >= 2 and (abs(lep.eta) <= 1.479 or (abs(lep.eta) > 1.479 and lep.sieie < 0.03 and lep.eInvMinusPInv < 0.014)):
            #if lep.cutBased >= 1:
                is_fakeable_id = True
                n_fakeable_leptons += 1

            # tight electron
            if lep.mvaFall17V2Iso_WP80 and lep.tightCharge == 2:
                # if leptons[i][0].cutBased > 3 and leptons[i][0].tightCharge == 2:
                is_tight_id = True
                n_tight_leptons += 1

        # if this electron is just loose, then drop this event
        if is_fakeable_id or is_tight_id:
            store = True
        else:
            store = False

        return store, is_fakeable_id, is_tight_id, n_fakeable_leptons, n_tight_leptons

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        # refer to: https://github.com/cms-nanoAOD/nanoAOD-tools/blob/b20be01e2087412051abb5d5b59d0a3d07835207/python/postprocessing/modules/common/collectionMerger.py#L56-L60
        # merge Electron and Muon to Lepton
        input = ["Electron", "Muon"]
        coll = [Collection(event, x) for x in input]
        leptons = [(coll[j][i], j, i) for j in xrange(len(input)) for i in xrange(len(coll[j]))]
        if self.selector: leptons = filter(lambda (obj, j, i): self.selector[j](obj), leptons)
        leptons.sort(key=self.sortkey, reverse=self.reverse)
        # electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        taus = Collection(event, "Tau")

        if hasattr(event, 'nGenPart'):
            genparts = Collection(event, "GenPart")

        # if hasattr(event, 'nLHEPart'):
        #     lheparts = Collection(event, "LHEPart")

        loose_leptons = []

        is_fakeable = []
        is_tight = []

        loose_jets = []

        n_fakeable_leptons = 0
        n_tight_leptons = 0

        if len(leptons) < self.minObjects:
            return False
        for i in range(0, len(leptons)):
            # muon
            if abs(leptons[i][0].pdgId) == 13:
                if leptons[i][0].pt < 10:
                    continue
                if abs(leptons[i][0].eta) > 2.4:
                    continue
                store, is_fakeable_id, is_tight_id, n_fakeable_leptons, n_tight_leptons = self.muonID(leptons[i][0], n_fakeable_leptons, n_tight_leptons)
                if store:
                    is_fakeable.append(is_fakeable_id)
                    is_tight.append(is_tight_id)
                    loose_leptons.append(i)
                    if len(loose_leptons) > self.maxObjects:
                        return False
                else:
                    continue

            # electron
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
                    store, is_fakeable_id, is_tight_id, n_fakeable_leptons, n_tight_leptons = self.electronID(leptons[i][0], n_fakeable_leptons, n_tight_leptons)
                    if store:
                        is_fakeable.append(is_fakeable_id)
                        is_tight.append(is_tight_id)
                        loose_leptons.append(i)
                        if len(loose_leptons) > self.maxObjects:
                            return False
                    # if is_loose_id is true, there will be additional loose leptons, so this event will be dropped
                    elif is_loose_id:
                        return False
                    # if is_loose_id is false, just skip this lepton
                    else:
                        continue

        if len(loose_leptons) > self.maxObjects or len(loose_leptons) < self.minObjects:
            return False

        if self.preSel and len(loose_leptons) > 1:
            if leptons[0][0].pt < 20 or leptons[1][0].pt < 15:
                return False

        # tau veto
        #tauVeto = True
        tauTagVVVLooseVSe = False
        tauTagVVLooseVSe = False
        tauTagVLooseVSe = False
        tauTagLooseVSe = False
        tauTagMediumVSe = False
        tauTagTightVSe = False
        tauTagVTightVSe = False
        tauTagVVTightVSe = False

        tauTagVVVLooseVSjet = False
        tauTagVVLooseVSjet = False
        tauTagVLooseVSjet = False
        tauTagLooseVSjet = False
        tauTagMediumVSjet = False
        tauTagTightVSjet = False
        tauTagVTightVSjet = False
        tauTagVVTightVSjet = False

        tauTagVLooseVSmu = False
        tauTagLooseVSmu = False
        tauTagMediumVSmu = False
        tauTagTightVSmu = False

        dr_flag = True
        for i in range(0, len(taus)):
            # if taus[i].pt > 18 and abs(taus[i].eta) < 2.3 and taus[i].idDecayMode and taus[i].idDecayModeNewDMs and taus[i].rawIso < 5:
            if taus[i].pt > 20 and abs(taus[i].eta) < 2.3 and taus[i].idDecayModeNewDMs:
                for j in range(0, len(loose_leptons)):
                    if not (deltaR(leptons[loose_leptons[j]][0].eta, leptons[loose_leptons[j]][0].phi, taus[i].eta, taus[i].phi) > 0.4):
                        dr_flag=False
                        break
                if dr_flag:
                    if taus[i].idDeepTau2017v2p1VSe >> 0 & 1:
                        tauTagVVVLooseVSe = True
                    if taus[i].idDeepTau2017v2p1VSe >> 1 & 1:
                        tauTagVVLooseVSe = True
                    if taus[i].idDeepTau2017v2p1VSe >> 2 & 1:
                        tauTagVLooseVSe = True
                    if taus[i].idDeepTau2017v2p1VSe >> 3 & 1:
                        tauTagLooseVSe = True
                    if taus[i].idDeepTau2017v2p1VSe >> 4 & 1:
                        tauTagMediumVSe = True
                    if taus[i].idDeepTau2017v2p1VSe >> 5 & 1:
                        tauTagTightVSe = True
                    if taus[i].idDeepTau2017v2p1VSe >> 6 & 1:
                        tauTagVTightVSe = True
                    if taus[i].idDeepTau2017v2p1VSe >> 7 & 1:
                        tauTagVVTightVSe = True

                    if taus[i].idDeepTau2017v2p1VSjet >> 0 & 1:
                        tauTagVVVLooseVSjet = True
                    if taus[i].idDeepTau2017v2p1VSjet >> 1 & 1:
                        tauTagVVLooseVSjet = True
                    if taus[i].idDeepTau2017v2p1VSjet >> 2 & 1:
                        tauTagVLooseVSjet = True
                    if taus[i].idDeepTau2017v2p1VSjet >> 3 & 1:
                        tauTagLooseVSjet = True
                    if taus[i].idDeepTau2017v2p1VSjet >> 4 & 1:
                        tauTagMediumVSjet = True
                    if taus[i].idDeepTau2017v2p1VSjet >> 5 & 1:
                        tauTagTightVSjet = True
                    if taus[i].idDeepTau2017v2p1VSjet >> 6 & 1:
                        tauTagVTightVSjet = True
                    if taus[i].idDeepTau2017v2p1VSjet >> 7 & 1:
                        tauTagVVTightVSjet = True

                    if taus[i].idDeepTau2017v2p1VSmu >> 0 & 1:
                        tauTagVLooseVSmu = True
                    if taus[i].idDeepTau2017v2p1VSmu >> 1 & 1:
                        tauTagLooseVSmu = True
                    if taus[i].idDeepTau2017v2p1VSmu >> 2 & 1:
                        tauTagMediumVSmu = True
                    if taus[i].idDeepTau2017v2p1VSmu >> 3 & 1:
                        tauTagTightVSmu = True

        #soft muon tag
        softmuonTag=False
        dr_flag = True
        for i in range(0, len(muons)):
            # if taus[i].pt > 18 and abs(taus[i].eta) < 2.3 and taus[i].idDecayMode and taus[i].idDecayModeNewDMs and taus[i].rawIso < 5:
            if abs(muons[i].dxy) < 0.02 and abs(muons[i].dz) < 0.1 and muons[i].softId and muons[i].pt>5:
                for j in range(0, len(loose_leptons)):
                    dr_flag*=(deltaR(leptons[loose_leptons[j]][0].eta, leptons[loose_leptons[j]][0].phi, muons[i].eta, muons[i].phi) > 0.4)
                if dr_flag:
                    softmuonTag = True


        # jets
        # if jet multiplicity is needed, then remove below cut
        #if len(jets) < 2:
        #    return False
        for i in range(0, len(jets)):
            if jets[i].pt < 20: # for btag the jets pt just need to > 20
                continue

            if abs(jets[i].eta) > 4.7:
                continue

            # clean from identified leptons
            is_clean_jet=True
            for ilep in loose_leptons:
                #if (is_fakeable[j] or is_tight[j]) and deltaR(leptons[loose_leptons[j]][0].eta, leptons[loose_leptons[j]][0].phi, jets[i].eta, jets[i].phi) < 0.4:
                if deltaR(leptons[ilep][0].eta, leptons[ilep][0].phi, jets[i].eta, jets[i].phi) < 0.4:
                    is_clean_jet=False
                    break

            # actually jet related lepton maybe not loose
            if is_clean_jet:
                loose_jets.append(i)

        # btag: discriminator value just for 2016
        btagCSVV2Loose = False
        btagCSVV2Medium = False
        btagCSVV2Tight = False

        btagDeepBLoose = False
        btagDeepBMedium = False
        btagDeepBTight = False

        for ijet in loose_jets:
            if (jets[ijet].pt>20 and abs(jets[ijet].eta)<2.4):
                if jets[ijet].btagCSVV2 > 0.5426:
                    btagCSVV2Loose = True
                if jets[ijet].btagCSVV2 > 0.8484:
                    btagCSVV2Medium = True
                if jets[ijet].btagCSVV2 > 0.9535:
                    btagCSVV2Tight = True

                if jets[ijet].btagDeepB > 0.2219:
                    btagDeepBLoose = True
                if jets[ijet].btagDeepB > 0.6324:
                    btagDeepBMedium = True
                if jets[ijet].btagDeepB > 0.8958:
                    btagDeepBTight = True

        # if jet multiplicity is needed, then remove below cut
        '''
        if self.preSel:
            if len(loose_jets) < 2:
                return False
            elif jets[loose_jets[1]].pt<30:
                return False
        '''

        # decide whether lepton real
        #isprompt_mask = (0 << 0)  # isPrompt
        #isdirectprompttaudecayproduct_mask = (1 << 5)  # isDirectPromptTauDecayProduct

        lepton_idx = []
        lepton_pdgId = []
        lepton_tight = []
        lepton_fakeable = []
        lepton_pt = []
        lepton_phi = []
        lepton_eta = []
        lepton_mass = []
        lepton_real = []
        lepton_mishits = []
        lepton_tkIsoId = []
        lepton_softmu = []
        lepton_zep = []
        if len(loose_jets) < 2:
            detajj=-9999.
            mjj=-9999.
        else:
            detajj = jets[loose_jets[0]].eta - jets[loose_jets[1]].eta
            mjj = (jets[loose_jets[0]].p4() + jets[loose_jets[1]].p4()).M()
        #if self.preSel:
        #    if mjj < 500:
        #        return False

        # store leptons information
        # loose leptons
        for i in range(0, len(loose_leptons)):
            if i >= self.maxObjects:
                break
            lepton_idx.append(loose_leptons[i])
            if abs(leptons[loose_leptons[i]][0].pdgId) == 13:
                PID = 13
                lepton_tkIsoId.append(leptons[loose_leptons[i]][0].tkIsoId)
                lepton_softmu.append(leptons[loose_leptons[i]][0].softId)
                lepton_mishits.append(-9999)
            elif abs(leptons[loose_leptons[i]][0].pdgId) == 11:
                PID = 11
                lepton_tkIsoId.append(-9999)
                lepton_softmu.append(False)
                lepton_mishits.append(leptons[loose_leptons[i]][0].lostHits)

            lepton_pdgId.append(leptons[loose_leptons[i]][0].pdgId)
            lepton_tight.append(is_tight[i])
            lepton_fakeable.append(is_fakeable[i])
            lepton_pt.append(leptons[loose_leptons[i]][0].pt)
            lepton_phi.append(leptons[loose_leptons[i]][0].phi)
            lepton_eta.append(leptons[loose_leptons[i]][0].eta)
            lepton_mass.append(leptons[loose_leptons[i]][0].mass)
            try:
                lepton_zep.append(abs((leptons[loose_leptons[i]][0].eta - (jets[loose_jets[0]].eta + jets[loose_jets[1]].eta) / 2.) / detajj))
            except:
                lepton_zep.append(-9999.)
            else:
                pass

            lepton_real_flag=False
            try:
                for j in range(0, len(genparts)):
                    if genparts[j].pt > 5 and abs(genparts[j].pdgId) == PID and ((genparts[j].statusFlags >> 0 & 1) or (genparts[j].statusFlags >> 5 & 1)) and deltaR(leptons[loose_leptons[i]][0].eta, leptons[loose_leptons[i]][0].phi, genparts[j].eta, genparts[j].phi) < 0.3:
                        lepton_real_flag=True
                        break
                lepton_real.append(lepton_real_flag)
            except:
                lepton_real.append(lepton_real_flag)
            else:
                pass

        # store jets information
        jet_idx = []
        jet_jetId = []
        jet_puId = []
        jet_pt = []
        jet_eta = []
        jet_phi = []
        jet_mass = []
        jet_btagCSVV2 = []
        jet_btagDeepB = []
        jet_hadronFlavour = []
        jet_partonFlavour = []
        for i in range(0, len(loose_jets)):
            jet_idx.append(loose_jets[i])
            jet_jetId.append(jets[loose_jets[i]].jetId)
            jet_puId.append(jets[loose_jets[i]].puId)
            jet_pt.append(jets[loose_jets[i]].pt)
            jet_eta.append(jets[loose_jets[i]].eta)
            jet_phi.append(jets[loose_jets[i]].phi)
            jet_mass.append(jets[loose_jets[i]].mass)
            jet_btagCSVV2.append(jets[loose_jets[i]].btagCSVV2)
            jet_btagDeepB.append(jets[loose_jets[i]].btagDeepB)
            if hasattr(jets[loose_jets[i]], 'hadronFlavour'):
                jet_hadronFlavour.append(jets[loose_jets[i]].hadronFlavour)
            else:
                jet_hadronFlavour.append(-9999)

            if hasattr(jets[loose_jets[i]], 'partonFlavour'):
                jet_partonFlavour.append(jets[loose_jets[i]].partonFlavour)
            else:
                jet_partonFlavour.append(-9999)

        self.out.fillBranch("run", event.run)
        self.out.fillBranch("lumi", event.luminosityBlock)
        self.out.fillBranch("event", event.event)

        if hasattr(event, 'Pileup_nPU'):
            self.out.fillBranch("npu", event.Pileup_nPU)
        else:
            self.out.fillBranch("npu", 0)

        if hasattr(event, 'Pileup_nTrueInt'):
            self.out.fillBranch("ntruepu", event.Pileup_nTrueInt)
        else:
            self.out.fillBranch("ntruepu", 0)

        self.out.fillBranch("npvs", event.PV_npvs)

        if hasattr(event, 'Generator_weight'):
            self.out.fillBranch("gen_weight", event.Generator_weight)
        else:
            self.out.fillBranch("gen_weight", 0)

        #self.out.fillBranch("tauTag", tauTag)
        self.out.fillBranch("tauTagVVVLooseVSe", tauTagVVVLooseVSe)
        self.out.fillBranch("tauTagVVLooseVSe", tauTagVVLooseVSe)
        self.out.fillBranch("tauTagVLooseVSe", tauTagVLooseVSe)
        self.out.fillBranch("tauTagLooseVSe", tauTagLooseVSe)
        self.out.fillBranch("tauTagMediumVSe", tauTagMediumVSe)
        self.out.fillBranch("tauTagTightVSe", tauTagTightVSe)
        self.out.fillBranch("tauTagVTightVSe", tauTagVTightVSe)
        self.out.fillBranch("tauTagVVTightVSe", tauTagVVTightVSe)

        self.out.fillBranch("tauTagVVVLooseVSjet", tauTagVVVLooseVSjet)
        self.out.fillBranch("tauTagVVLooseVSjet", tauTagVVLooseVSjet)
        self.out.fillBranch("tauTagVLooseVSjet", tauTagVLooseVSjet)
        self.out.fillBranch("tauTagLooseVSjet", tauTagLooseVSjet)
        self.out.fillBranch("tauTagMediumVSjet", tauTagMediumVSjet)
        self.out.fillBranch("tauTagTightVSjet", tauTagTightVSjet)
        self.out.fillBranch("tauTagVTightVSjet", tauTagVTightVSjet)
        self.out.fillBranch("tauTagVVTightVSjet", tauTagVVTightVSjet)

        self.out.fillBranch("tauTagVLooseVSmu", tauTagVLooseVSmu)
        self.out.fillBranch("tauTagLooseVSmu", tauTagLooseVSmu)
        self.out.fillBranch("tauTagMediumVSmu", tauTagMediumVSmu)
        self.out.fillBranch("tauTagTightVSmu", tauTagTightVSmu)

        self.out.fillBranch("softmuonTag", softmuonTag)
        self.out.fillBranch("n_tight_leptons", n_tight_leptons)
        self.out.fillBranch("n_fakeable_leptons", n_fakeable_leptons)
        self.out.fillBranch("lepton_idx", lepton_idx)
        self.out.fillBranch("lepton_pdgId", lepton_pdgId)
        self.out.fillBranch("lepton_tight", lepton_tight)
        self.out.fillBranch("lepton_fakeable", lepton_fakeable)
        self.out.fillBranch("lepton_pt", lepton_pt)
        self.out.fillBranch("lepton_eta", lepton_eta)
        self.out.fillBranch("lepton_phi", lepton_phi)
        self.out.fillBranch("lepton_mass", lepton_mass)
        self.out.fillBranch("lepton_real", lepton_real)
        self.out.fillBranch("lepton_mishits", lepton_mishits)
        self.out.fillBranch("lepton_tkIsoId", lepton_tkIsoId)
        self.out.fillBranch("lepton_softmu", lepton_softmu)
        self.out.fillBranch("lepton_zep", lepton_zep)
        mll = -9999.
        if len(loose_leptons) > 1:
            mll = (leptons[loose_leptons[0]][0].p4() + leptons[loose_leptons[1]][0].p4()).M()
        self.out.fillBranch("mll", mll)
        '''
        mll02 = -9999.
        mll12 = -9999.
        mlll = -9999.
        if len(loose_leptons) > 2:
            mll02 = (leptons[loose_leptons[0]][0].p4() + leptons[loose_leptons[2]][0].p4()).M()
            mll12 = (leptons[loose_leptons[1]][0].p4() + leptons[loose_leptons[2]][0].p4()).M()
            mlll = (leptons[loose_leptons[0]][0].p4() + leptons[loose_leptons[1]][0].p4() + leptons[loose_leptons[2]][0].p4()).M()
        self.out.fillBranch("mll02", mll02)
        self.out.fillBranch("mll12", mll12)
        self.out.fillBranch("mlll", mlll)
        mll_z0 = -9999.
        mll_z1 = -9999.
        mllll = -9999.
        tmp2 = -9999.
        if len(loose_leptons) > 3:
            for i in range(1, len(loose_leptons)):
                tmp = (leptons[loose_leptons[0]][0].p4() + leptons[loose_leptons[i]][0].p4()).M() - 91.1876
                if abs(tmp) < abs(tmp2):
                    mll_z0 = (leptons[loose_leptons[0]][0].p4() + leptons[loose_leptons[i]][0].p4()).M()
                    tmp2 = tmp
                    remain_lepton = [1, 2, 3]
                    remain_lepton.remove(i)
                    mll_z1 = (leptons[loose_leptons[remain_lepton[0]]][0].p4() + leptons[loose_leptons[remain_lepton[1]]][0].p4()).M()
            mllll = (leptons[loose_leptons[0]][0].p4() + leptons[loose_leptons[1]][0].p4() + leptons[loose_leptons[2]][0].p4() + leptons[loose_leptons[3]][0].p4()).M()
        self.out.fillBranch("mll_z0", mll_z0)
        self.out.fillBranch("mll_z1", mll_z1)
        self.out.fillBranch("mllll", mllll)
        '''
        self.out.fillBranch("detajj", detajj)
        self.out.fillBranch("jet_idx", jet_idx)
        self.out.fillBranch("jet_jetId", jet_jetId)
        self.out.fillBranch("jet_puId", jet_puId)
        self.out.fillBranch("jet_pt", jet_pt)
        self.out.fillBranch("jet_eta", jet_eta)
        self.out.fillBranch("jet_phi", jet_phi)
        self.out.fillBranch("jet_mass", jet_mass)
        self.out.fillBranch("jet_btagCSVV2", jet_btagCSVV2)
        self.out.fillBranch("jet_btagDeepB", jet_btagDeepB)
        self.out.fillBranch("jet_hadronFlavour", jet_hadronFlavour)
        self.out.fillBranch("jet_partonFlavour", jet_partonFlavour)

        self.out.fillBranch("btagCSVV2Loose", btagCSVV2Loose)
        self.out.fillBranch("btagCSVV2Medium", btagCSVV2Medium)
        self.out.fillBranch("btagCSVV2Tight", btagCSVV2Tight)

        self.out.fillBranch("btagDeepBLoose", btagDeepBLoose)
        self.out.fillBranch("btagDeepBMedium", btagDeepBMedium)
        self.out.fillBranch("btagDeepBTight", btagDeepBTight)

        self.out.fillBranch("mjj", mjj)
        return True


sswwModule2016 = lambda: sswwProducer(minObjects=2, maxObjects=4, preSel=True, year='2016')
sswwModule2017 = lambda: sswwProducer(minObjects=2, maxObjects=4, preSel=True, year='2017')
sswwModule2018 = lambda: sswwProducer(minObjects=2, maxObjects=4, preSel=True, year='2018')

#python scripts/nano_postproc.py . /afs/cern.ch/work/j/jixiao/nano/2016/CMSSW_10_2_13/src/PhysicsTools/NanoAODTools/2016_DY_nanoAODv5.root -I PhysicsTools.NanoAODTools.postprocessing.modules.ssww.sswwModule_copy sswwModule2016 --bi python/postprocessing/scripts/ssww_keep_and_drop_2016.txt --bo python/postprocessing/scripts/ssww_output_branch_selection_2016.txt