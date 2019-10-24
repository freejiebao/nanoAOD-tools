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