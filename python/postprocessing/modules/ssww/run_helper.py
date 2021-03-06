import argparse
import os
import ROOT
import SAMPLE
import datetime

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-y','--year', help='which year, default is 2016', default= '2016', choices=('2016','2017','2018'))
parser.add_argument('-i','--input', help='input path', default= '/home/cmsdas/testuser01/jie/ssww_ntuple/')
#parser.add_argument('-i','--input', help='input path', default= '/eos/user/l/llinwei/jie/ssww_ntuple/')
parser.add_argument('-t','--theory', help='get the theoretic un certainty, default is false',action='store_true', default= False)
parser.add_argument('-x','--xsweight', help='get xs scale factor, default is false',action='store_true', default= False)
parser.add_argument('-s','--skim', help='do 1st skim, default is false',action='store_true', default= False)
parser.add_argument('-e','--eff_sf', help='calculate efficiency sf for electron and muon, default is false',action='store_true', default= False)
parser.add_argument('-f','--fake_weight', help='calculate fake weight for each event, default is false',action='store_true', default= False)
#parser.add_argument('-tr','--trigger', help='trigger maker, default is false',action='store_true', default= False)
parser.add_argument('-post','--poststep', help='declare poststep path postfix', default= 'skim')
parser.add_argument('-pre','--prestep', help='declare prestep path postfix', default= '')
args = parser.parse_args()

ROOT.ROOT.EnableImplicitMT(32)

# Include necessary header
#run_helper_header_path = os.environ['CMSSW_BASE'] + "/python/PhysicsTools/NanoAODTools/postprocessing/modules/ssww/run_helper_python.h"
run_helper_header_path = "run_helper_python.h"

ROOT.gInterpreter.Declare('#include "{}"'.format(run_helper_header_path))

