import argparse
import os
import ROOT
import SAMPLE

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-y','--year', help='which year, default is 2016', default= '2016', choices=('2016','2017','2018'))
parser.add_argument('-i','--input', help='input path', default= '/home/cmsdas/testuser01/jie/ssww_ntuple/')
#parser.add_argument('-i','--input', help='input path', default= '/eos/user/l/llinwei/jie/ssww_ntuple/')
parser.add_argument('-t','--theory', help='get the theoretic un certainty, default is false',action='store_true', default= False)
parser.add_argument('-x','--xsweight', help='get xs scale factor, default is false',action='store_true', default= False)
parser.add_argument('-f','--fixreal', help='fix the real lepton decision',action='store_true', default= False)
args = parser.parse_args()

ROOT.ROOT.EnableImplicitMT(70)
def remove_text(a, year):
    xs_file_path='../../../../crab/'
    with open(xs_file_path+'xs_' + year + '_nano_v4.py', 'r') as f:
        lines = []  # empty list
        for line in f.readlines():
            lines.append(line)
    with open(xs_file_path+'xs_' + year + '_nano_v4.py', 'w') as f:
        for line in lines:
            if not (a in line):
                f.write('%s' % line)


if __name__ == '__main__':
    samples, data_chain, mc_chain = SAMPLE.set_samples(args.year)
    for imc in mc_chain:
        for i in range(0,len(samples[imc])):
            # xs weight must go the first, or the input name will change
            if args.xsweight:
                if not os.path.exists('xs_' + args.year + '_nano_v4_v1.py'):
                    collect = open('xs_' + args.year + '_nano_v4_v1.py', "w")
                    collect.write('XSDB = {} \n')
                    collect.close()
                else:
                    pass

                f=ROOT.TFile(args.input+args.year+'/'+samples[imc][i],'update')
                xs_file_path='../../../../crab/'
                sample_sub=samples[imc][i].strip('.root')
                lumi=SAMPLE.get_lumi(args.year)
                with open(xs_file_path+'xs_' + args.year + '_nano_v4.py', 'r') as collect:
                    exec (collect)
                _XSDB = XSDB
                #print _XSDB
                try:
                    weight=_XSDB[sample_sub]['xs']*_XSDB[sample_sub]['kFactor']*lumi*1000/(f.Get("nEventsGenWeighted").GetBinContent(1))
                    print '>>>>>>>>>>>>>>>>>>>> xs weight for %s: %s' % (samples[imc][i],weight)
                except:
                    print("==================== Error: cannot find %s in XSDB") % samples[imc][i]
                    assert False
                _XSDB[sample_sub]['xsweight']=weight
                new = 'XSDB[\"' + sample_sub + '\"] = ' + str(_XSDB[sample_sub]) + '\n'
                with open('xs_' + args.year + '_nano_v4_v1.py', 'a+') as collect:
                    collect.write(new)
                #h_xsweight=ROOT.TH1D('xsweight','xsweight',1,0,1)
                #h_xsweight.SetBinContent(1,weight)
                #h_xsweight.Write()
                f.Close()
            if args.fixreal:
                df = ROOT.ROOT.RDataFrame("Events", args.input+args.year+'/'+samples[imc][i])
                df01=df.Filter("nGenJet>0").Define("lepton_real_new","bool lepton_real_new[nlepton];for(int i=0; i<nlepton; i++){for(int j=0; j<nGenJet; j++){if(GenPart_pt[j]>5 && abs(GenPart_pdgId[j])==abs(lepton_pdg_id[i]) && (GenPart_statusFlags==0 || GenPart_statusFlags==6) && (sqrt(pow(lepton_eta[i] - GenPart_pt_eta[j], 2) + pow(abs(abs(lepton_phi[i] - GenPart_phi[j])-TMath::Pi())-TMath::Pi(), 2)) < 0.3)){lepton_real_new[i]=true;} else{lepton_real_new[i]=false;};}}; return lepton_real_new;")
                df01.Snapshot("Events",args.input+args.year+'/fix_'+samples[imc][i])
            # theoretic uncertainties using nanoAOD framework
            if args.theory:
                print '>>>>>>>>>>>>>>>>>>>> theoretic uncertainty for %s' % samples[imc][i]
                run_command='python ../../../../scripts/nano_postproc.py '
                run_command+=args.input+args.year+' '
                run_command+=args.input+args.year+'/'+samples[imc][i]
                run_command+=' -I PhysicsTools.NanoAODTools.postprocessing.modules.ssww.helper_ssww helper_thoeretic -s _thoeretic'
                os.system(run_command)
                # python ../../../../scripts/nano_postproc.py . /afs/cern.ch/work/j/jixiao/nano/2016/CMSSW_10_2_13/src/PhysicsTools/NanoAODTools/2016_WZ_nanoAOD.root -I PhysicsTools.NanoAODTools.postprocessing.modules.ssww.helper_ssww helper_thoeretic -s _thoeretic