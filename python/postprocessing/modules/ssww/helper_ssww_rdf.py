import argparse
import ROOT
import SAMPLE

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-y','--year', help='which year, default is 2016', default= '2016', choices=('2016','2017','2018'))
parser.add_argument('-i','--input', help='input path', default= '/eos/user/l/llinwei/jie/ssww_ntuple/')
parser.add_argument('-t','--theory', help='get the theoretic un certainty',action='store_false', default= True)
parser.add_argument('-x','--xsweight', help='get xs scale factor',action='store_false', default= True)
args = parser.parse_args()

ROOT.ROOT.EnableImplicitMT()


def theory_unc(df):
    #df = ROOT.ROOT.RDataFrame("Events", files)
    print(">>>>>>>>>>>>>>>>>>>> theoretic uncertainty")
    # some samples doesn't have theoretic uncertainty
    branch_list=df.GetColumnNames()
    if not "nLHEPdfWeight" in branch_list:
        return df
    df_unc=df.Define('qcd_unc','float sum=0;for(int i=0; i < nLHEPdfWeight; i++){sum += LHEPdfWeight[i];};\
                      float mean=sum/nLHEPdfWeight;sum=0;for(int i=0; i < nLHEPdfWeight; i++){sum+=LHEPdfWeight[i]*LHEPdfWeight[i];};\
                      return sqrt((sum-nLHEPdfWeight*mean*mean)/(nLHEPdfWeight-1));')\
             .Define('scale_unc','float Max=LHEScaleWeight[0],Min=LHEScaleWeight[0],central=LHEScaleWeight[4];\
                      for(int i=0; i < nLHEScaleWeight; i++){\
                      if(i!=2 || i!=6){if(Max<LHEScaleWeight[i]){Max=LHEScaleWeight[i];};if(Min>LHEScaleWeight[i]){Min=LHEScaleWeight[i];};};};\
                      return max(abs(Max-central),abs(Min-central))/central;')
    return df_unc


def xs_weight(_year, sample, df, n_weighted_events):
    print(">>>>>>>>>>>>>>>>>>>> xs weight of %s") % sample
    input='../../../../crab/'
    sample_sub=sample.strip('.root')
    lumi=SAMPLE.get_lumi(_year)
    with open(input+'xs_' + _year + '_nano_v4.py', 'r') as collect:
        exec (collect)
    _XSDB = XSDB
    try:
        weight=_XSDB[sample_sub]['xs']*_XSDB[sample_sub]['kFactor']*lumi*1000/n_weighted_events
    except:
        print("==================== Error: cannot find %s in XSDB") % sample
        assert False
    df_xsweight=df.Define('xsweight','return '+str(weight)+';')
    return df_xsweight


if __name__ == '__main__':
    samples, data_chain, mc_chain = SAMPLE.set_samples(args.year)
    for imc in mc_chain:
        for i in range(len(samples[imc])):
            f=ROOT.TFile(args.input+args.year+'/'+samples[imc][i])
            df = ROOT.ROOT.RDataFrame("Events", f)
            if args.theory:
                df = theory_unc(df)
            if args.xsweight:
                df = xs_weight(args.year,samples[imc][i],df,f.Get("nEventsGenWeighted").GetBinContent(1))

            df.Snapshot("Events", args.input+args.year+'/'+"new"+samples[imc][i])
