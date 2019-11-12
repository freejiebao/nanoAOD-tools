/// \file
/// \ingroup tutorial_dataframe
/// Header file with functions needed to execute the Python version
/// of the NanoAOD Higgs tutorial. The header is declared to the
/// ROOT C++ interpreter prior to the start of the analysis via the
/// `ROOT.gInterpreter.Declare()` function.
///
/// \date July 2019
/// \author Stefan Wunsch (KIT, CERN), Vincenzo Eduardo Padulano (UniMiB, CERN)

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TLatex.h"
#include "Math/Vector4D.h"
#include "TStyle.h"
#include "deltaR.h"

using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;
using rvec_f = const RVec<float> &;
using rvec_i = const RVec<int> &;

// match leptons to gen information
// reference to: https://github.com/root-project/root/blob/master/tutorials/dataframe/df103_NanoAODHiggsAnalysis_python.h

// https://github.com/PKUHEPEWK/WGamma/blob/master/wg_rdf.py
// lepton sf file
TFile electron_id_2016_sf_file("../../data/leptonSF/electron/2016/2016LegacyReReco_ElectronMVA80_Fall17V2.root","read");
TH2F * electron_id_2016_sf = (TH2F*) electron_id_2016_sf_file.Get("EGamma_SF2D");
TFile electron_id_2017_sf_file("../../data/leptonSF/electron/2017/2017_ElectronMedium.root","read");
TH2F * electron_id_2017_sf = (TH2F*)electron_id_2017_sf_file.Get("EGamma_SF2D");
TFile electron_id_2018_sf_file("../../data/leptonSF/electron/2018/2018_ElectronMedium.root","read");
TH2F * electron_id_2018_sf = (TH2F*)electron_id_2018_sf_file.Get("EGamma_SF2D");
TFile electron_reco_2016_sf_file("../../data/leptonSF/electron/2016/EGM2D_BtoH_GT20GeV_RecoSF_Legacy2016.root","read");
TH2F * electron_reco_2016_sf = (TH2F*) electron_reco_2016_sf_file.Get("EGamma_SF2D");
TFile electron_reco_2017_sf_file("../../data/leptonSF/electron/2017/egammaEffi.txt_EGM2D_runBCDEF_passingRECO.root","read");
TH2F * electron_reco_2017_sf = (TH2F*)electron_reco_2017_sf_file.Get("EGamma_SF2D");
TFile electron_reco_2018_sf_file("../../data/leptonSF/electron/2018/egammaEffi.txt_EGM2D_updatedAll.root" ,"read");
TH2F * electron_reco_2018_sf = (TH2F*)electron_reco_2018_sf_file.Get("EGamma_SF2D");

TFile muon_iso_2016_sf_file("../../data/leptonSF/muon/2016/RunBCDEF_SF_ISO_tight.root","read");
TH2D * muon_iso_2016_sf = (TH2D*) muon_iso_2016_sf_file.Get("NUM_TightRelIso_DEN_TightIDandIPCut_eta_pt");
TFile muon_id_2016_sf_file("../../data/leptonSF/muon/2016/RunBCDEF_SF_ID.root","read");
TH2D * muon_id_2016_sf = (TH2D*) muon_id_2016_sf_file.Get("NUM_TightID_DEN_genTracks_eta_pt");
TFile muon_iso_2017_sf_file("../../data/leptonSF/electron/2017/RunBCDEF_SF_ISO.root","read");
TH2D * muon_iso_2017_sf = (TH2D*) muon_iso_2017_sf_file.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta");
TFile muon_id_2017_sf_file("../../data/leptonSF/electron/2017/RunBCDEF_SF_ID.root","read");
TH2D * muon_id_2017_sf = (TH2D*) muon_id_2017_sf_file.Get("NUM_TightID_DEN_genTracks_pt_abseta");
TFile muon_iso_2018_sf_file("../../data/leptonSF/electron/2018/RunABCD_SF_ISO.root","read");
TH2D * muon_iso_2018_sf = (TH2D*) muon_iso_2018_sf_file.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta");
TFile muon_id_2018_sf_file("../../data/leptonSF/electron/2018/RunABCD_SF_ID.root","read");
TH2D * muon_id_2018_sf = (TH2D*)muon_id_2018_sf_file.Get("NUM_TightID_DEN_TrackerMuons_pt_abseta");

