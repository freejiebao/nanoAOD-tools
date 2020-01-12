/// \file
/// \ingroup tutorial_dataframe
/// Header file with functions needed to execute the Python version
/// of the NanoAOD Higgs tutorial. The header is declared to the
/// ROOT C++ interpreter prior to the start of the analysis via the
/// `ROOT.gInterpreter.Declare()` function.
///
/// \date July 2019
/// \author Stefan Wunsch (KIT, CERN), Vincenzo Eduardo Padulano (UniMiB, CERN)

#include "Math/Vector4D.h"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TLatex.h"
#include "TStyle.h"
#include "deltaR.h"

using namespace ROOT::VecOps;
using RNode  = ROOT::RDF::RNode;
using rvec_f = const RVec<float>&;
using rvec_i = const RVec<int>&;
using rvec_b = const RVec<bool>&;

// match leptons to gen information
// reference to: https://github.com/root-project/root/blob/master/tutorials/dataframe/df103_NanoAODHiggsAnalysis_python.h

// https://github.com/PKUHEPEWK/WGamma/blob/master/wg_rdf.py
// lepton sf file
TFile electron_id_2016_sf_file("../../data/leptonSF/2016/electron/2016LegacyReReco_ElectronMVA80_Fall17V2.root", "read");
TH2F* electron_id_2016_sf = (TH2F*)electron_id_2016_sf_file.Get("EGamma_SF2D");
TFile electron_id_2017_sf_file("../../data/leptonSF/2017/electron/2017_ElectronTight.root", "read");
TH2F* electron_id_2017_sf = (TH2F*)electron_id_2017_sf_file.Get("EGamma_SF2D");
TFile electron_id_2018_sf_file("../../data/leptonSF/2018/electron/2018_ElectronMVA80.root", "read");
TH2F* electron_id_2018_sf = (TH2F*)electron_id_2018_sf_file.Get("EGamma_SF2D");
TFile electron_reco_2016_sf_file("../../data/leptonSF/2016/electron/EGM2D_BtoH_GT20GeV_RecoSF_Legacy2016.root", "read");
TH2F* electron_reco_2016_sf = (TH2F*)electron_reco_2016_sf_file.Get("EGamma_SF2D");
TFile electron_reco_2017_sf_file("../../data/leptonSF/2017/electron/egammaEffi.txt_EGM2D_runBCDEF_passingRECO.root", "read");
TH2F* electron_reco_2017_sf = (TH2F*)electron_reco_2017_sf_file.Get("EGamma_SF2D");
TFile electron_reco_2018_sf_file("../../data/leptonSF/2018/electron/egammaEffi.txt_EGM2D_updatedAll.root", "read");
TH2F* electron_reco_2018_sf = (TH2F*)electron_reco_2018_sf_file.Get("EGamma_SF2D");

TFile muon_iso_2016_sf_file("../../data/leptonSF/2016/muon/RunBCDEF_SF_ISO_tight.root", "read");
TH2D* muon_iso_2016_sf = (TH2D*)muon_iso_2016_sf_file.Get("NUM_TightRelIso_DEN_TightIDandIPCut_eta_pt");
TFile muon_id_2016_sf_file("../../data/leptonSF/2016/muon/RunBCDEF_SF_ID.root", "read");
TH2D* muon_id_2016_sf = (TH2D*)muon_id_2016_sf_file.Get("NUM_TightID_DEN_genTracks_eta_pt");
TFile muon_iso_2017_sf_file("../../data/leptonSF/2017/muon/RunBCDEF_SF_ISO_syst_tight.root", "read");
TH2D* muon_iso_2017_sf = (TH2D*)muon_iso_2017_sf_file.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta");
TFile muon_id_2017_sf_file("../../data/leptonSF/2017/muon/RunBCDEF_SF_ID_syst.root", "read");
TH2D* muon_id_2017_sf = (TH2D*)muon_id_2017_sf_file.Get("NUM_TightID_DEN_genTracks_pt_abseta");
TFile muon_iso_2018_sf_file("../../data/leptonSF/2018/muon/RunABCD_SF_ISO_tight.root", "read");
TH2D* muon_iso_2018_sf = (TH2D*)muon_iso_2018_sf_file.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta");
TFile muon_id_2018_sf_file("../../data/leptonSF/2018/muon/RunABCD_SF_ID.root", "read");
TH2D* muon_id_2018_sf = (TH2D*)muon_id_2018_sf_file.Get("NUM_TightID_DEN_TrackerMuons_pt_abseta");

