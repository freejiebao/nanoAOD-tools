#include "../python/PhysicsTools/NanoAODTools/postprocessing/interface/PyJetResolutionWrapper.h"
#include "../python/PhysicsTools/NanoAODTools/postprocessing/interface/PyJetResolutionScaleFactorWrapper.h"
#include "../python/PhysicsTools/NanoAODTools/postprocessing/interface/PyJetParametersWrapper.h"
#include "../python/PhysicsTools/NanoAODTools/postprocessing/interface/WeightCalculatorFromHistogram.h"
#include "../python/PhysicsTools/NanoAODTools/postprocessing/interface/ReduceMantissa.h"
#include "../python/PhysicsTools/NanoAODTools/postprocessing/interface/LeptonEfficiencyCorrectorCppWorker.h"

PyJetResolutionWrapper jetRes;
PyJetResolutionScaleFactorWrapper jetResScaleFactor;
PyJetParametersWrapper jetParams;
WeightCalculatorFromHistogram wcalc;
ReduceMantissaToNbitsRounding red(12);
LeptonEfficiencyCorrectorCppWorker lepSF;