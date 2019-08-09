import ROOT
import SAMPLE

ROOT.ROOT.EnableImplicitMT()

def theory_unc(df):
    #df = ROOT.ROOT.RDataFrame("Events", files)
    df_unc=df.Filter('nLepton>1 && nCleanJet > 1 && mll > 20 && MET_pt > 30 && mjj > 500 && abs(detajj) > 2.5')\
        .Filter('CleanJet_eta[0]<4.7 && CleanJet_eta[1]<4.7 && CleanJet_pt[0]>30 && CleanJet_pt[1]>30')\
        .Filter('Lepton_pt[0]>30 && Lepton_pt[1]>30 && Alt$(Lepton_pt[2],-9999.) < 10')\
        .Filter('(abs(Lepton_pdgId[0])==11 && abs(Lepton_eta[0])<2.4) || (abs(Lepton_pdgId[0])==13 && abs(Lepton_eta[0])<2.5)')\
        .Filter('(abs(Lepton_pdgId[1])==11 && abs(Lepton_eta[1])<2.4) || (abs(Lepton_pdgId[1])==13 && abs(Lepton_eta[1])<2.5)') \
        .Filter('abs((Lepton_eta[0] - (CleanJet_eta[0]+CleanJet_eta[1])/2)/detajj) < 0.5') \
        .Filter('abs((Lepton_eta[1] - (CleanJet_eta[0]+CleanJet_eta[1])/2)/detajj) < 0.5') \
        .Filter('abs(Lepton_pdgId[0]*Lepton_pdgId[1])!=11*11 || abs(mll - 91) > 15')\
        .Filter('bool bVeto=true;for(int i=0;i<nCleanJet;i++){if(CleanJet_pt[i]>20 && abs(CleanJet_eta[i]) < 2.5 && Jet_btagDeepB[CleanJet_jetIdx[i]] > 0.1522){bVeto=false;break;};};return bVeto;') \
        .Filter('bool tauVeto=true;for(int i=0;i<nTau;i++){if(Tau_pt[i] > 18 && Tau_rawIso[i] >=1 && sqrt( pow(Tau_eta[i] - Lepton_eta[0], 2) + pow(abs(abs(Tau_phi[i] - Lepton_phi[0])-pi)-pi, 2) ) > 0.3 && Tau_pt[i] > 18 && Tau_rawIso[i] >=1 && sqrt( pow(Tau_eta[i] - Lepton_eta[1], 2) + pow(abs(abs(Tau_phi[i] - Lepton_phi[1])-pi)-pi, 2) ) > 0.3){tauVeto=false; break;};};return tauVeto;')\
        .Filter('Sum$(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Jet_btagDeepB[CleanJet_jetIdx] > 0.1522) == 0')\
        .Define('qcd_unc','float sum=0;for(int i=0; i < nLHEPdfWeight; i++){sum += LHEPdfWeight[i];};\
                         float mean=sum/nLHEPdfWeight;sum=0;for(int i=0; i < nLHEPdfWeight; i++){sum+=LHEPdfWeight[i]*LHEPdfWeight[i];};\
                         return sqrt((sum-nLHEPdfWeight*mean*mean)/(nLHEPdfWeight-1));')\
        .Define('scale_unc','float Max=LHEScaleWeight[0],Min=LHEScaleWeight[0],central=LHEScaleWeight[4];\
                           for(int i=0; i < nLHEScaleWeight; i++){\
                           if(i!=2 || i!=6){if(Max<LHEScaleWeight[i]){Max=LHEScaleWeight[i];};if(Min>LHEScaleWeight[i]){Min=LHEScaleWeight[i];};};};\
                           return max(abs(Max-central),abs(Min-central))/central;')
    histo=df_unc.Filter('Lepton_pdgId[0]*Lepton_pdgId[1]>0')\
                   .Define('weight','return XSWeight*SFweight2l*GenLepMatch2l*METFilter_MC*LepCut2l__ele_mvaFall17Iso_WP90_SS__mu_cut_Tight_HWWW*LepSF2l__ele_mvaFall17Iso_WP90_SS__mu_cut_Tight_HWWW')\
                   .Define('genlep1pt','return GenDressedLepton_pt[0]')\
                   .Histo1D(("GenDressedLepton_pt", "GenDressedLepton_pt", 20, 0, 300), "genlep1pt","weight")
    c1 = ROOT.TCanvas()
    histo.Draw()
    c1.Saveas('GenDressedLepton_pt.pdf')
    return df_unc

if __name__ == '__main__':
    df = ROOT.ROOT.RDataFrame("Events", 'WpWpJJ_EWK.root')
    df_unc = theory_unc(df)
    df_unc.Snapshot("Events", "newWpWpJJ_EWK.root")