// fake lepton weight files

TFile muon_2016_file("2016_fakerate_muon.root");
TFile electron_2016_file("2016_fakerate_electron.root");
TFile muon_2017_file("2017_fakerate_muon.root");
TFile electron_2017_file("2017_fakerate_electron.root");
TFile muon_2018_file("2018_fakerate_muon.root");
TFile electron_2018_file("2018_fakerate_electron.root");
TH2D* muon_2016_fr_hist     = (TH2D*)muon_2016_file.Get("fakerate");
TH2D* electron_2016_fr_hist = (TH2D*)electron_2016_file.Get("fakerate");
TH2D* muon_2017_fr_hist     = (TH2D*)muon_2017_file.Get("fakerate");
TH2D* electron_2017_fr_hist = (TH2D*)electron_2017_file.Get("fakerate");
TH2D* muon_2018_fr_hist     = (TH2D*)muon_2018_file.Get("fakerate");
TH2D* electron_2018_fr_hist = (TH2D*)electron_2018_file.Get("fakerate");

float electron_efficiency_scale_factor(float pt, float eta, TH2F* electron_reco_sf, TH2F* electron_id_sf, string id_err = "nom", string reco_err = "nom") {
    //the reco 2D histogram is really a 1D histogram
    float sf_id = electron_id_sf->GetBinContent(electron_id_sf->GetXaxis()->FindFixBin(eta), electron_id_sf->GetYaxis()->FindFixBin(pt));
    if (id_err == "up") {
        sf_id += electron_id_sf->GetBinError(electron_id_sf->GetXaxis()->FindFixBin(eta), electron_id_sf->GetYaxis()->FindFixBin(pt));
    }
    else if (id_err == "down") {
        sf_id -= electron_id_sf->GetBinError(electron_id_sf->GetXaxis()->FindFixBin(eta), electron_id_sf->GetYaxis()->FindFixBin(pt));
    }

    float sf_reco = electron_reco_sf->GetBinContent(electron_reco_sf->GetXaxis()->FindFixBin(eta), 1);
    if (reco_err == "up") {
        sf_reco += electron_reco_sf->GetBinError(electron_reco_sf->GetXaxis()->FindFixBin(eta), 1);
    }
    else if (reco_err == "down") {
        sf_reco -= electron_reco_sf->GetBinError(electron_reco_sf->GetXaxis()->FindFixBin(eta), 1);
    }

    return sf_id * sf_reco;
}