def DropColumns(column_list,drop_branches):
    branchList = ROOT.vector('string')()
    for i in range(0,len(column_list)):
        if not (column_list[i] in drop_branches):
            branchList.push_back(column_list[i])
    #for i in range(0,len(branchList)):
    #    print branchList[i]
    return branchList

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
    with open('no_events_'+ args.year + '.txt','a') as f:
        f.write('date: {} \n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

    for imc in mc_chain:
        for i in range(0,len(samples[imc])):
            # xs weight must go the first, or the input name will change
            if args.xsweight:
                tmp_path='/tmp/jixiao%s/' % args.year
                if not os.path.exists(tmp_path):
                    os.mkdir(tmp_path)
                print('>>>>>>>>>>>>>>>>>>>> xsweight {}'.format(samples[imc][i]))
                f=ROOT.TFile.Open(args.input+args.year+'/'+args.prestep+'/'+samples[imc][i])
                if not hasattr(f,"Events"):
                    print("==================== Cannot find tree with name Events in {}".format(f))
                    with open('no_events_'+ args.year + '.txt','a') as wirtefile:
                        wirtefile.write('{}\n'.format(f))
                    continue
                df = ROOT.ROOT.RDataFrame("Events",f)
                brach_list=df.GetColumnNames()
                if ("xsweight" in brach_list):
                    print("==================== Warning: xsweight already exist in {}, please check".format(samples[imc][i]))
                    continue
                '''
                if not os.path.exists('xs_' + args.year + '_nano_v4_v1.py'):
                    collect = open('xs_' + args.year + '_nano_v4_v1.py', "w")
                    collect.write('XSDB = {} \n')
                    collect.close()
                else:
                    pass
                '''
                xs_file_path='../../../../crab/'
                sample_sub=samples[imc][i].strip('.root')
                lumi=SAMPLE.get_lumi(args.year)
                with open(xs_file_path+'xs_' + args.year + '_nano_v4.py', 'r') as collect:
                    exec (collect)
                _XSDB = XSDB
                #print _XSDB
                try:
                    weight=_XSDB[sample_sub]['xs']*_XSDB[sample_sub]['kFactor']*lumi*1000/(f.Get("nEventsGenWeighted").GetBinContent(1))
                    df1=df.Define('xsweight',str(weight)+'*(gen_weight/abs(gen_weight))')
                    df1.Snapshot("Events",tmp_path+'/'+samples[imc][i],DropColumns(df1.GetColumnNames(),['gen_weight']))
                    f.Close()
                    os.system('mv ' +tmp_path+'/'+samples[imc][i]+' '+args.input+args.year+'/'+args.prestep)
                    print('>>>>>>>>>>>>>>>>>>>> xs weight for {}: {}'.format(samples[imc][i],weight))
                except:
                    print("==================== Error: cannot find {} in XSDB".format(samples[imc][i]))
                    f.Close()
                    assert False
                '''
                _XSDB[sample_sub]['xsweight']=weight
                new = 'XSDB[\"' + sample_sub + '\"] = ' + str(_XSDB[sample_sub]) + '\n'
                with open('xs_' + args.year + '_nano_v4_v1.py', 'a+') as collect:
                    collect.write(new)
                '''

            if args.eff_sf:
                if not os.path.exists(args.input+'/'+args.year+'/'+args.poststep):
                    print("==================== Error: directory does not exist: {}".format(args.input+'/'+args.year+'/'+args.poststep))
                    assert False
                if not os.path.exists(args.input+args.year+'/'+args.poststep+'/'+samples[imc][i]):
                    continue
                f=ROOT.TFile.Open(args.input+args.year+'/'+args.poststep+'/'+samples[imc][i])
                if not hasattr(f,"Events"):
                    print("==================== Cannot find tree with name Events in {}".format(f))
                    with open('no_events_'+ args.year + '.txt','a') as wirtefile:
                        wirtefile.write('{}\n'.format(f))
                    continue
                df = ROOT.ROOT.RDataFrame("Events",f)
                brach_list=df.GetColumnNames()
                if ("lepton_sf" in brach_list) or ("lepton_sf_up" in brach_list) or ("lepton_sf_down" in brach_list):
                    print("==================== Warning: lepton_sf already exist in {}, please check".format(samples[imc][i]))
                    continue
                print(">>>>> eff sf: {}".format(samples[imc][i]))
                df1=df.Define("lepton_sf","efficiency_scale_factor(lepton_pt,lepton_eta,lepton_pdgId,\""+args.year+"\",\"nom\")")\
                    .Define("lepton_sf_muon_id_up","efficiency_scale_factor(lepton_pt,lepton_eta,lepton_pdgId,\""+args.year+"\",\"muon_id_up\")")\
                    .Define("lepton_sf_muon_id_down","efficiency_scale_factor(lepton_pt,lepton_eta,lepton_pdgId,\""+args.year+"\",\"muon_id_down\")")\
                    .Define("lepton_sf_muon_iso_up","efficiency_scale_factor(lepton_pt,lepton_eta,lepton_pdgId,\""+args.year+"\",\"muon_iso_up\")")\
                    .Define("lepton_sf_muon_iso_down","efficiency_scale_factor(lepton_pt,lepton_eta,lepton_pdgId,\""+args.year+"\",\"muon_iso_down\")") \
                    .Define("lepton_sf_electron_id_up","efficiency_scale_factor(lepton_pt,lepton_eta,lepton_pdgId,\""+args.year+"\",\"electron_id_up\")") \
                    .Define("lepton_sf_electron_id_down","efficiency_scale_factor(lepton_pt,lepton_eta,lepton_pdgId,\""+args.year+"\",\"electron_id_down\")") \
                    .Define("lepton_sf_electron_reco_up","efficiency_scale_factor(lepton_pt,lepton_eta,lepton_pdgId,\""+args.year+"\",\"electron_reco_up\")") \
                    .Define("lepton_sf_electron_reco_down","efficiency_scale_factor(lepton_pt,lepton_eta,lepton_pdgId,\""+args.year+"\",\"electron_reco_down\")")
                #df1=df.Define("lepton_sf","efficiency_scale_factor(lepton_pt,lepton_eta,\""+args.year+"\",\"nom\")")
                tmp_path='/tmp/jixiao%s/' % args.year
                if not os.path.exists(tmp_path):
                    os.mkdir(tmp_path)
                df1.Snapshot("Events",tmp_path+'/'+samples[imc][i],DropColumns(df1.GetColumnNames(),[]))
                os.system('mv ' +tmp_path+'/'+samples[imc][i]+' '+args.input+args.year+'/'+args.poststep)

            if args.fake_weight:
                if not os.path.exists(args.input+'/'+args.year+'/'+args.poststep):
                    print("==================== Error: directory does not exist: {}".format(args.input+'/'+args.year+'/'+args.poststep))
                    assert False

                f=ROOT.TFile.Open(args.input+args.year+'/'+args.poststep+'/'+samples[imc][i])
                if not hasattr(f,"Events"):
                    print("==================== Cannot find tree with name Events in {}".format(f))
                    with open('no_events_'+ args.year + '.txt','a') as wirtefile:
                        wirtefile.write('{}\n'.format(f))
                    continue
                df = ROOT.ROOT.RDataFrame("Events",f)
                brach_list=df.GetColumnNames()
                if ("lepton_fake_weight" in brach_list):
                    print("==================== Warning: lepton_fake_weight already exist in {}, please check".format(samples[imc][i]))
                    continue
                print(">>>>> fake weight: {}".format(samples[imc][i]))
                df1=df.Define("lepton_fake_weight","get_fake_lepton_weight(lepton_fakeable,lepton_tight,lepton_pt,lepton_eta,lepton_pdgId,\""+args.year+"\",\"nominal\")") \
                    .Define("lepton_fake_weight_up","get_fake_lepton_weight(lepton_fakeable,lepton_tight,lepton_pt,lepton_eta,lepton_pdgId,\""+args.year+"\",\"up\")")\
                    .Define("lepton_fake_weight_down","get_fake_lepton_weight(lepton_fakeable,lepton_tight,lepton_pt,lepton_eta,lepton_pdgId,\""+args.year+"\",\"down\")")

                tmp_path='/tmp/jixiao%s/' % args.year
                if not os.path.exists(tmp_path):
                    os.mkdir(tmp_path)
                df1.Snapshot("Events",tmp_path+'/'+samples[imc][i],DropColumns(df1.GetColumnNames(),[]))
                os.system('mv ' +tmp_path+'/'+samples[imc][i]+' '+args.input+args.year+'/'+args.poststep)

            # theoretic uncertainties using nanoAOD framework
            if args.theory:
                print('>>>>>>>>>>>>>>>>>>>> theoretic uncertainty for {}'.format(samples[imc][i]))
                run_command='python ../../../../scripts/nano_postproc.py '
                run_command+=args.input+args.year+' '
                run_command+=args.input+args.year+'/'+samples[imc][i]
                run_command+=' -I PhysicsTools.NanoAODTools.postprocessing.modules.ssww.helper_ssww helper_thoeretic -s _thoeretic'
                os.system(run_command)
                # python ../../../../scripts/nano_postproc.py . /afs/cern.ch/work/j/jixiao/nano/2016/CMSSW_10_2_13/src/PhysicsTools/NanoAODTools/2016_WZ_nanoAOD.root -I PhysicsTools.NanoAODTools.postprocessing.modules.ssww.helper_ssww helper_thoeretic -s _thoeretic
            if args.skim:
                print('>>>>>>>>>>>>>>>>>>>> skim {}'.format(samples[imc][i]))
                f=ROOT.TFile.Open(args.input+args.year+'/'+args.prestep+'/'+samples[imc][i])
                if not hasattr(f,"Events"):
                    print("==================== Cannot find tree with name Events in {}".format(f))
                    with open('no_events_'+ args.year + '.txt','a') as wirtefile:
                        wirtefile.write('{}\n'.format(f))
                    continue
                df = ROOT.ROOT.RDataFrame("Events", f)
                if args.poststep=='skim':
                    # lepton pt > 20, jet pt > 30
                    df1 = df.Filter("nlepton>1") \
                        .Filter("lepton_pt[0]>25 || lepton_corrected_pt[0]>25 || lepton_correctedUp_pt[0]>25 || lepton_correctedDown_pt[0]>25","cut lep1_pt") \
                        .Filter("lepton_pt[1]>20 || lepton_corrected_pt[1]>20 || lepton_correctedUp_pt[1]>20 || lepton_correctedDown_pt[1]>20","cut lep2_pt") \
                        .Filter("(MET_pt > 30 || MET_pt_nom>30 || MET_pt_jerUp>30 || MET_pt_jerDown>30 || MET_pt_jesTotalUp >30 || MET_pt_jesTotalDown >30)")\
                        .Filter("jet_pt[0]>30 || jet_pt_nom[0]>30 || jet_pt_jerUp[0]>30 || jet_pt_jesTotalUp[0]>30 || jet_pt_jerDown[0]>30 || jet_pt_jesTotalDown[0]>30","cut jet1_pt") \
                        .Filter("jet_pt[1]>30 || jet_pt_nom[1]>30 || jet_pt_jerUp[1]>30 || jet_pt_jesTotalUp[1]>30 || jet_pt_jerDown[1]>30 || jet_pt_jesTotalDown[1]>30","cut jet2_pt")
                    # new variable for mjj w.r.t jes jer
                    df2 = df1.Define("mjj_nom","calc_mjj(jet_pt_nom[0],jet_eta[0],jet_phi[0],jet_mass_nom[0],jet_pt_nom[1],jet_eta[1],jet_phi[1],jet_mass_nom[1])") \
                        .Define("mjj_jerUp","calc_mjj(jet_pt_jerUp[0],jet_eta[0],jet_phi[0],jet_mass_jerUp[0],jet_pt_jerUp[1],jet_eta[1],jet_phi[1],jet_mass_jerUp[1])") \
                        .Define("mjj_jerDown","calc_mjj(jet_pt_jerDown[0],jet_eta[0],jet_phi[0],jet_mass_jerDown[0],jet_pt_jerDown[1],jet_eta[1],jet_phi[1],jet_mass_jerDown[1])") \
                        .Define("mjj_jesTotalUp","calc_mjj(jet_pt_jesTotalUp[0],jet_eta[0],jet_phi[0],jet_mass_jesTotalUp[0],jet_pt_jesTotalUp[1],jet_eta[1],jet_phi[1],jet_mass_jesTotalUp[1])") \
                        .Define("mjj_jesTotalDown","calc_mjj(jet_pt_jesTotalDown[0],jet_eta[0],jet_phi[0],jet_mass_jesTotalDown[0],jet_pt_jesTotalDown[1],jet_eta[1],jet_phi[1],jet_mass_jesTotalDown[1])")
                        #.Define("mll_corrected","calc_mjj(jet_pt_jesTotalDown[0],jet_eta[0],jet_phi[0],jet_mass_jesTotalDown[0],jet_pt_jesTotalDown[1],jet_eta[1],jet_phi[1],jet_mass_jesTotalDown[1])") \
                        #.Define("mll_correctedUp","calc_mjj(jet_pt_jesTotalDown[0],jet_eta[0],jet_phi[0],jet_mass_jesTotalDown[0],jet_pt_jesTotalDown[1],jet_eta[1],jet_phi[1],jet_mass_jesTotalDown[1])") \
                        #.Define("mll_correctedDown","calc_mjj(jet_pt_jesTotalDown[0],jet_eta[0],jet_phi[0],jet_mass_jesTotalDown[0],jet_pt_jesTotalDown[1],jet_eta[1],jet_phi[1],jet_mass_jesTotalDown[1])")

                elif args.poststep=='skim_l1':
                    print('>>>>> skim_l1')
                    df2 = df.Filter('nlepton==1','common cuts for one lepton')
                elif args.poststep=='skim_l2':
                    print('>>>>> skim_l2')
                    df2 = df.Filter("nlepton==2") \
                        .Filter("lepton_pt[0]>25 || lepton_corrected_pt[0]>25 || lepton_correctedUp_pt[0]>25 || lepton_correctedDown_pt[0]>25","cut lep1_pt") \
                        .Filter("lepton_pt[1]>20 || lepton_corrected_pt[1]>20 || lepton_correctedUp_pt[1]>20 || lepton_correctedDown_pt[1]>20","cut lep2_pt") \
                        .Filter("(MET_pt > 30 || MET_pt_nom>30 || MET_pt_jerUp>30 || MET_pt_jerDown>30 || MET_pt_jesTotalUp >30 || MET_pt_jesTotalDown >30)")
                elif args.poststep=='vbs_l2' and args.prestep=='skim_l2':
                    print('>>>>> skim_l2 -> vbs')
                    df2 = df.Filter("njet>1") \
                        .Filter("jet_pt[0]>30 || jet_pt_nom[0]>30 || jet_pt_jerUp[0]>30 || jet_pt_jesTotalUp[0]>30 || jet_pt_jerDown[0]>30 || jet_pt_jesTotalDown[0]>30","cut jet1_pt") \
                        .Filter("jet_pt[1]>30 || jet_pt_nom[1]>30 || jet_pt_jerUp[1]>30 || jet_pt_jesTotalUp[1]>30 || jet_pt_jerDown[1]>30 || jet_pt_jesTotalDown[1]>30","cut jet2_pt") \
                        .Define("mjj_nom","calc_mjj(jet_pt_nom[0],jet_eta[0],jet_phi[0],jet_mass_nom[0],jet_pt_nom[1],jet_eta[1],jet_phi[1],jet_mass_nom[1])") \
                        .Define("mjj_jerUp","calc_mjj(jet_pt_jerUp[0],jet_eta[0],jet_phi[0],jet_mass_jerUp[0],jet_pt_jerUp[1],jet_eta[1],jet_phi[1],jet_mass_jerUp[1])") \
                        .Define("mjj_jerDown","calc_mjj(jet_pt_jerDown[0],jet_eta[0],jet_phi[0],jet_mass_jerDown[0],jet_pt_jerDown[1],jet_eta[1],jet_phi[1],jet_mass_jerDown[1])") \
                        .Define("mjj_jesTotalUp","calc_mjj(jet_pt_jesTotalUp[0],jet_eta[0],jet_phi[0],jet_mass_jesTotalUp[0],jet_pt_jesTotalUp[1],jet_eta[1],jet_phi[1],jet_mass_jesTotalUp[1])") \
                        .Define("mjj_jesTotalDown","calc_mjj(jet_pt_jesTotalDown[0],jet_eta[0],jet_phi[0],jet_mass_jesTotalDown[0],jet_pt_jesTotalDown[1],jet_eta[1],jet_phi[1],jet_mass_jesTotalDown[1])") \
                        .Filter("(mjj > 500 || mjj_nom > 500 || mjj_jerUp > 500 || mjj_jerDown > 500 || mjj_jesTotalUp > 500 || mjj_jesTotalDown > 500)","common cuts for two jets")
                elif args.poststep=='lowmjj_l2' and args.prestep=='skim_l2':
                    print('>>>>> skim_l2 -> lowmjj')
                    df2 = df.Filter("njet>1") \
                        .Filter("jet_pt[0]>30 || jet_pt_nom[0]>30 || jet_pt_jerUp[0]>30 || jet_pt_jesTotalUp[0]>30 || jet_pt_jerDown[0]>30 || jet_pt_jesTotalDown[0]>30","cut jet1_pt") \
                        .Filter("jet_pt[1]>30 || jet_pt_nom[1]>30 || jet_pt_jerUp[1]>30 || jet_pt_jesTotalUp[1]>30 || jet_pt_jerDown[1]>30 || jet_pt_jesTotalDown[1]>30","cut jet2_pt") \
                        .Define("mjj_nom","calc_mjj(jet_pt_nom[0],jet_eta[0],jet_phi[0],jet_mass_nom[0],jet_pt_nom[1],jet_eta[1],jet_phi[1],jet_mass_nom[1])") \
                        .Define("mjj_jerUp","calc_mjj(jet_pt_jerUp[0],jet_eta[0],jet_phi[0],jet_mass_jerUp[0],jet_pt_jerUp[1],jet_eta[1],jet_phi[1],jet_mass_jerUp[1])") \
                        .Define("mjj_jerDown","calc_mjj(jet_pt_jerDown[0],jet_eta[0],jet_phi[0],jet_mass_jerDown[0],jet_pt_jerDown[1],jet_eta[1],jet_phi[1],jet_mass_jerDown[1])") \
                        .Define("mjj_jesTotalUp","calc_mjj(jet_pt_jesTotalUp[0],jet_eta[0],jet_phi[0],jet_mass_jesTotalUp[0],jet_pt_jesTotalUp[1],jet_eta[1],jet_phi[1],jet_mass_jesTotalUp[1])") \
                        .Define("mjj_jesTotalDown","calc_mjj(jet_pt_jesTotalDown[0],jet_eta[0],jet_phi[0],jet_mass_jesTotalDown[0],jet_pt_jesTotalDown[1],jet_eta[1],jet_phi[1],jet_mass_jesTotalDown[1])") \
                        .Filter("(mjj < 500 || mjj_nom < 500 || mjj_jerUp < 500 || mjj_jerDown < 500 || mjj_jesTotalUp < 500 || mjj_jesTotalDown < 500)","common cuts for two jets 1") \
                        .Filter("(mjj > 100 || mjj_nom > 100 || mjj_jerUp > 100 || mjj_jerDown > 100 || mjj_jesTotalUp > 100 || mjj_jesTotalDown > 100)","common cuts for two jets 2")

                elif args.poststep=='skim_l3':
                    print('>>>>> skim_l3')
                    df2 = df.Filter('nlepton==3','common cuts for three leptons') \
                        .Filter("(MET_pt > 30 || MET_pt_nom>30 || MET_pt_jerUp>30 || MET_pt_jerDown>30 || MET_pt_jesTotalUp >30 || MET_pt_jesTotalDown >30)") \
                        .Define("valid_lepton_order","order_wz(lepton_pdgId,lepton_pt,lepton_eta,lepton_phi,lepton_mass)") \
                        .Filter("valid_lepton_order[0]>0","WZ selections") \
                        .Define("ml1l2","invariant_mass_wz(valid_lepton_order,lepton_pt,lepton_eta,lepton_phi,lepton_mass,0)") \
                        .Filter("abs(ml1l2-91.1876)<15","in Z pole") \
                        .Define("ml1l3","invariant_mass_wz(valid_lepton_order,lepton_pt,lepton_eta,lepton_phi,lepton_mass,1)") \
                        .Define("ml2l3","invariant_mass_wz(valid_lepton_order,lepton_pt,lepton_eta,lepton_phi,lepton_mass,2)") \
                        .Define("mlll","invariant_mass_wz(valid_lepton_order,lepton_pt,lepton_eta,lepton_phi,lepton_mass,3)")
                elif args.poststep=='vbs_l3' and args.prestep=='skim_l3':
                    print('>>>>> skim_l3 -> vbs')
                    df2 = df.Filter("njet>1") \
                        .Filter("jet_pt[0]>30 || jet_pt_nom[0]>30 || jet_pt_jerUp[0]>30 || jet_pt_jesTotalUp[0]>30 || jet_pt_jerDown[0]>30 || jet_pt_jesTotalDown[0]>30","cut jet1_pt") \
                        .Filter("jet_pt[1]>30 || jet_pt_nom[1]>30 || jet_pt_jerUp[1]>30 || jet_pt_jesTotalUp[1]>30 || jet_pt_jerDown[1]>30 || jet_pt_jesTotalDown[1]>30","cut jet2_pt") \
                        .Define("mjj_nom","calc_mjj(jet_pt_nom[0],jet_eta[0],jet_phi[0],jet_mass_nom[0],jet_pt_nom[1],jet_eta[1],jet_phi[1],jet_mass_nom[1])") \
                        .Define("mjj_jerUp","calc_mjj(jet_pt_jerUp[0],jet_eta[0],jet_phi[0],jet_mass_jerUp[0],jet_pt_jerUp[1],jet_eta[1],jet_phi[1],jet_mass_jerUp[1])") \
                        .Define("mjj_jerDown","calc_mjj(jet_pt_jerDown[0],jet_eta[0],jet_phi[0],jet_mass_jerDown[0],jet_pt_jerDown[1],jet_eta[1],jet_phi[1],jet_mass_jerDown[1])") \
                        .Define("mjj_jesTotalUp","calc_mjj(jet_pt_jesTotalUp[0],jet_eta[0],jet_phi[0],jet_mass_jesTotalUp[0],jet_pt_jesTotalUp[1],jet_eta[1],jet_phi[1],jet_mass_jesTotalUp[1])") \
                        .Define("mjj_jesTotalDown","calc_mjj(jet_pt_jesTotalDown[0],jet_eta[0],jet_phi[0],jet_mass_jesTotalDown[0],jet_pt_jesTotalDown[1],jet_eta[1],jet_phi[1],jet_mass_jesTotalDown[1])") \
                        .Filter("(mjj > 500 || mjj_nom > 500 || mjj_jerUp > 500 || mjj_jerDown > 500 || mjj_jesTotalUp > 500 || mjj_jesTotalDown > 500)","common cuts for two jets") \
                        .Filter("abs(detajj)>2.5")

                    #df2 = df1.Filter("lepton_pt[2]>10 || lepton_corrected_pt[2]>10 || lepton_correctedUp_pt[2]>10 || lepton_correctedDown_pt[2]>10","cut lep2_pt")
                elif args.poststep=='skim_l4':
                    print('>>>>> skim_l4')
                    df2 = df.Filter('nlepton==4','common cuts for four leptons') \
                        .Filter("(MET_pt > 30 || MET_pt_nom>30 || MET_pt_jerUp>30 || MET_pt_jerDown>30 || MET_pt_jesTotalUp >30 || MET_pt_jesTotalDown >30)") \
                        .Define("valid_lepton_order","order_zz(lepton_pdgId,lepton_pt,lepton_eta,lepton_phi,lepton_mass)") \
                        .Define("mZ0","invariant_mass_zz(valid_lepton_order,lepton_pt,lepton_eta,lepton_phi,lepton_mass,0)") \
                        .Define("mZ1","invariant_mass_zz(valid_lepton_order,lepton_pt,lepton_eta,lepton_phi,lepton_mass,1)") \
                        .Define("mllll","invariant_mass_zz(valid_lepton_order,lepton_pt,lepton_eta,lepton_phi,lepton_mass,2)")
                elif args.poststep=='vbs_l4' and args.prestep=='skim_l4':
                    print('>>>>> skim_l4 -> vbs')
                    df2 = df.Filter("njet>1") \
                        .Filter("jet_pt[0]>30 || jet_pt_nom[0]>30 || jet_pt_jerUp[0]>30 || jet_pt_jesTotalUp[0]>30 || jet_pt_jerDown[0]>30 || jet_pt_jesTotalDown[0]>30","cut jet1_pt") \
                        .Filter("jet_pt[1]>30 || jet_pt_nom[1]>30 || jet_pt_jerUp[1]>30 || jet_pt_jesTotalUp[1]>30 || jet_pt_jerDown[1]>30 || jet_pt_jesTotalDown[1]>30","cut jet2_pt") \
                        .Define("mjj_nom","calc_mjj(jet_pt_nom[0],jet_eta[0],jet_phi[0],jet_mass_nom[0],jet_pt_nom[1],jet_eta[1],jet_phi[1],jet_mass_nom[1])") \
                        .Define("mjj_jerUp","calc_mjj(jet_pt_jerUp[0],jet_eta[0],jet_phi[0],jet_mass_jerUp[0],jet_pt_jerUp[1],jet_eta[1],jet_phi[1],jet_mass_jerUp[1])") \
                        .Define("mjj_jerDown","calc_mjj(jet_pt_jerDown[0],jet_eta[0],jet_phi[0],jet_mass_jerDown[0],jet_pt_jerDown[1],jet_eta[1],jet_phi[1],jet_mass_jerDown[1])") \
                        .Define("mjj_jesTotalUp","calc_mjj(jet_pt_jesTotalUp[0],jet_eta[0],jet_phi[0],jet_mass_jesTotalUp[0],jet_pt_jesTotalUp[1],jet_eta[1],jet_phi[1],jet_mass_jesTotalUp[1])") \
                        .Define("mjj_jesTotalDown","calc_mjj(jet_pt_jesTotalDown[0],jet_eta[0],jet_phi[0],jet_mass_jesTotalDown[0],jet_pt_jesTotalDown[1],jet_eta[1],jet_phi[1],jet_mass_jesTotalDown[1])") \
                        .Filter("(mjj > 400 || mjj_nom > 400 || mjj_jerUp > 400 || mjj_jerDown > 400 || mjj_jesTotalUp > 400 || mjj_jesTotalDown > 400)","common cuts for two jets") \
                        .Filter("abs(detajj)>2.4")
                        #df2 = df1.Filter("lepton_pt[2]>10 || lepton_corrected_pt[2]>10 || lepton_correctedUp_pt[2]>10 || lepton_correctedDown_pt[2]>10","cut lep2_pt")
                else:
                    assert(0)
                if not os.path.exists(args.input+'/'+args.year+'/'+args.poststep):
                    os.mkdir(args.input+'/'+args.year+'/'+args.poststep)
                df2.Snapshot("Events",args.input+'/'+args.year+'/'+args.poststep+'/'+samples[imc][i])
                allCutsReport = df.Report()
                allCutsReport.Print()


    for idata in data_chain:
        for i in range(0,len(samples[idata])):
            if args.skim:
                print('>>>>>>>>>>>>>>>>>>>> skim %s') % samples[idata][i]
                f=ROOT.TFile.Open(args.input+args.year+'/'+args.prestep+'/'+samples[idata][i])
                if not hasattr(f,"Events"):
                    print("==================== Cannot find tree with name Events in {}".format(f))
                    with open('no_events_'+ args.year + '.txt','a') as wirtefile:
                        wirtefile.write('{}\n'.format(f))
                    continue
                df = ROOT.ROOT.RDataFrame("Events",f)
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

                elif args.poststep=='skim_l1':
                    print('>>>>> skim_l1')
                    df2 = df.Filter('nlepton==1','common cuts for one lepton')
                elif args.poststep=='skim_l2':
                    print('>>>>> skim_l2')
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
                    df2 = df1.Filter("nlepton==2 && MET_pt > 30") \
                        .Filter("lepton_pt[0]>25 || lepton_corrected_pt[0]>25 || lepton_correctedUp_pt[0]>25 || lepton_correctedDown_pt[0]>25","cut lep1_pt") \
                        .Filter("lepton_pt[1]>20 || lepton_corrected_pt[1]>20 || lepton_correctedUp_pt[1]>20 || lepton_correctedDown_pt[1]>20","cut lep2_pt")
                elif args.poststep=='vbs_l2' and args.prestep=='skim_l2':
                    print('>>>>> skim_l2 -> vbs')
                    df2 = df.Filter("njet>1") \
                        .Filter("jet_pt[0]>30 && jet_pt[1]>30 && mjj>500","vbs selections")
                elif args.poststep=='lowmjj_l2' and args.prestep=='skim_l2':
                    print('>>>>> skim_l2 -> lowmjj')
                    df2 = df.Filter("njet>1") \
                        .Filter("jet_pt[0]>30 && jet_pt[1]>30 && mjj > 100 && mjj < 500","low mjj selections")

                elif args.poststep=='skim_l3':
                    print('>>>>> skim_l3')
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
                    df2 = df1.Filter('nlepton==3 && MET_pt > 30','common cuts for three leptons') \
                        .Define("valid_lepton_order","order_wz(lepton_pdgId,lepton_pt,lepton_eta,lepton_phi,lepton_mass)") \
                        .Filter("valid_lepton_order[0]>0","WZ selections") \
                        .Define("ml1l2","invariant_mass_wz(valid_lepton_order,lepton_pt,lepton_eta,lepton_phi,lepton_mass,0)") \
                        .Filter("abs(ml1l2-91.1876)<15","in Z pole") \
                        .Define("ml1l3","invariant_mass_wz(valid_lepton_order,lepton_pt,lepton_eta,lepton_phi,lepton_mass,1)") \
                        .Define("ml2l3","invariant_mass_wz(valid_lepton_order,lepton_pt,lepton_eta,lepton_phi,lepton_mass,2)") \
                        .Define("mlll","invariant_mass_wz(valid_lepton_order,lepton_pt,lepton_eta,lepton_phi,lepton_mass,3)")
                elif args.poststep=='vbs_l3' and args.prestep=='skim_l3':
                    print('>>>>> skim_l3 -> vbs')
                    df2 = df.Filter("njet>1") \
                        .Filter("jet_pt[0]>30 && jet_pt[1]>30 && mjj > 500 && abs(detajj)>2.5","vbs selections")

                    #df2 = df1.Filter("lepton_pt[2]>10 || lepton_corrected_pt[2]>10 || lepton_correctedUp_pt[2]>10 || lepton_correctedDown_pt[2]>10","cut lep2_pt")
                elif args.poststep=='skim_l4':
                    print('>>>>> skim_l4')
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
                    df2 = df1.Filter('nlepton==4 && MET_pt> 30','common cuts for four leptons') \
                        .Define("valid_lepton_order","order_zz(lepton_pdgId,lepton_pt,lepton_eta,lepton_phi,lepton_mass)") \
                        .Define("mZ0","invariant_mass_zz(valid_lepton_order,lepton_pt,lepton_eta,lepton_phi,lepton_mass,0)") \
                        .Define("mZ1","invariant_mass_zz(valid_lepton_order,lepton_pt,lepton_eta,lepton_phi,lepton_mass,1)") \
                        .Define("mllll","invariant_mass_zz(valid_lepton_order,lepton_pt,lepton_eta,lepton_phi,lepton_mass,2)")
                elif args.poststep=='vbs_l4' and args.prestep=='skim_l4':
                    print('>>>>> skim_l4 -> vbs')
                    df2 = df.Filter("njet>1") \
                        .Filter("jet_pt[0]>30 && jet_pt[1]>30","jet cut") \
                        .Filter("mjj > 400 && abs(detajj)>2.4","vbs cuts")
                else:
                    assert(0)

                if not os.path.exists(args.input+'/'+args.year+'/'+args.poststep):
                    os.mkdir(args.input+'/'+args.year+'/'+args.poststep)
                df2.Snapshot("Events",args.input+'/'+args.year+'/'+args.poststep+'/'+samples[idata][i])
                allCutsReport = df.Report()
                allCutsReport.Print()

            if args.fake_weight:
                if not os.path.exists(args.input+'/'+args.year+'/'+args.poststep):
                    print("==================== Error: directory does not exist {}".format(args.input+'/'+args.year+'/'+args.poststep))
                    assert False

                f=ROOT.TFile.Open(args.input+args.year+'/'+args.poststep+'/'+samples[idata][i])
                if not hasattr(f,"Events"):
                    print("==================== Cannot find tree with name Events in {}".format(f))
                    with open('no_events_'+ args.year + '.txt','a') as wirtefile:
                        wirtefile.write('{}\n'.format(f))
                    continue
                df = ROOT.ROOT.RDataFrame("Events",f)
                brach_list=df.GetColumnNames()
                if ("lepton_fake_weight" in brach_list):
                    print("==================== Warning: lepton_fake_weight already exist in {}, please check".format(samples[idata][i]))
                    continue
                print(">>>>> fake weight: {}".format(samples[idata][i]))
                df1=df.Define("lepton_fake_weight","get_fake_lepton_weight(lepton_fakeable,lepton_tight,lepton_pt,lepton_eta,lepton_pdgId,\""+args.year+"\",\"nominal\")") \
                    .Define("lepton_fake_weight_up","get_fake_lepton_weight(lepton_fakeable,lepton_tight,lepton_pt,lepton_eta,lepton_pdgId,\""+args.year+"\",\"up\")") \
                    .Define("lepton_fake_weight_down","get_fake_lepton_weight(lepton_fakeable,lepton_tight,lepton_pt,lepton_eta,lepton_pdgId,\""+args.year+"\",\"down\")")

                tmp_path='/tmp/jixiao%s/' % args.year
                if not os.path.exists(tmp_path):
                    os.mkdir(tmp_path)
                df1.Snapshot("Events",tmp_path+'/'+samples[idata][i],DropColumns(df1.GetColumnNames(),[]))
                os.system('mv ' +tmp_path+'/'+samples[idata][i]+' '+args.input+args.year+'/'+args.poststep)
