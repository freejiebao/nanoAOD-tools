import argparse
import os
import ROOT
import SAMPLE

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-y','--year', help='which year, default is 2016', default= '2016', choices=('2016','2017','2018'))
parser.add_argument('-i','--input', help='input path', default= '/eos/user/l/llinwei/jie/ssww_ntuple/')
parser.add_argument('-t','--theory', help='get the theoretic un certainty',action='store_false', default= True)
parser.add_argument('-x','--xsweight', help='get xs scale factor',action='store_false', default= True)
args = parser.parse_args()

ROOT.ROOT.EnableImplicitMT()

if __name__ == '__main__':
    samples, data_chain, mc_chain = SAMPLE.set_samples(args.year)
    for imc in mc_chain:
        for i in range(len(samples[imc])):
            # xs weight must go the first, or the input name will change
            if args.xsweight:
                f=ROOT.TFile(args.input+args.year+'/'+samples[imc][i],'update')
                xs_file_path='../../../../crab/'
                sample_sub=samples[imc][i].strip('.root')
                lumi=SAMPLE.get_lumi(args.year)
                with open(xs_file_path+'xs_' + args.year + '_nano_v4.py', 'r') as collect:
                    exec (collect)
                _XSDB = XSDB
                try:
                    weight=_XSDB[sample_sub]['xs']*_XSDB[sample_sub]['kFactor']*lumi*1000/(f.Get("nEventsGenWeighted").GetBinContent(1))
                except:
                    print("==================== Error: cannot find %s in XSDB") % sample
                    assert False
                h_xsweight=ROOT.TH1D('xsweight','xsweight',1,0,1)
                h_xsweight.SetBinContent(1,weight)
                h_xsweight.Write()
                f.Close()

            # theoretic uncertainties using nanoAOD framework
            if args.theory:
                run_command='python ../../../../scripts/nano_postproc.py '
                run_command+=args.input+args.year+'/theoretic/ '
                run_command+=args.input+args.year+'/'+samples[imc][i]
                run_command+=' -I PhysicsTools.NanoAODTools.postprocessing.modules.ssww.helper_ssww helper_thoeretic --bi ../scripts/keep_and_drop_theoretic.txt -s _thoeretic'
                os.system(run_command)