float muon_efficiency_scale_factor(float pt, float eta, string year, TH2D* muon_iso_sf, TH2D* muon_id_sf, string id_err = "nom", string iso_err = "nom") {
    int muon_iso_sf_xaxisbin = -1;
    int muon_iso_sf_yaxisbin = -1;
    if (year == "2016") {
        muon_iso_sf_xaxisbin = muon_iso_sf->GetXaxis()->FindFixBin(eta);
        muon_iso_sf_yaxisbin = muon_iso_sf->GetYaxis()->FindFixBin(TMath::Min(pt, float(muon_iso_sf->GetYaxis()->GetBinCenter(muon_iso_sf->GetNbinsY()))));
    }
    else if (year == "2017") {
        muon_iso_sf_yaxisbin = muon_iso_sf->GetYaxis()->FindFixBin(abs(eta));
        muon_iso_sf_xaxisbin = muon_iso_sf->GetXaxis()->FindFixBin(TMath::Min(pt, float(muon_iso_sf->GetXaxis()->GetBinCenter(muon_iso_sf->GetNbinsX()))));
    }
    else if (year == "2018") {
        muon_iso_sf_yaxisbin = muon_iso_sf->GetYaxis()->FindFixBin(abs(eta));
        muon_iso_sf_xaxisbin = muon_iso_sf->GetXaxis()->FindFixBin(TMath::Min(pt, float(muon_iso_sf->GetXaxis()->GetBinCenter(muon_iso_sf->GetNbinsX()))));
    }
    else
        assert(0);
    int muon_id_sf_xaxisbin = -1;
    int muon_id_sf_yaxisbin = -1;
    if (year == "2016") {
        muon_id_sf_xaxisbin = muon_id_sf->GetXaxis()->FindFixBin(eta);
        muon_id_sf_yaxisbin = muon_id_sf->GetYaxis()->FindFixBin(TMath::Min(pt, float(muon_id_sf->GetYaxis()->GetBinCenter(muon_id_sf->GetNbinsY()))));
    }
    else if (year == "2017") {
        muon_id_sf_yaxisbin = muon_id_sf->GetYaxis()->FindFixBin(abs(eta));
        muon_id_sf_xaxisbin = muon_id_sf->GetXaxis()->FindFixBin(TMath::Min(pt, float(muon_id_sf->GetXaxis()->GetBinCenter(muon_id_sf->GetNbinsX()))));
    }
    else if (year == "2018") {
        muon_id_sf_yaxisbin = muon_id_sf->GetYaxis()->FindFixBin(abs(eta));
        muon_id_sf_xaxisbin = muon_id_sf->GetXaxis()->FindFixBin(TMath::Min(pt, float(muon_id_sf->GetXaxis()->GetBinCenter(muon_id_sf->GetNbinsX()))));
    }
    else
        assert(0);
    float iso_sf = muon_iso_sf->GetBinContent(muon_iso_sf_xaxisbin, muon_iso_sf_yaxisbin);
    if (iso_err == "up") {
        iso_sf += muon_iso_sf->GetBinError(muon_iso_sf_xaxisbin, muon_iso_sf_yaxisbin);
    }
    else if (iso_err == "down") {
        iso_sf -= muon_iso_sf->GetBinError(muon_iso_sf_xaxisbin, muon_iso_sf_yaxisbin);
    }

    float id_sf = muon_id_sf->GetBinContent(muon_id_sf_xaxisbin, muon_id_sf_yaxisbin);
    if (id_err == "up") {
        id_sf += muon_id_sf->GetBinError(muon_id_sf_xaxisbin, muon_id_sf_yaxisbin);
    }
    else if (id_err == "down") {
        id_sf -= muon_id_sf->GetBinError(muon_id_sf_xaxisbin, muon_id_sf_yaxisbin);
    }
    return iso_sf * id_sf;
}

RVec<float> efficiency_scale_factor(rvec_f pt, rvec_f eta, rvec_i pdg_id, string year, string err_type) {
    RVec<float> sf(pt.size());

    TH2F* electron_reco_sf = 0;
    TH2F* electron_id_sf   = 0;
    TH2D* muon_iso_sf      = 0;
    TH2D* muon_id_sf       = 0;
    if (year == "2016") {
        electron_reco_sf = electron_reco_2016_sf;
        electron_id_sf   = electron_id_2016_sf;

        muon_iso_sf = muon_iso_2016_sf;
        muon_id_sf  = muon_id_2016_sf;
    }
    else if (year == "2017") {
        electron_reco_sf = electron_reco_2017_sf;
        electron_id_sf   = electron_id_2017_sf;

        muon_iso_sf = muon_iso_2017_sf;
        muon_id_sf  = muon_id_2017_sf;
    }
    else if (year == "2018") {
        electron_reco_sf = electron_reco_2018_sf;
        electron_id_sf   = electron_id_2018_sf;

        muon_iso_sf = muon_iso_2018_sf;
        muon_id_sf  = muon_id_2018_sf;
    }
    else
        assert(0);

    string muon_err_id       = "nom";
    string muon_err_iso      = "nom";
    string electron_err_id   = "nom";
    string electron_err_reco = "nom";

    if (err_type == "muon_id_up") {
        muon_err_id = "up";
    }
    else if (err_type == "muon_id_down") {
        muon_err_id = "down";
    }
    else if (err_type == "muon_iso_up") {
        muon_err_iso = "up";
    }
    else if (err_type == "muon_iso_down") {
        muon_err_iso = "down";
    }
    else if (err_type == "electron_id_up") {
        electron_err_id = "up";
    }
    else if (err_type == "electron_id_down") {
        electron_err_id = "down";
    }
    else if (err_type == "electron_reco_up") {
        electron_err_reco = "up";
    }
    else if (err_type == "electron_reco_down") {
        electron_err_reco = "down";
    }

    for (size_t i = 0; i < pdg_id.size(); i++) {
        if (abs(pdg_id[i]) == 13) {
            sf[i] = muon_efficiency_scale_factor(pt[i], eta[i], year, muon_id_sf, muon_iso_sf, muon_err_id, muon_err_iso);
        }
        else if (abs(pdg_id[i]) == 11) {
            sf[i] = electron_efficiency_scale_factor(pt[i], eta[i], electron_id_sf, electron_reco_sf, electron_err_id, electron_err_reco);
        }
        else
            assert(0);
    }
    return sf;
}

