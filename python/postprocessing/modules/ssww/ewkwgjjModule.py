import ROOT

from math import cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi

class exampleProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("run",  "i");
        self.out.branch("lumi",  "i");
        self.out.branch("event",  "l");
        self.out.branch("npu",  "I");
        self.out.branch("ntruepu",  "F");
        self.out.branch("lepton_pdg_id",  "I",lenVar="nlepton");
        self.out.branch("lepton_pt",  "F",lenVar="nlepton");
        self.out.branch("lepton_phi",  "F",lenVar="nlepton");
        self.out.branch("lepton_eta",  "F",lenVar="nlepton");
        self.out.branch("lepton_mass",  "F",lenVar="nlepton");
        self.out.branch("lepton_tight",  "B",lenVar="nlepton");
        self.out.branch("lepton_real",  "B",lenVar="nlepton");
        self.out.branch("photon_pt",  "F",lenVar="nphoton");
        self.out.branch("photon_phi",  "F",lenVar="nphoton");
        self.out.branch("photon_eta",  "F",lenVar="nphoton");
        self.out.branch("photon_mass",  "F",lenVar="nphoton");
        self.out.branch("photon_selection",  "I",lenVar="nphoton");
        self.out.branch("photon_gen_matching",  "I",lenVar="nphoton");
        self.out.branch("mlg",  "F");
        self.out.branch("btagging_selection",  "I");
        self.out.branch("met",  "F");
        self.out.branch("met_phi",  "F");
        self.out.branch("mt",  "F");
        self.out.branch("mjj","F")
        self.out.branch("npvs","I")
        self.out.branch("njets","I")
        self.out.branch("jet_idx", "I", lenVar="njet")
        self.out.branch("jet_id", "I", lenVar="njet")
        self.out.branch("jet_pt", "F", lenVar="njet")
        self.out.branch("jet_eta", "F", lenVar="njet")
        self.out.branch("jet_phi", "F", lenVar="njet")
        self.out.branch("jet_mass", "F", lenVar="njet")
        self.out.branch("jet_btagCSVV2", "F", lenVar="njet")
        self.out.branch("jet_btagDeepB", "F", lenVar="njet")
        self.out.branch("jet_hadronFlavour", "I", lenVar="njet")
        self.out.branch("jet_partonFlavour", "I", lenVar="njet")
        self.out.branch("gen_weight",  "F");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        photons = Collection(event, "Photon")

        try:

            genparts = Collection(event, "GenPart")
        except:
            pass

        tight_muons = []

        loose_but_not_tight_muons = []
        
        tight_electrons = []

        loose_but_not_tight_electrons = []
        
        tight_photons = []

        tight_jets = []

        for i in range(0,len(muons)):

            if muons[i].pt < 20:
                continue

            if abs(muons[i].eta) > 2.4:
                continue

            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)
            elif muons[i].pfRelIso04_all < 0.4:
                loose_but_not_tight_muons.append(i)

        for i in range (0,len(electrons)):

            if electrons[i].pt/electrons[i].eCorr < 20:
                continue
            
            if abs(electrons[i].eta + electrons[i].deltaEtaSC) > 2.5:
                continue

            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                if electrons[i].cutBased >= 3:
                    tight_electrons.append(i)

                elif electrons[i].cutBased >= 1:
                    loose_but_not_tight_electrons.append(i)

        for i in range (0,len(photons)):

            if photons[i].pt/photons[i].eCorr < 20:
                continue

            #if not ((abs(photons[i].eta) < 1.4442) or (1.566 < abs(photons[i].eta) and abs(photons[i].eta) < 2.5) ):
            if not ((abs(photons[i].eta) < 1.4442) or (1.566 < abs(photons[i].eta) and abs(photons[i].eta) < 2.5) ):
                continue

            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) 
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[i].vidNestedWPBitmap & mask1

            #first add the photons that pass the full ID
            if not (bitmap == mask1):
                continue

            if not((bitmap == mask1) or (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4) or (bitmap == mask5)):
                continue

            #if photons[i].cutBased == 0 or photons[i].cutBased == 1:
            #    continue

