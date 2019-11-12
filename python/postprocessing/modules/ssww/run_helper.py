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
parser.add_argument('-s','--skim', help='do 1st skim, default is false',action='store_true', default= False)
#parser.add_argument('-tr','--trigger', help='trigger maker, default is false',action='store_true', default= False)
parser.add_argument('-post','--poststep', help='declare poststep path postfix', default= 'skim')
parser.add_argument('-pre','--prestep', help='declare prestep path postfix', default= '')
args = parser.parse_args()

ROOT.ROOT.EnableImplicitMT(32)

# Include necessary header
#run_helper_header_path = os.environ['CMSSW_BASE'] + "/python/PhysicsTools/NanoAODTools/postprocessing/modules/ssww/run_helper_python.h"
run_helper_header_path = "run_helper_python.h"

ROOT.gInterpreter.Declare('#include "{}"'.format(run_helper_header_path))

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

                f=ROOT.TFile(args.input+args.year+'/'+samples[imc][i])
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
            '''
            if args.fixreal:
                df = ROOT.ROOT.RDataFrame("Events", args.input+args.year+'/'+samples[imc][i])
                df01=df.Filter("nGenPart>0").Define("lepton_real_new","lepton_real_code(nlepton,lepton_pdg_id,lepton_pt,lepton_eta,lepton_phi,nGenPart,GenPart_pdgId,GenPart_pt,GenPart_statusFlags,GenPart_eta,GenPart_phi)")
                df01.Snapshot("Events",args.input+args.year+'/fix_'+samples[imc][i])
            '''
            # theoretic uncertainties using nanoAOD framework
            if args.theory:
                print '>>>>>>>>>>>>>>>>>>>> theoretic uncertainty for %s' % samples[imc][i]
                run_command='python ../../../../scripts/nano_postproc.py '
                run_command+=args.input+args.year+' '
                run_command+=args.input+args.year+'/'+samples[imc][i]
                run_command+=' -I PhysicsTools.NanoAODTools.postprocessing.modules.ssww.helper_ssww helper_thoeretic -s _thoeretic'
                os.system(run_command)
                # python ../../../../scripts/nano_postproc.py . /afs/cern.ch/work/j/jixiao/nano/2016/CMSSW_10_2_13/src/PhysicsTools/NanoAODTools/2016_WZ_nanoAOD.root -I PhysicsTools.NanoAODTools.postprocessing.modules.ssww.helper_ssww helper_thoeretic -s _thoeretic
            if args.skim:
                print '>>>>>>>>>>>>>>>>>>>> skim %s' % samples[imc][i]
                df = ROOT.ROOT.RDataFrame("Events", args.input+args.year+'/'+args.prestep+'/'+samples[imc][i])
                if args.poststep=='skim':
                    # lepton pt > 20, jet pt > 30
                    df1 = df.Filter("nlepton>1 && njet>1") \
                        .Filter("lepton_pt[0]>20 || lepton_corrected_pt[0]>20 || lepton_correctedUp_pt[0]>20 || lepton_correctedDown_pt[0]>20","cut lep1_pt") \
                        .Filter("lepton_pt[1]>20 || lepton_corrected_pt[1]>20 || lepton_correctedUp_pt[1]>20 || lepton_correctedDown_pt[1]>20","cut lep2_pt") \
                        .Filter("jet_pt[0]>30 || jet_pt_nom[0]>30 || jet_pt_jerUp[0]>30 || jet_pt_jesTotalUp[0]>30 || jet_pt_jerDown[0]>30 || jet_pt_jesTotalDown[0]>30","cut jet1_pt") \
                        .Filter("jet_pt[1]>30 || jet_pt_nom[1]>30 || jet_pt_jerUp[1]>30 || jet_pt_jesTotalUp[1]>30 || jet_pt_jerDown[1]>30 || jet_pt_jesTotalDown[1]>30","cut jet2_pt")
                    # new variable for mjj w.r.t jes jer
                    df2 = df1.Define("mjj_nom","calc_mjj(jet_pt_nom[0],jet_eta[0],jet_phi[0],jet_mass_nom[0],jet_pt_nom[1],jet_eta[1],jet_phi[1],jet_mass_nom[1])") \
                                .Define("mjj_jerUp","calc_mjj(jet_pt_jerUp[0],jet_eta[0],jet_phi[0],jet_mass_jerUp[0],jet_pt_jerUp[1],jet_eta[1],jet_phi[1],jet_mass_jerUp[1])") \
                                .Define("mjj_jerDown","calc_mjj(jet_pt_jerDown[0],jet_eta[0],jet_phi[0],jet_mass_jerDown[0],jet_pt_jerDown[1],jet_eta[1],jet_phi[1],jet_mass_jerDown[1])") \
                                .Define("mjj_jesTotalUp","calc_mjj(jet_pt_jesTotalUp[0],jet_eta[0],jet_phi[0],jet_mass_jesTotalUp[0],jet_pt_jesTotalUp[1],jet_eta[1],jet_phi[1],jet_mass_jesTotalUp[1])") \
                                .Define("mjj_jesTotalDown","calc_mjj(jet_pt_jesTotalDown[0],jet_eta[0],jet_phi[0],jet_mass_jesTotalDown[0],jet_pt_jesTotalDown[1],jet_eta[1],jet_phi[1],jet_mass_jesTotalDown[1])")
                elif args.poststep=='skim_l1':
                    print '>>>>> skim_l1'
                    df2 = df.Filter('nlepton==1','common cuts for one lepton')
                elif args.poststep=='skim_l2':
                    df2 = df.Filter("nlepton==2").Filter("met > 30 && mll > 20 && (mjj > 100 || mjj_nom > 100 || mjj_jerUp > 100 || mjj_jerDown > 100 || mjj_jesTotalUp > 100 || mjj_jesTotalDown > 100)","common cuts for two leptons")
                elif args.poststep=='skim_l3':
                    df2 = df.Filter('nlepton==3','common cuts for three leptons')
                    #df2 = df1.Filter("lepton_pt[2]>10 || lepton_corrected_pt[2]>10 || lepton_correctedUp_pt[2]>10 || lepton_correctedDown_pt[2]>10","cut lep2_pt")
                elif args.poststep=='skim_l4':
                    df2 = df.Filter('nlepton==4','common cuts for four leptons')
                    #df2 = df1.Filter("lepton_pt[2]>10 || lepton_corrected_pt[2]>10 || lepton_correctedUp_pt[2]>10 || lepton_correctedDown_pt[2]>10","cut lep2_pt")
                else:
                    assert(0)
                if not os.path.exists(args.input+'/'+args.year+'/'+args.prestep):
                    os.mkdir(args.input+'/'+args.year+'/'+args.prestep)
                df2.Snapshot("Events",args.input+'/'+args.year+'/'+args.prestep+'/'+samples[imc][i])
                allCutsReport = df.Report()
                allCutsReport.Print()


    for idata in data_chain:
        for i in range(0,len(samples[idata])):
            if args.skim:
                print '>>>>>>>>>>>>>>>>>>>> skim %s' % samples[idata][i]
                df = ROOT.ROOT.RDataFrame("Events", args.input+args.year+'/'+args.prestep+'/'+samples[idata][i])
                if args.poststep=='skim':
                    branch_list=df.GetColumnNames()
                    # trigger cut
                    if 'MuonEG' in idata:
                        trigger_cut=SAMPLE.trigger_maker(args.year,branch_list,"MuonEG")  # type: str
                    elif 'SingleMuon' in idata:
                        trigger_cut=SAMPLE.trigger_maker(args.year,branch_list,"SingleMuon")
                    elif 'SingleElectron' in idata:
                        trigger_cut=SAMPLE.trigger_maker(args.year,branch_list,"SingleElectron")
                    elif 'DoubleMuon' in idata:
                        trigger_cut=SAMPLE.trigger_maker(args.year,branch_list,"DoubleMuon")
                    elif 'DoubleEG' in idata:
                        trigger_cut=SAMPLE.trigger_maker(args.year,branch_list,"DoubleEG")
                    elif 'EGamma' in idata:
                        trigger_cut=SAMPLE.trigger_maker(args.year,branch_list,"EGamma")
                    df1=df.Filter(trigger_cut,"trigger cut")
                    # lepton pt > 20, jet pt > 30
                    df2 = df1.Filter("nlepton>1 && njet>1") \
                        .Filter("lepton_pt[0]>20 || lepton_corrected_pt[0]>20 || lepton_correctedUp_pt[0]>20 || lepton_correctedDown_pt[0]>20","cut lep1_pt") \
                        .Filter("lepton_pt[1]>20 || lepton_corrected_pt[1]>20 || lepton_correctedUp_pt[1]>20 || lepton_correctedDown_pt[1]>20","cut lep2_pt") \
                        .Filter("jet_pt[0]>30","cut jet1_pt") \
                        .Filter("jet_pt[1]>30","cut jet2_pt")
                elif args.poststep=='skim_l2':
                    df2 = df.Filter("nlepton==2").Filter("met > 30 && mll > 20 && (mjj > 100 || mjj_nom > 100 || mjj_jerUp > 100 || mjj_jerDown > 100 || mjj_jesTotalUp > 100 || mjj_jesTotalDown > 100)","common cuts for two leptons")
                elif args.poststep=='skim_l3':
                    df2 = df.Filter('nlepton==3','common cuts for three leptons')
                    #df2 = df1.Filter("lepton_pt[2]>10 || lepton_corrected_pt[2]>10 || lepton_correctedUp_pt[2]>10 || lepton_correctedDown_pt[2]>10","cut lep2_pt")
                elif args.poststep=='skim_l4':
                    df2 = df.Filter('nlepton==4','common cuts for four leptons')
                    #df2 = df1.Filter("lepton_pt[2]>10 || lepton_corrected_pt[2]>10 || lepton_correctedUp_pt[2]>10 || lepton_correctedDown_pt[2]>10","cut lep2_pt")

                if not os.path.exists(args.input+'/'+args.year+'/'+args.prestep):
                    os.mkdir(args.input+'/'+args.year+'/'+args.prestep)
                df2.Snapshot("Events",args.input+'/'+args.year+'/'+args.prestep+'/'+samples[idata][i])
                allCutsReport = df.Report()
                allCutsReport.Print()