RVec<float> get_fake_lepton_weight(rvec_b fakeable, rvec_b tight, rvec_f pt, rvec_f eta, rvec_i pdg_id, string year, string syst = "nominal") {
    TH2D*       fr_hist_muon     = 0;
    TH2D*       fr_hist_electron = 0;
    RVec<float> wgt(pt.size());
    if (year == "2016") {
        fr_hist_muon     = muon_2016_fr_hist;
        fr_hist_electron = electron_2016_fr_hist;
    }
    else if (year == "2017") {
        fr_hist_muon     = muon_2017_fr_hist;
        fr_hist_electron = electron_2017_fr_hist;
    }
    else if (year == "2018") {
        fr_hist_muon     = muon_2018_fr_hist;
        fr_hist_electron = electron_2018_fr_hist;
    }
    else
        assert(0);

    for (size_t i = 0; i < pdg_id.size(); i++) {
        float myeta = TMath::Min(abs(eta[i]), float(2.4999));
        float mypt  = TMath::Min(pt[i], float(59.999));
        int   etabin;
        int   ptbin;
        float prob;
        if (fakeable[i] && !tight[i]) {
            if (abs(pdg_id[i]) == 13) {
                etabin = fr_hist_muon->GetXaxis()->FindFixBin(myeta);
                ptbin  = fr_hist_muon->GetYaxis()->FindFixBin(mypt);
                prob   = fr_hist_muon->GetBinContent(etabin, ptbin);
                if (syst == "up")
                    prob += fr_hist_muon->GetBinError(etabin, ptbin);
                else if (syst == "down")
                    prob -= fr_hist_muon->GetBinError(etabin, ptbin);
            }
            else if (abs(pdg_id[i]) == 11) {
                etabin = fr_hist_electron->GetXaxis()->FindFixBin(myeta);
                ptbin  = fr_hist_electron->GetYaxis()->FindFixBin(mypt);
                prob   = fr_hist_electron->GetBinContent(etabin, ptbin);
                if (syst == "up")
                    prob += fr_hist_electron->GetBinError(etabin, ptbin);
                else if (syst == "down")
                    prob -= fr_hist_electron->GetBinError(etabin, ptbin);
            }
            wgt[i] = prob / (1 - prob);
        }
        else {
            wgt[i] = 1.;
        }
    }
    return wgt;
}

float calc_mjj(float j1_pt, float j1_eta, float j1_phi, float j1_mass, float j2_pt, float j2_eta, float j2_phi, float j2_mass) {
    ROOT::Math::PtEtaPhiMVector p1(j1_pt, j1_eta, j1_phi, j1_mass);
    ROOT::Math::PtEtaPhiMVector p2(j2_pt, j2_eta, j2_phi, j2_mass);
    return (p1 + p2).M();
}

bool bveto_helper(rvec_f j_pt, rvec_f j_eta, rvec_f j_tagger, float wp) {
    for (auto i = 0U; i < j_pt.size(); ++i) {
        if (j_pt[i] > 20 && abs(j_eta[i]) < 2.4 && j_tagger[i] > wp)
            return false;
    }
    return true;
}

