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