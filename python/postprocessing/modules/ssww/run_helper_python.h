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
using rvec_b = const RVec<bool> &;

// match leptons to gen information
// reference to: https://github.com/root-project/root/blob/master/tutorials/dataframe/df103_NanoAODHiggsAnalysis_python.h
RVec<int> lepton_real_code(int nlepton, rvec_i lepton_pdg_id, rvec_f lepton_pt, rvec_f lepton_eta, rvec_f lepton_phi, int nGenPart, rvec_i GenPart_pdgId, rvec_f GenPart_pt, rvec_i GenPart_statusFlags, rvec_f GenPart_eta, rvec_f GenPart_phi)
{
   RVec<int> lepton_real_fix(nlepton);
   for(int i=0; i<nlepton; i++){
    lepton_real_new[i]=0;
    for(int j=0; j<nGenPart; j++){
        if(GenPart_pt[j]>5 && abs(GenPart_pdgId[j])==abs(lepton_pdg_id[i]) && (GenPart_statusFlags[j]==0 || GenPart_statusFlags[j]==3) && deltaR(lepton_eta[i],lepton_phi[i],GenPart_eta[j],GenPart_phi[j])< 0.3){
            lepton_real_fix[i]=1;
            break;
        }
    }
   }
   return  lepton_real_fix;
}