RVec<int> order_wz(rvec_i lepton_pdgId, rvec_f lepton_pt, rvec_f lepton_eta, rvec_f lepton_phi, rvec_f lepton_mass) {
    RVec<int> valid_order{0, 0, 1, 2};  // first is the flag for passing WZ selections, then two Z leptons, and one W lepton

    RVec<ROOT::Math::PtEtaPhiMVector> parts;
    for (int i = 0; i < lepton_pdgId.size(); i++) {
        ROOT::Math::PtEtaPhiMVector p(lepton_pt[i], lepton_eta[i], lepton_phi[i], lepton_mass[i]);
        parts.push_back(p);
    }

    // QCD suppression
    for (int i = 0; i < 2; i++) {
        for (int j = i + 1; j < 3; j++) {
            if ((parts[i] + parts[j]).M() <= 4) {
                return valid_order;
            }
            /*
            if (lepton_pdgId[i] * lepton_pdgId[j] < 0) {
                if ((parts[i] + parts[j]).M() <= 4) {
                    return valid_order;
                }
            }*/
        }
    }
    // mlll cut
    if((parts[0] + parts[1]+parts[2]).M()<=100){
        return valid_order;
    }

    float Zmass_2l  = -99999;
    int   Z_lepton1 = -1;
    int   Z_lepton2 = -1;
    int   W_lepton  = -1;
    for (int i = 0; i < 2; i++) {
        for (int j = i + 1; j < 3; j++) {
            if (lepton_pdgId[i] + lepton_pdgId[j] == 0) {
                if (abs((parts[i] + parts[j]).M() - 91.1876) < abs(Zmass_2l - 91.1876)) {
                    Zmass_2l  = (parts[i] + parts[j]).M();
                    Z_lepton1 = i;
                    Z_lepton2 = j;
                    W_lepton  = 3 - i - j;
                }
            }
        }
    }
    if (Z_lepton1 == -1) {  // no ossf pair found
        return valid_order;
    }
    else {
        if (lepton_pt[Z_lepton1] > 25 && lepton_pt[Z_lepton2] > 10 && lepton_pt[W_lepton] > 20 && abs(Zmass_2l - 91.1876) < 15) {
            valid_order = {1, Z_lepton1, Z_lepton2, W_lepton};
        }
    }

    return valid_order;
}
RVec<int> order_zz(rvec_i lepton_pdgId, rvec_f lepton_pt, rvec_f lepton_eta, rvec_f lepton_phi, rvec_f lepton_mass) {
    RVec<int> valid_order{0, 0, 1, 2, 3};        // first is the flag for passing ZZ selections, then two Z1 leptons, and two Z2 leptons
    RVec<int> _order1(lepton_pdgId.size() + 1);  // first is the flag for passing ZZ selections
    RVec<int> _order2(lepton_pdgId.size() + 1);  // first is the flag for passing ZZ selections
    RVec<int> _order3(lepton_pdgId.size() + 1);  // first is the flag for passing ZZ selections

    if ((lepton_pdgId[0] + lepton_pdgId[1] + lepton_pdgId[2] + lepton_pdgId[3]) != 0) {
        return valid_order;
    }
    //ROOT::Math::PtEtaPhiMVector       p1(lepton_pt[0], lepton_eta[0], lepton_phi[0], lepton_mass[0]);
    //ROOT::Math::PtEtaPhiMVector       p2(lepton_pt[1], lepton_eta[1], lepton_phi[1], lepton_mass[1]);
    //ROOT::Math::PtEtaPhiMVector       p3(lepton_pt[2], lepton_eta[2], lepton_phi[2], lepton_mass[2]);
    //ROOT::Math::PtEtaPhiMVector       p4(lepton_pt[3], lepton_eta[3], lepton_phi[3], lepton_mass[3]);

    RVec<ROOT::Math::PtEtaPhiMVector> parts;
    for (int i = 0; i < lepton_pdgId.size(); i++) {
        ROOT::Math::PtEtaPhiMVector p(lepton_pt[i], lepton_eta[i], lepton_phi[i], lepton_mass[i]);
        parts.push_back(p);
    }
    // QCD suppression
    for (int i = 0; i < 3; i++) {
        for (int j = i + 1; j < 4; j++) {
            if (lepton_pdgId[i] * lepton_pdgId[j] < 0) {
                if ((parts[i] + parts[j]).M() <= 4) {
                    return valid_order;
                }
            }
        }
    }
    if ((parts[0] + parts[1] + parts[2] + parts[3]).M() <= 70) {
        return valid_order;
    }

    float           Za_mass[]          = {-999999, -999999, -999999};
    float           Zb_mass[]          = {-999999, -999999, -999999};
    float           delta_Zmass_min[]  = {-999999, -999999, -999999};
    float           Z2_scalar_pt_sum[] = {-999999, -999999, -999999};
    int             Za_lep1[]          = {0, 0, 0};
    int             Za_lep2[]          = {1, 2, 3};
    int             Zb_lep1[]          = {2, 1, 1};
    int             Zb_lep2[]          = {3, 3, 2};
    RVec<RVec<int>> _order{_order1, _order2, _order3};
    bool case[] = {false, false, false};

    int idx = 0;
    // case1: p1 pair with p2
    for (int i = 0; i < 3; i++) {
        Za_mass[i] = (parts[Za_lep1[i]] + parts[Za_lep2[i]]).M();
        Zb_mass[i] = (parts[Zb_lep1[i]] + parts[Zb_lep2[i]]).M();
        if ((lepton_pdgId[Za_lep1[i]] + lepton_pdgId[Za_lep2[i]] == 0) && (lepton_pdgId[Zb_lep1[i]] + lepton_pdgId[Zb_lep2[i]] == 0) && Za_mass[i] > 60 && Za_mass[i] < 120 && Zb_mass[i] > 60 && Zb_mass[i] < 120) {  //Z candidates, both are on shell
            if (lepton_pt[Za_lep1[i]] > 20 && lepton_pt[Za_lep2[i]] > 10 && lepton_pt[Zb_lep1[i]] > 20 && lepton_pt[Zb_lep2[i]] > 10) {                                                                                //lepton pt
                case[i]=true;
                if (abs(Za_mass[i] - 91.1876) < abs(Zb_mass[i] - 91.1876)) {
                    Z2_scalar_pt_sum[i] = (lepton_pt[Zb_lep1[i]] + lepton_pt[Zb_lep2[i]]);
                    delta_Zmass_min[i]  = abs(Za_mass[i] - 91.1876);
                    _order[i]           = {1, Za_lep1[i], Za_lep2[i],Zb_lep1[i], Zb_lep2[i]};
                }else{
                    Z2_scalar_pt_sum[i] = (lepton_pt[Za_lep1[i]] + lepton_pt[Za_lep2[i]]);
                    delta_Zmass_min[i]  = abs(Zb_mass[i] - 91.1876);
                    _order[i]           = {1, Zb_lep1[i], Zb_lep2[i],Za_lep1[i], Za_lep2[i]};
                }
            }
        }
    }

    if (!(case[0] || case[1] ||case[3])){
        return valid_order;
    }

    int who_win=0;
    float winner_delta_Zmass_min=9999;
    float winner_sum_pt=-9999;
    for(int i=0; i<3;i++){
        if(!case[i]){
            continue;
        }
        if(winner_delta_Zmass_min>delta_Zmass_min[i]){
            who_win=i;
            winner_delta_Zmass_min=delta_Zmass_min[i];
            winner_sum_pt=Z2_scalar_pt_sum[i];
        }else(abs(winner_delta_Zmass_min-delta_Zmass_min[i])<0.000001){
            if(winner_sum_pt<Z2_scalar_pt_sum[i]){
                who_win=i;
                winner_delta_Zmass_min=delta_Zmass_min[i];
                winner_sum_pt=Z2_scalar_pt_sum[i];
            }
        }
    }
    return _order[who_win];
    /*
    Za_mass[idx] = (parts[0] + parts[1]).M();
    Zb_mass[idx] = (parts[2] + parts[3]).M();
    if ((lepton_pdgId[0] + lepton_pdgId[1] == 0) && (lepton_pdgId[2] + lepton_pdgId[3] == 0)) {
        if (Za_mass[idx] > 60 && Za_mass[idx] < 120 && Zb_mass[idx] > 60 && Zb_mass[idx] < 120) {
            if (lepton_pt[0] > 20 && lepton_pt[1] > 10 && lepton_pt[2] > 20 && lepton_pt[3] > 10) {  //lepton pt
                if ((parts[0] + parts[1] + parts[2] + parts[3]).M() > 70) {
                    case[idx] = true;
                    if (abs(Za_mass[idx] - 91.1876) < abs(Zb_mass[idx] - 91.1876)) {
                        Z2_scalar_pt_sum[idx] = (lepton_pt[2] + lepton_pt[3]);
                        delta_Zmass_min[idx]  = abs(Za_mass[idx] - 91.1876);
                        _order1             = {1, 0, 1, 2, 3};
                    }
                    else {
                        Z2_scalar_pt_sum[idx] = (lepton_pt[0] + lepton_pt[1]);
                        delta_Zmass_min[idx]  = abs(Zb_mass[idx] - 91.1876);
                        _order1             = {1, 2, 3, 0, 1};
                    }
                }
            }
        }
    }
    */
    // case1: p1 pair with p3
    /*
    Za_mass[1] = (parts[0] + parts[2]).M();
    Zb_mass[1] = (parts[1] + parts[3]).M();
    if ((lepton_pdgId[0] + lepton_pdgId[2] == 0) && (lepton_pdgId[1] + lepton_pdgId[3] == 0)) {
        if (Za_mass[1] > 60 && Za_mass[1] < 120 && Zb_mass[1] > 60 && Zb_mass[1] < 120) {            //Z candidates, both are on shell
            if (lepton_pt[0] > 20 && lepton_pt[2] > 10 && lepton_pt[1] > 20 && lepton_pt[3] > 10) {  //lepton pt
                if ((parts[0] + parts[1] + parts[2] + parts[3]).M() > 70) {
                    case2 = true;
                    if (abs(Za_mass[1] - 91.1876) < abs(Zb_mass[1] - 91.1876)) {
                        Z2_scalar_pt_sum[1] = (lepton_pt[1] + lepton_pt[3]);
                        delta_Zmass_min[1]  = abs(Za_mass[1] - 91.1876);
                        _order2             = {1, 0, 2, 1, 3};
                    }
                    else {
                        Z2_scalar_pt_sum[1] = (lepton_pt[0] + lepton_pt[2]);
                        delta_Zmass_min[1]  = abs(Zb_mass[1] - 91.1876);
                        _order2             = {1, 1, 3, 0, 2};
                    }
                }
            }
        }
    }
    */
    // case1: p1 pair with p4
    /*
    Za_mass[2] = (parts[0] + parts[3]).M();
    Zb_mass[2] = (parts[1] + parts[2]).M();
    if ((lepton_pdgId[0] + lepton_pdgId[3] == 0) && (lepton_pdgId[1] + lepton_pdgId[2] == 0)) {
        if (Za_mass[2] > 60 && Za_mass[2] < 120 && Zb_mass[2] > 60 && Zb_mass[2] < 120) {            //Z candidates, both are on shell
            if (lepton_pt[0] > 20 && lepton_pt[3] > 10 && lepton_pt[1] > 20 && lepton_pt[2] > 10) {  //lepton pt
                if ((parts[0] + parts[1] + parts[2] + parts[3]).M() > 70) {
                    case3 = true;
                    if (abs(Za_mass[2] - 91.1876) < abs(Zb_mass[2] - 91.1876)) {
                        Z2_scalar_pt_sum[2] = (lepton_pt[1] + lepton_pt[2]);
                        delta_Zmass_min[2]  = abs(Za_mass[2] - 91.1876);
                        _order3             = {1, 0, 3, 1, 2};
                    }
                    else {
                        Z2_scalar_pt_sum[2] = (lepton_pt[0] + lepton_pt[3]);
                        delta_Zmass_min[2]  = abs(Zb_mass[2] - 91.1876);
                        _order3             = {1, 1, 2, 0, 3};
                    }
                }
            }
        }
    }
    */
}