// fake lepton weight files
TFile muon_2016_file("/afs/cern.ch/user/a/amlevin/wg/fake_lepton_weights/muon_2016_frs.root");
TFile electron_2016_file("/afs/cern.ch/user/a/amlevin/wg/fake_lepton_weights/electron_2016_frs.root");
TFile muon_2017_file("/afs/cern.ch/user/a/amlevin/wg/fake_lepton_weights/muon_2017_frs.root");
TFile electron_2017_file("/afs/cern.ch/user/a/amlevin/wg/fake_lepton_weights/electron_2017_frs.root");
TFile muon_2018_file("/afs/cern.ch/user/a/amlevin/wg/fake_lepton_weights/muon_2018_frs.root");
TFile electron_2018_file("/afs/cern.ch/user/a/amlevin/wg/fake_lepton_weights/electron_2018_frs.root");
TH2D * muon_2016_fr_hist = (TH2D*)muon_2016_file.Get("muon_frs");
TH2D * electron_2016_fr_hist = (TH2D*)electron_2016_file.Get("electron_frs");
TH2D * muon_2017_fr_hist = (TH2D*)muon_2017_file.Get("muon_frs");
TH2D * electron_2017_fr_hist = (TH2D*)electron_2017_file.Get("electron_frs");
TH2D * muon_2018_fr_hist = (TH2D*)muon_2018_file.Get("muon_frs");
TH2D * electron_2018_fr_hist = (TH2D*)electron_2018_file.Get("electron_frs");

RVec<float> electron_efficiency_scale_factor(rvec_f pt, rvec_f eta, string year,bool id_err_up=false, bool reco_err_up=false) {
    TH2F * electron_reco_sf = 0;
    TH2F * electron_id_sf = 0;
    RVec<float> sf(pt.size());
    if (year == "2016") {
        electron_reco_sf = electron_reco_2016_sf;
        electron_id_sf = electron_id_2016_sf;
    }
    else if (year == "2017"){
        electron_reco_sf = electron_reco_2017_sf;
        electron_id_sf = electron_id_2017_sf;
    }
    else if (year == "2018") {
        electron_reco_sf = electron_reco_2018_sf;
        electron_id_sf = electron_id_2018_sf;
    }
    else
        assert(0);
    //the reco 2D histogram is really a 1D histogram
    for (size_t i = 0; i < pt.size(); i++) {
        float sf_id=electron_id_sf->GetBinContent(electron_id_sf->GetXaxis()->FindFixBin(eta[i]),electron_id_sf->GetYaxis()->FindFixBin(pt[i]));
        if (id_err_up) sf_id+=electron_id_sf->GetBinError(electron_id_sf->GetXaxis()->FindFixBin(eta[i]),electron_id_sf->GetYaxis()->FindFixBin(pt[i]));
        float sf_reco=electron_reco_sf->GetBinContent(electron_reco_sf->GetXaxis()->FindFixBin(eta[i]),1);
        if (reco_err_up) sf_reco+=electron_reco_sf->GetBinError(electron_reco_sf->GetXaxis()->FindFixBin(eta[i]),1);

        sf[i]=sf_id*sf_reco;
    }
    return sf;
}

