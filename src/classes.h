#include "../interface/PyJetResolutionWrapper.h"
#include "../interface/PyJetResolutionScaleFactorWrapper.h"
#include "../interface/PyJetParametersWrapper.h"
#include "../interface/WeightCalculatorFromHistogram.h"
#include "../interface/ReduceMantissa.h"
#include "../interface/LeptonEfficiencyCorrectorCppWorker.h"

PyJetResolutionWrapper jetRes;
PyJetResolutionScaleFactorWrapper jetResScaleFactor;
PyJetParametersWrapper jetParams;
WeightCalculatorFromHistogram wcalc;
ReduceMantissaToNbitsRounding red(12);
LeptonEfficiencyCorrectorCppWorker lepSF;

/*
#include "../python/PhysicsTools/NanoAODTools/postprocessing/interface/PyJetResolutionWrapper.h"
#include "../python/PhysicsTools/NanoAODTools/postprocessing/interface/PyJetResolutionScaleFactorWrapper.h"
#include "../python/PhysicsTools/NanoAODTools/postprocessing/interface/PyJetParametersWrapper.h"
#include "../python/PhysicsTools/NanoAODTools/postprocessing/interface/WeightCalculatorFromHistogram.h"
#include "../python/PhysicsTools/NanoAODTools/postprocessing/interface/ReduceMantissa.h"

PyJetResolutionWrapper jetRes;
PyJetResolutionScaleFactorWrapper jetResScaleFactor;
PyJetParametersWrapper jetParams;
WeightCalculatorFromHistogram wcalc;
ReduceMantissaToNbitsRounding red(12);
*/