float invariant_mass_wz(rvec_i lepton_order, rvec_f lepton_pt, rvec_f lepton_eta, rvec_f lepton_phi, rvec_f lepton_mass, int type) {
    float invariant_mass = -9999;
    switch (type) {
    case 0:
        // l1 l2
        ROOT::Math::PtEtaPhiMVector p1(lepton_pt[lepton_order[1]], lepton_eta[lepton_order[1]], lepton_phi[lepton_order[1]], lepton_mass[lepton_order[1]]);
        ROOT::Math::PtEtaPhiMVector p2(lepton_pt[lepton_order[2]], lepton_eta[lepton_order[2]], lepton_phi[lepton_order[2]], lepton_mass[lepton_order[2]]);
        invariant_mass = (p1 + p2).M();
        break;
    case 1:
        // l1 l3
        ROOT::Math::PtEtaPhiMVector p1(lepton_pt[lepton_order[1]], lepton_eta[lepton_order[1]], lepton_phi[lepton_order[1]], lepton_mass[lepton_order[1]]);
        ROOT::Math::PtEtaPhiMVector p2(lepton_pt[lepton_order[3]], lepton_eta[lepton_order[3]], lepton_phi[lepton_order[3]], lepton_mass[lepton_order[3]]);
        invariant_mass = (p1 + p2).M();
        break;
    case 2:
        // l2 l3
        ROOT::Math::PtEtaPhiMVector p1(lepton_pt[lepton_order[2]], lepton_eta[lepton_order[2]], lepton_phi[lepton_order[2]], lepton_mass[lepton_order[2]]);
        ROOT::Math::PtEtaPhiMVector p2(lepton_pt[lepton_order[3]], lepton_eta[lepton_order[3]], lepton_phi[lepton_order[3]], lepton_mass[lepton_order[3]]);
        invariant_mass = (p1 + p2).M();
        break;
    case 3:
        // l1 l2 l3
        ROOT::Math::PtEtaPhiMVector p1(lepton_pt[lepton_order[1]], lepton_eta[lepton_order[1]], lepton_phi[lepton_order[1]], lepton_mass[lepton_order[1]]);
        ROOT::Math::PtEtaPhiMVector p2(lepton_pt[lepton_order[2]], lepton_eta[lepton_order[2]], lepton_phi[lepton_order[2]], lepton_mass[lepton_order[2]]);
        ROOT::Math::PtEtaPhiMVector p1(lepton_pt[lepton_order[3]], lepton_eta[lepton_order[3]], lepton_phi[lepton_order[3]], lepton_mass[lepton_order[3]]);
        invariant_mass = (p1 + p2 + p3).M();
        break;
    default:
        invariant_mass = -9999;
    }
    return invariant_mass;
}