RVec<float> muon_efficiency_scale_factor(rvec_f pt,rvec_f eta,string year,bool iso_err_up=false,bool id_err_up=false) {
    TH2D * muon_iso_sf = 0;
    TH2D * muon_id_sf = 0;
    RVec<float> sf(pt.size());
    if (year == "2016") {
        muon_iso_sf = muon_iso_2016_sf;
        muon_id_sf = muon_id_2016_sf;
    }
    else if (year == "2017") {
        muon_iso_sf = muon_iso_2017_sf;
        muon_id_sf = muon_id_2017_sf;
    }
    else if (year == "2018"){
        muon_iso_sf = muon_iso_2018_sf;
        muon_id_sf = muon_id_2018_sf;
    }
    else assert(0);

    for (size_t i = 0; i < pt.size(); i++) {
        int muon_iso_sf_xaxisbin = -1;
        int muon_iso_sf_yaxisbin = -1;
        if (year == "2016") {
            muon_iso_sf_xaxisbin = muon_iso_sf->GetXaxis()->FindFixBin(eta[i]);
            muon_iso_sf_yaxisbin = muon_iso_sf->GetYaxis()->FindFixBin(TMath::Min(pt[i],float(muon_iso_sf->GetYaxis()->GetBinCenter(muon_iso_sf->GetNbinsY()))));
        }
        else if (year == "2017") {
            muon_iso_sf_yaxisbin = muon_iso_sf->GetYaxis()->FindFixBin(abs(eta[i]));
            muon_iso_sf_xaxisbin = muon_iso_sf->GetXaxis()->FindFixBin(TMath::Min(pt[i],float(muon_iso_sf->GetXaxis()->GetBinCenter(muon_iso_sf->GetNbinsX()))));
        }
        else if (year == "2018") {
            muon_iso_sf_yaxisbin = muon_iso_sf->GetYaxis()->FindFixBin(abs(eta[i]));
            muon_iso_sf_xaxisbin = muon_iso_sf->GetXaxis()->FindFixBin(TMath::Min(pt[i],float(muon_iso_sf->GetXaxis()->GetBinCenter(muon_iso_sf->GetNbinsX()))));
        }
        else assert(0);
        int muon_id_sf_xaxisbin = -1;
        int muon_id_sf_yaxisbin = -1;
        if (year == "2016") {
            muon_id_sf_xaxisbin = muon_id_sf->GetXaxis()->FindFixBin(eta[i]);
            muon_id_sf_yaxisbin = muon_id_sf->GetYaxis()->FindFixBin(TMath::Min(pt[i],float(muon_id_sf->GetYaxis()->GetBinCenter(muon_id_sf->GetNbinsY()))));
        }
        else if (year == "2017") {
            muon_id_sf_yaxisbin = muon_id_sf->GetYaxis()->FindFixBin(abs(eta[i]));
            muon_id_sf_xaxisbin = muon_id_sf->GetXaxis()->FindFixBin(TMath::Min(pt[i],float(muon_id_sf->GetXaxis()->GetBinCenter(muon_id_sf->GetNbinsX()))));
        }
        else if (year == "2018") {
            muon_id_sf_yaxisbin = muon_id_sf->GetYaxis()->FindFixBin(abs(eta[i]));
            muon_id_sf_xaxisbin = muon_id_sf->GetXaxis()->FindFixBin(TMath::Min(pt[i],float(muon_id_sf->GetXaxis()->GetBinCenter(muon_id_sf->GetNbinsX()))));
        }
        else assert(0);
        float iso_sf = muon_iso_sf->GetBinContent(muon_iso_sf_xaxisbin,muon_iso_sf_yaxisbin);
        if (iso_err_up) iso_sf += muon_iso_sf->GetBinError(muon_iso_sf_xaxisbin,muon_iso_sf_yaxisbin);
        float id_sf = muon_id_sf->GetBinContent(muon_id_sf_xaxisbin,muon_id_sf_yaxisbin);

        if (id_err_up) id_sf += muon_id_sf->GetBinError(muon_id_sf_xaxisbin,muon_id_sf_yaxisbin) ;
        sf[i]=iso_sf * id_sf;
    }
    return sf;
}

RVec<float> get_fake_lepton_weight(rvec_f eta, rvec_f pt, string year, int lepton_pdg_id, string syst = "nominal")
{
    TH2D * fr_hist = 0;
    RVec<float> wgt(pt.size());
    if (year == "2016" && abs(lepton_pdg_id) == 13) fr_hist = muon_2016_fr_hist;
    else if (year == "2016" && abs(lepton_pdg_id) == 11) fr_hist = electron_2016_fr_hist;
    else if (year == "2017" && abs(lepton_pdg_id) == 13) fr_hist = muon_2017_fr_hist;
    else if (year == "2017" && abs(lepton_pdg_id) == 11) fr_hist = electron_2017_fr_hist;
    else if (year == "2018" && abs(lepton_pdg_id) == 13) fr_hist = muon_2018_fr_hist;
    else if (year == "2018" && abs(lepton_pdg_id) == 11) fr_hist = electron_2018_fr_hist;
    else assert(0);
    for (size_t i; i<pt.size();i++){
        float myeta  = TMath::Min(abs(eta[i]),float(2.4999));
        float mypt  = TMath::Min(pt[i],float(59.999));
        int etabin = fr_hist->GetXaxis()->FindFixBin(myeta);
        int ptbin = fr_hist->GetYaxis()->FindFixBin(mypt);
        float prob = fr_hist->GetBinContent(etabin,ptbin);
        if (syst == "up") prob += fr_hist->GetBinError(etabin,ptbin);
        else if (syst == "down") prob -= fr_hist->GetBinError(etabin,ptbin);
        else assert(syst == "nominal");
        wgt[i]=prob/(1-prob);
    }
    return wgt;
}

float calc_mjj(float j1_pt, float j1_eta, float j1_phi, float j1_mass, float j2_pt, float j2_eta, float j2_phi, float j2_mass)
{
    ROOT::Math::PtEtaPhiMVector p1(j1_pt, j1_eta, j1_phi, j1_mass);
    ROOT::Math::PtEtaPhiMVector p2(j2_pt, j2_eta, j2_phi, j2_mass);
    return (p1 + p2).M();
}

bool bveto_helper(rvec_f j_pt, rvec_f j_eta, rvec_f j_tagger, float wp)
{
    for (auto i=0U;i < j_pt.size(); ++i) {
        if(j_pt[i]>20 && abs(j_eta[i])<2.4 && j_tagger[i]>wp)
            return false;
    }
    return true;
}