#            if not photons[i].electronVeto:
#                continue

            if photons[i].pixelSeed:
                continue

            pass_lepton_dr_cut = True

            for j in range(0,len(tight_muons)):
                if deltaR(muons[tight_muons[j]].eta,muons[tight_muons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False

            for j in range(0,len(tight_electrons)):

                if deltaR(electrons[tight_electrons[j]].eta,electrons[tight_electrons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False

            if not pass_lepton_dr_cut:
                continue

            tight_photons.append(i)

        for i in range (0,len(photons)):


            if photons[i].pt/photons[i].eCorr < 20:
                continue

            #if not ((abs(photons[i].eta) < 1.4442) or (1.566 < abs(photons[i].eta) and abs(photons[i].eta) < 2.5) ):
            if not ((abs(photons[i].eta) < 1.4442) or (1.566 < abs(photons[i].eta) and abs(photons[i].eta) < 2.5) ):
                continue

            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) 
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[i].vidNestedWPBitmap & mask1

            #after adding the photons that pass the full ID, add the photons that pass the inverted ID
            if (bitmap == mask1):
                continue

            if not((bitmap == mask1) or (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4) or (bitmap == mask5)):
                continue

            #if photons[i].cutBased == 0 or photons[i].cutBased == 1:
            #    continue

#            if not photons[i].electronVeto:
#                continue
            
            if photons[i].pixelSeed:
                continue

            pass_lepton_dr_cut = True

            for j in range(0,len(tight_muons)):
                if deltaR(muons[tight_muons[j]].eta,muons[tight_muons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False

            for j in range(0,len(tight_electrons)):
                if deltaR(electrons[tight_electrons[j]].eta,electrons[tight_electrons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False

            if not pass_lepton_dr_cut:
                continue

            tight_photons.append(i)

        if len(tight_photons) == 0:
            return False

        njets = 0

        for i in range(0,len(jets)):

            if jets[i].pt < 30:
                continue

            if abs(jets[i].eta) > 4.7:
                continue

            if not jets[i].jetId & (1 << 0):
                continue

            njets+=1

        for i in range(0,len(jets)):

            if jets[i].pt < 30:
                continue

            if abs(jets[i].eta) > 4.7:
                continue

            if not jets[i].jetId & (1 << 0):
                continue

            #pass_photon_dr_cut = True

            #for j in range(0,len(tight_photons)):

            #    print "deltaR(photons[tight_photons[j]].eta,photons[tight_photons[j]].phi,jets[i].eta,jets[i].phi) = " + str(deltaR(photons[tight_photons[j]].eta,photons[tight_photons[j]].phi,jets[i].eta,jets[i].phi))
                
            #    if deltaR(photons[tight_photons[j]].eta,photons[tight_photons[j]].phi,jets[i].eta,jets[i].phi) < 0.5:
            #        pass_photon_dr_cut = False

            #if not pass_photon_dr_cut:
            #    continue

            if deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,jets[i].eta,jets[i].phi) < 0.5:
                continue

            pass_lepton_dr_cut = True

            for j in range(0,len(tight_muons)):

                if deltaR(muons[tight_muons[j]].eta,muons[tight_muons[j]].phi,jets[i].eta,jets[i].phi) < 0.5:
                    pass_lepton_dr_cut = False

            for j in range(0,len(tight_electrons)):
                
                if deltaR(electrons[tight_electrons[j]].eta,electrons[tight_electrons[j]].phi,jets[i].eta,jets[i].phi) < 0.5:

                    pass_lepton_dr_cut = False

            for j in range(0,len(loose_but_not_tight_muons)):

                if deltaR(muons[loose_but_not_tight_muons[j]].eta,muons[loose_but_not_tight_muons[j]].phi,jets[i].eta,jets[i].phi) < 0.5:

                    pass_lepton_dr_cut = False

            for j in range(0,len(loose_but_not_tight_electrons)):

                if deltaR(electrons[loose_but_not_tight_electrons[j]].eta,electrons[loose_but_not_tight_electrons[j]].phi,jets[i].eta,jets[i].phi) < 0.5:

                     pass_lepton_dr_cut = False

            if not pass_lepton_dr_cut:
                continue

            tight_jets.append(i)

        if len(tight_jets) < 2:
            return False

        if jets[tight_jets[0]].btagCSVV2 < 0.8484 and jets[tight_jets[1]].btagCSVV2 < 0.8484:
            self.out.fillBranch("btagging_selection",1)
        else:   
            self.out.fillBranch("btagging_selection",0)            

        if jets[tight_jets[0]].pt < 40:
            return False

        if jets[tight_jets[1]].pt < 30:
            return False

        if abs(jets[tight_jets[0]].eta) > 4.7:
            return False

        if abs(jets[tight_jets[1]].eta) > 4.7:
            return False

        if (jets[tight_jets[0]].p4() + jets[tight_jets[1]].p4()).M() < 200:
            return False

        #if abs(jets[0].p4().Eta() - jets[1].p4().Eta()) < 2.5:
        #    return False

        if photons[tight_photons[0]].pt/photons[tight_photons[0]].eCorr < 20:
            return False

        #if not (abs(photons[tight_photons[0]].eta) < 1.4442):
        #if not (abs(photons[tight_photons[0]].eta) < 1.4442):
        #    return False        

        if not ((abs(photons[tight_photons[0]].eta) < 1.4442) or (1.566 < abs(photons[tight_photons[0]].eta) and abs(photons[tight_photons[0]].eta) < 2.5) ):
            return False        

        if deltaR(photons[tight_photons[0]].eta , photons[tight_photons[0]].phi,jets[tight_jets[0]].eta,jets[tight_jets[0]].phi) < 0.5:
            return False

        if deltaR(photons[tight_photons[0]].eta , photons[tight_photons[0]].phi,jets[tight_jets[1]].eta,jets[tight_jets[1]].phi) < 0.5:
            return False

        if deltaR(jets[tight_jets[0]].eta , jets[tight_jets[0]].phi,jets[tight_jets[1]].eta,jets[tight_jets[1]].phi) < 0.5:
            return False

        #if photons[tight_photons[0]].cutBased == 0 or photons[tight_photons[0]].cutBased == 1:
        #    return False

#        if not photons[tight_photons[0]].electronVeto:
#            return False

        if photons[tight_photons[0]].pixelSeed:
            return False

        #if event.MET_pt < 35:
        #    return False

        if abs(deltaPhi(event.MET_phi,jets[tight_jets[0]].phi)) < 0.4:
            return False

        if abs(deltaPhi(event.MET_phi,jets[tight_jets[1]].phi)) < 0.4:
            return False

        if len(tight_muons) + len(loose_but_not_tight_muons) +  len(tight_electrons) + len(loose_but_not_tight_electrons) > 1:
            return False

        isprompt_mask = (1 << 0) #isPrompt
        isprompttaudecayproduct_mask = (1 << 4) #isPromptTauDecayProduct


        lepton_real=0


        if len(tight_muons) == 1:

            try:

                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 13 and ((genparts[i].statusFlags == 0) or (genparts[i].statusFlags == 3)) and deltaR(muons[tight_muons[0]].eta,muons[tight_muons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        lepton_real=1
            except:
                pass

            if not (event.HLT_IsoMu24 or event.HLT_IsoTkMu24):
                return False
        
            if deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,muons[tight_muons[0]].eta,muons[tight_muons[0]].phi) < 0.5:
                return False

            if muons[tight_muons[0]].pt < 25:
                return False

            if abs(muons[tight_muons[0]].eta) > 2.4:
                return False

            if muons[tight_muons[0]].pfRelIso04_all > 0.15:
                return False

            if not muons[tight_muons[0]].tightId:
                return False

            #if sqrt(2*muons[tight_muons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[tight_muons[0]].phi))) < 30:
            #    return False

            self.out.fillBranch("mt",sqrt(2*muons[tight_muons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[tight_muons[0]].phi))))

            #print "selected muon event: " + str(event.event) + " " + str(event.luminosityBlock) + " " + str(event.run)
            
            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) 
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the medium photon ID with the sigma_ietaieta cut removed

            _photon_pt=[]
            _photon_phi=[]
            _photon_eta=[]
            _photon_mass=[]
            _photon_selection=[]
            bitmap = photons[tight_photons[0]].vidNestedWPBitmap & mask1
            if (bitmap == mask1):
                _photon_selection.append(int(2))
                self.out.fillBranch("photon_selection",_photon_selection)
            elif (bitmap == mask5):
                _photon_selection.append(int(1))
                self.out.fillBranch("photon_selection",_photon_selection)
            elif (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4):
                _photon_selection.append(int(0))
                self.out.fillBranch("photon_selection",_photon_selection)
            else:
                assert(0)

            _lepton_real=[]
            _lepton_pdg_id=[]
            _lepton_pt=[]
            _lepton_eta=[]
            _lepton_phi=[]
            _lepton_mass=[]
            _lepton_tight=[]

            _lepton_real.append(lepton_real)
            _lepton_pdg_id.append(muons[tight_muons[0]].pdgId)
            _lepton_pt.append(muons[tight_muons[0]].pt)
            _lepton_eta.append(muons[tight_muons[0]].eta)
            _lepton_phi.append(muons[tight_muons[0]].phi)
            _lepton_mass.append(muons[tight_muons[0]].mass)
            _lepton_tight.append(bool(1))
            _photon_pt.append(photons[tight_photons[0]].pt/photons[tight_photons[0]].eCorr)
            _photon_eta.append(photons[tight_photons[0]].eta)
            _photon_phi.append(photons[tight_photons[0]].phi)
            _photon_mass.append(photons[tight_photons[0]].mass)
            self.out.fillBranch("lepton_real",_lepton_real)
            self.out.fillBranch("lepton_pdg_id",_lepton_pdg_id)
            self.out.fillBranch("lepton_pt",_lepton_pt)
            self.out.fillBranch("lepton_eta",_lepton_eta)
            self.out.fillBranch("lepton_phi",_lepton_phi)
            self.out.fillBranch("lepton_mass",_lepton_mass)
            self.out.fillBranch("lepton_tight",_lepton_tight)
            self.out.fillBranch("met",event.MET_pt)
            self.out.fillBranch("met_phi",event.MET_phi)
            self.out.fillBranch("photon_pt",_photon_pt)
            self.out.fillBranch("photon_eta",_photon_eta)
            self.out.fillBranch("photon_phi",_photon_phi)
            self.out.fillBranch("photon_mass",_photon_mass)
            #self.out.fillBranch("mjj",(jets[tight_jets[0]].p4() + jets[tight_jets[1]].p4()).M())
            self.out.fillBranch("mlg",(muons[tight_muons[0]].p4() + photons[tight_photons[0]].p4()).M())

        elif len(loose_but_not_tight_muons) == 1:

            try:

                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 13 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct_mask == isprompttaudecayproduct_mask)) and deltaR(muons[loose_but_not_tight_muons[0]].eta,muons[loose_but_not_tight_muons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        lepton_real=1
            except:
                pass

            if not (event.HLT_IsoMu24 or event.HLT_IsoTkMu24):
                return False
        
            if deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,muons[loose_but_not_tight_muons[0]].eta,muons[loose_but_not_tight_muons[0]].phi) < 0.5:
                return False

            if muons[loose_but_not_tight_muons[0]].pt < 25:
                return False

            if abs(muons[loose_but_not_tight_muons[0]].eta) > 2.4:
                return False

            #if sqrt(2*muons[loose_but_not_tight_muons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[loose_but_not_tight_muons[0]].phi))) < 30:
            #    return False

            self.out.fillBranch("mt",sqrt(2*muons[loose_but_not_tight_muons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[loose_but_not_tight_muons[0]].phi))))

            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) 
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[tight_photons[0]].vidNestedWPBitmap & mask1

            _photon_pt=[]
            _photon_phi=[]
            _photon_eta=[]
            _photon_mass=[]
            _photon_selection=[]
            if (bitmap == mask1):
                _photon_selection.append(int(2))
                self.out.fillBranch("photon_selection",_photon_selection)
            elif (bitmap == mask5):
                _photon_selection.append(int(1))
                self.out.fillBranch("photon_selection",_photon_selection)
            elif (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4):
                _photon_selection.append(int(0))
                self.out.fillBranch("photon_selection",_photon_selection)
            else:
                assert(0)

            _lepton_real=[]
            _lepton_pdg_id=[]
            _lepton_pt=[]
            _lepton_eta=[]
            _lepton_phi=[]
            _lepton_mass=[]
            _lepton_tight=[]

            _lepton_real.append(lepton_real)
            _lepton_pdg_id.append(muons[tight_muons[0]].pdgId)
            _lepton_pt.append(muons[tight_muons[0]].pt)
            _lepton_eta.append(muons[tight_muons[0]].eta)
            _lepton_phi.append(muons[tight_muons[0]].phi)
            _lepton_mass.append(muons[tight_muons[0]].mass)
            _lepton_tight.append(bool(0))
            _photon_pt.append(photons[tight_photons[0]].pt/photons[tight_photons[0]].eCorr)
            _photon_eta.append(photons[tight_photons[0]].eta)
            _photon_phi.append(photons[tight_photons[0]].phi)
            _photon_mass.append(photons[tight_photons[0]].mass)
            self.out.fillBranch("lepton_real",_lepton_real)
            self.out.fillBranch("lepton_pdg_id",_lepton_pdg_id)
            self.out.fillBranch("lepton_pt",_lepton_pt)
            self.out.fillBranch("lepton_eta",_lepton_eta)
            self.out.fillBranch("lepton_phi",_lepton_phi)
            self.out.fillBranch("lepton_mass",_lepton_mass)
            self.out.fillBranch("lepton_tight",_lepton_tight)
            self.out.fillBranch("met",event.MET_pt)
            self.out.fillBranch("met_phi",event.MET_phi)
            self.out.fillBranch("photon_pt",_photon_pt)
            self.out.fillBranch("photon_eta",_photon_eta)
            self.out.fillBranch("photon_phi",_photon_phi)
            self.out.fillBranch("photon_mass",_photon_mass)
            #self.out.fillBranch("mjj",(jets[tight_jets[0]].p4() + jets[tight_jets[1]].p4()).M())
            self.out.fillBranch("mlg",(muons[loose_but_not_tight_muons[0]].p4() + photons[tight_photons[0]].p4()).M())

        elif len(tight_electrons) == 1:

            try:

                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 11 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct_mask == isprompttaudecayproduct_mask)) and deltaR(electrons[tight_electrons[0]].eta,electrons[tight_electrons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        lepton_real=1
            except:
                pass

            if not event.HLT_Ele27_WPTight_Gsf:
                return False

            if electrons[tight_electrons[0]].cutBased == 0 or electrons[tight_electrons[0]].cutBased == 1:
                return False

            if deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,electrons[tight_electrons[0]].eta,electrons[tight_electrons[0]].phi) < 0.5:
                return False

            if electrons[tight_electrons[0]].pt/electrons[tight_electrons[0]].eCorr < 30:
                return False

            if abs(electrons[tight_electrons[0]].eta) > 2.5:
                return False

            ele_p4 = electrons[tight_electrons[0]].p4()

            pho_p4 = photons[tight_photons[0]].p4()

            ele_p4.SetPtEtaPhiM(ele_p4.Pt()/electrons[tight_electrons[0]].eCorr , ele_p4.Eta(), ele_p4.Phi() , ele_p4.M())

            pho_p4.SetPtEtaPhiM(pho_p4.Pt()/photons[tight_photons[0]].eCorr , pho_p4.Eta(), pho_p4.Phi() , pho_p4.M())

#            if (ele_p4 + pho_p4).M() > 81.2 and (ele_p4 + pho_p4).M() < 101.2:
#            if (ele_p4 + pho_p4).M() > 76.2 and (ele_p4 + pho_p4).M() < 106.2:
#                return False

            #if sqrt(2*electrons[tight_electrons[0]].pt/electrons[tight_electrons[0]].eCorr*event.MET_pt*(1 - cos(event.MET_phi - electrons[tight_electrons[0]].phi))) < 30:
            #    return False

            self.out.fillBranch("mt",sqrt(2*electrons[tight_electrons[0]].pt/electrons[tight_electrons[0]].eCorr*event.MET_pt*(1 - cos(event.MET_phi - electrons[tight_electrons[0]].phi))))

            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) 
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[tight_photons[0]].vidNestedWPBitmap & mask1

            _photon_pt=[]
            _photon_phi=[]
            _photon_eta=[]
            _photon_mass=[]
            _photon_selection=[]
            if (bitmap == mask1):
                _photon_selection.append(int(2))
                self.out.fillBranch("photon_selection",_photon_selection)
            elif (bitmap == mask5):
                _photon_selection.append(int(1))
                self.out.fillBranch("photon_selection",_photon_selection)
            elif (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4):
                _photon_selection.append(int(0))
                self.out.fillBranch("photon_selection",_photon_selection)
            else:
                assert(0)

            _lepton_real=[]
            _lepton_pdg_id=[]
            _lepton_pt=[]
            _lepton_eta=[]
            _lepton_phi=[]
            _lepton_mass=[]
            _lepton_tight=[]

            _lepton_real.append(lepton_real)
            _lepton_pdg_id.append(electrons[tight_electrons[0]].pdgId)
            _lepton_pt.append(electrons[tight_electrons[0]].pt)
            _lepton_eta.append(electrons[tight_electrons[0]].eta)
            _lepton_phi.append(electrons[tight_electrons[0]].phi)
            _lepton_mass.append(electrons[tight_electrons[0]].mass)
            _lepton_tight.append(bool(1))
            _photon_pt.append(photons[tight_photons[0]].pt/photons[tight_photons[0]].eCorr)
            _photon_eta.append(photons[tight_photons[0]].eta)
            _photon_phi.append(photons[tight_photons[0]].phi)
            _photon_mass.append(photons[tight_photons[0]].mass)

            self.out.fillBranch("lepton_real",_lepton_real)
            self.out.fillBranch("lepton_pdg_id",_lepton_pdg_id)
            self.out.fillBranch("lepton_pt",_lepton_pt)
            self.out.fillBranch("lepton_eta",_lepton_eta)
            self.out.fillBranch("lepton_phi",_lepton_phi)
            self.out.fillBranch("lepton_mass",_lepton_mass)
            self.out.fillBranch("lepton_tight",_lepton_tight)
            self.out.fillBranch("met",event.MET_pt)
            self.out.fillBranch("met_phi",event.MET_phi)
            self.out.fillBranch("photon_pt",_photon_pt)
            self.out.fillBranch("photon_eta",_photon_eta)
            self.out.fillBranch("photon_phi",_photon_phi)
            self.out.fillBranch("photon_mass",_photon_mass)
            #self.out.fillBranch("mjj",(jets[tight_jets[0]].p4() + jets[tight_jets[1]].p4()).M())
            self.out.fillBranch("mlg",(ele_p4 + pho_p4).M())

            print "selected electron event: " + str(event.event) + " " + str(event.luminosityBlock) + " " + str(event.run)

        elif len(loose_but_not_tight_electrons) == 1:

            try:

                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 11 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct_mask == isprompttaudecayproduct_mask)) and deltaR(electrons[loose_but_not_tight_electrons[0]].eta,electrons[loose_but_not_tight_electrons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        lepton_real=1

            except:

                pass
                        
            if not event.HLT_Ele27_WPTight_Gsf:
                return False

            if deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,electrons[loose_but_not_tight_electrons[0]].eta,electrons[loose_but_not_tight_electrons[0]].phi) < 0.5:
                return False

            if electrons[loose_but_not_tight_electrons[0]].pt/electrons[loose_but_not_tight_electrons[0]].eCorr < 30:
                return False

            if abs(electrons[loose_but_not_tight_electrons[0]].eta) > 2.5:
                return False

            ele_p4 = electrons[loose_but_not_tight_electrons[0]].p4()

            pho_p4 = photons[tight_photons[0]].p4()

            ele_p4.SetPtEtaPhiM(ele_p4.Pt()/electrons[loose_but_not_tight_electrons[0]].eCorr , ele_p4.Eta(), ele_p4.Phi() , ele_p4.M())

            pho_p4.SetPtEtaPhiM(pho_p4.Pt()/photons[tight_photons[0]].eCorr , pho_p4.Eta(), pho_p4.Phi() , pho_p4.M())

#            if (ele_p4 + pho_p4).M() > 81.2 and (ele_p4 + pho_p4).M() < 101.2:
#            if (ele_p4 + pho_p4).M() > 76.2 and (ele_p4 + pho_p4).M() < 106.2:
#                return False

            #if sqrt(2*electrons[loose_but_not_tight_electrons[0]].pt/electrons[loose_but_not_tight_electrons[0]].eCorr*event.MET_pt*(1 - cos(event.MET_phi - electrons[loose_but_not_tight_electrons[0]].phi))) < 30:
            #    return False

            self.out.fillBranch("mt",sqrt(2*electrons[loose_but_not_tight_electrons[0]].pt/electrons[loose_but_not_tight_electrons[0]].eCorr*event.MET_pt*(1 - cos(event.MET_phi - electrons[loose_but_not_tight_electrons[0]].phi))))                    

            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) 
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[tight_photons[0]].vidNestedWPBitmap & mask1

            _photon_pt=[]
            _photon_phi=[]
            _photon_eta=[]
            _photon_mass=[]
            _photon_selection=[]
            if (bitmap == mask1):
                _photon_selection.append(int(2))
                self.out.fillBranch("photon_selection",_photon_selection)
            elif (bitmap == mask5):
                _photon_selection.append(int(1))
                self.out.fillBranch("photon_selection",_photon_selection)
            elif (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4):
                _photon_selection.append(int(0))
                self.out.fillBranch("photon_selection",_photon_selection)
            else:
                assert(0)

            _lepton_real=[]
            _lepton_pdg_id=[]
            _lepton_pt=[]
            _lepton_eta=[]
            _lepton_phi=[]
            _lepton_mass=[]
            _lepton_tight=[]

            _lepton_real.append(lepton_real)
            _lepton_pdg_id.append(electrons[tight_electrons[0]].pdgId)
            _lepton_pt.append(electrons[tight_electrons[0]].pt)
            _lepton_eta.append(electrons[tight_electrons[0]].eta)
            _lepton_phi.append(electrons[tight_electrons[0]].phi)
            _lepton_mass.append(electrons[tight_electrons[0]].mass)
            _lepton_tight.append(bool(0))
            _photon_pt.append(photons[tight_photons[0]].pt/photons[tight_photons[0]].eCorr)
            _photon_eta.append(photons[tight_photons[0]].eta)
            _photon_phi.append(photons[tight_photons[0]].phi)
            _photon_mass.append(photons[tight_photons[0]].mass)

            self.out.fillBranch("lepton_real",_lepton_real)
            self.out.fillBranch("lepton_pdg_id",_lepton_pdg_id)
            self.out.fillBranch("lepton_pt",_lepton_pt)
            self.out.fillBranch("lepton_eta",_lepton_eta)
            self.out.fillBranch("lepton_phi",_lepton_phi)
            self.out.fillBranch("lepton_mass",_lepton_mass)
            self.out.fillBranch("lepton_tight",_lepton_tight)
            self.out.fillBranch("met",event.MET_pt)
            self.out.fillBranch("met_phi",event.MET_phi)
            self.out.fillBranch("photon_pt",_photon_pt)
            self.out.fillBranch("photon_eta",_photon_eta)
            self.out.fillBranch("photon_phi",_photon_phi)
            self.out.fillBranch("photon_mass",_photon_mass)
            #self.out.fillBranch("mjj",(jets[tight_jets[0]].p4() + jets[tight_jets[1]].p4()).M())
            self.out.fillBranch("mlg",(ele_p4 + pho_p4).M())

        else:
            return False


        #print event.event


        #self.out.fillBranch("EventMass",eventSum.M())
        #if eventSum.M() < 2000:
        #    return False
        #else:
        #    return True

        _photon_gen_matching=[]
        photon_gen_matching=0

        try:

            for i in range(0,len(genparts)):
                if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 13 and genparts[i].status == 1 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct_mask == isprompttaudecayproduct_mask)) and deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                    photon_gen_matching += 1
                    break

            for i in range(0,len(genparts)):
                if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 11 and genparts[i].status == 1 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct_mask == isprompttaudecayproduct_mask)) and deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                    photon_gen_matching += 2
                    break

            for i in range(0,len(genparts)):
                if genparts[i].pt > 5 and genparts[i].pdgId == 22 and genparts[i].status == 1 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct_mask == isprompttaudecayproduct_mask)) and deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:

                    if genparts[i].genPartIdxMother >= 0 and (abs(genparts[genparts[i].genPartIdxMother].pdgId) == 11 or abs(genparts[genparts[i].genPartIdxMother].pdgId) == 13 or abs(genparts[genparts[i].genPartIdxMother].pdgId) == 15):
                        photon_gen_matching += 8
                    else:
                        photon_gen_matching += 4                        
                    break

        except:
            pass
        _photon_gen_matching.append(photon_gen_matching)
        self.out.fillBranch("photon_gen_matching",_photon_gen_matching)

        try:

            self.out.fillBranch("gen_weight",event.Generator_weight)

        except:
            pass

        try:
            
            self.out.fillBranch("npu",event.Pileup_nPU)
            self.out.fillBranch("ntruepu",event.Pileup_nTrueInt)

        except:
            pass

        # store jets information
        jet_idx = []
        jet_id = []
        jet_pt = []
        jet_eta = []
        jet_phi = []
        jet_mass = []
        jet_btagCSVV2 = []
        jet_btagDeepB = []
        jet_hadronFlavour = []
        jet_partonFlavour = []
        for i in range(0, len(tight_jets)):
            jet_idx.append(tight_jets[i])
            jet_id.append(jets[tight_jets[i]].jetId)
            jet_pt.append(jets[tight_jets[i]].pt)
            jet_eta.append(jets[tight_jets[i]].eta)
            jet_phi.append(jets[tight_jets[i]].phi)
            jet_mass.append(jets[tight_jets[i]].mass)
            jet_btagCSVV2.append(jets[tight_jets[i]].btagCSVV2)
            jet_btagDeepB.append(jets[tight_jets[i]].btagDeepB)
            if hasattr(jets[tight_jets[i]], 'hadronFlavour'):
                jet_hadronFlavour.append(jets[tight_jets[i]].hadronFlavour)
            else:
                jet_hadronFlavour.append(-9999)

            if hasattr(jets[tight_jets[i]], 'partonFlavour'):
                jet_partonFlavour.append(jets[tight_jets[i]].partonFlavour)
            else:
                jet_partonFlavour.append(-9999)

        self.out.fillBranch("njets",njets)
        self.out.fillBranch("jet_idx", jet_idx)
        self.out.fillBranch("jet_id", jet_id)
        self.out.fillBranch("jet_pt", jet_pt)
        self.out.fillBranch("jet_eta", jet_eta)
        self.out.fillBranch("jet_phi", jet_phi)
        self.out.fillBranch("jet_mass", jet_mass)
        self.out.fillBranch("jet_btagCSVV2", jet_btagCSVV2)
        self.out.fillBranch("jet_btagDeepB", jet_btagDeepB)
        self.out.fillBranch("jet_hadronFlavour", jet_hadronFlavour)
        self.out.fillBranch("jet_partonFlavour", jet_partonFlavour)
        self.out.fillBranch("mjj",(jets[tight_jets[0]].p4() + jets[tight_jets[1]].p4()).M())
        self.out.fillBranch("npvs",event.PV_npvs)
        self.out.fillBranch("event",event.event)
        self.out.fillBranch("lumi",event.luminosityBlock)
        self.out.fillBranch("run",event.run)

        return True

exampleModule = lambda : exampleProducer()

#python scripts/nano_postproc.py . /afs/cern.ch/work/j/jixiao/nano/2016/CMSSW_10_2_13/src/PhysicsTools/NanoAODTools/2016_DY_nanoAODv5.root -I PhysicsTools.NanoAODTools.postprocessing.modules.ssww.ewkwgjjModule exampleModule --bi python/postprocessing/scripts/ssww_keep_and_drop_2016_jec.txt --bo python/postprocessing/scripts/ssww_output_branch_selection_2016.txt