float invariant_mass_zz(rvec_i lepton_order, rvec_f lepton_pt, rvec_f lepton_eta, rvec_f lepton_phi, rvec_f lepton_mass, int type) {
    float invariant_mass = -9999;
    switch (type) {
    case 0:
        // l1 l2
        ROOT::Math::PtEtaPhiMVector p1(lepton_pt[lepton_order[1]], lepton_eta[lepton_order[1]], lepton_phi[lepton_order[1]], lepton_mass[lepton_order[1]]);
        ROOT::Math::PtEtaPhiMVector p2(lepton_pt[lepton_order[2]], lepton_eta[lepton_order[2]], lepton_phi[lepton_order[2]], lepton_mass[lepton_order[2]]);
        invariant_mass = (p1 + p2).M();
        break;
    case 1:
        // l3 l4
        ROOT::Math::PtEtaPhiMVector p1(lepton_pt[lepton_order[3]], lepton_eta[lepton_order[3]], lepton_phi[lepton_order[3]], lepton_mass[lepton_order[3]]);
        ROOT::Math::PtEtaPhiMVector p2(lepton_pt[lepton_order[4]], lepton_eta[lepton_order[4]], lepton_phi[lepton_order[4]], lepton_mass[lepton_order[4]]);
        invariant_mass = (p1 + p2).M();
        break;
    case 2:
        // l1 l2 l3 l4
        ROOT::Math::PtEtaPhiMVector p1(lepton_pt[lepton_order[1]], lepton_eta[lepton_order[1]], lepton_phi[lepton_order[1]], lepton_mass[lepton_order[1]]);
        ROOT::Math::PtEtaPhiMVector p2(lepton_pt[lepton_order[2]], lepton_eta[lepton_order[2]], lepton_phi[lepton_order[2]], lepton_mass[lepton_order[2]]);
        ROOT::Math::PtEtaPhiMVector p3(lepton_pt[lepton_order[3]], lepton_eta[lepton_order[3]], lepton_phi[lepton_order[3]], lepton_mass[lepton_order[3]]);
        ROOT::Math::PtEtaPhiMVector p4(lepton_pt[lepton_order[4]], lepton_eta[lepton_order[4]], lepton_phi[lepton_order[4]], lepton_mass[lepton_order[4]]);
        invariant_mass = (p1 + p2 + p3 + p4).M();
        break;
    default:
        invariant_mass = -9999;
    }
    return invariant_mass;
}
