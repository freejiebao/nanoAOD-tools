import sys

def get_lumi(_year):
    if _year=='2016':
        return 35.92
    elif _year == '2017':
        return 41.53
    else:
        return 59.74

def set_samples(_year):
    sample = {}
    if _year=='2016':
        sample['SingleMuon']=['SingleMuon_Run2016B.root','SingleMuon_Run2016C.root','SingleMuon_Run2016D.root','SingleMuon_Run2016E.root','SingleMuon_Run2016F.root','SingleMuon_Run2016G.root','SingleMuon_Run2016H.root']
        sample['SingleElectron']=['SingleElectron_Run2016B.root','SingleElectron_Run2016C.root','SingleElectron_Run2016D.root','SingleElectron_Run2016E.root','SingleElectron_Run2016F.root','SingleElectron_Run2016G.root','SingleElectron_Run2016H.root']
        sample['MuonEG']=['MuonEG_Run2016B.root','MuonEG_Run2016C.root','MuonEG_Run2016D.root','MuonEG_Run2016E.root','MuonEG_Run2016F.root','MuonEG_Run2016G.root','MuonEG_Run2016H.root']
        sample['DoubleMuon']=['DoubleMuon_Run2016B.root','DoubleMuon_Run2016C.root','DoubleMuon_Run2016D.root','DoubleMuon_Run2016E.root','DoubleMuon_Run2016F.root','DoubleMuon_Run2016G.root','DoubleMuon_Run2016H.root']
        sample['DoubleEG']=['DoubleEG_Run2016B.root','DoubleEG_Run2016C.root','DoubleEG_Run2016D.root','DoubleEG_Run2016E.root','DoubleEG_Run2016F.root','DoubleEG_Run2016G.root','DoubleEG_Run2016H.root']
        sample['WpWpJJ_EWK']=['WpWpJJ_EWK.root']
        sample['WpWpJJ_QCD']=['WpWpJJ_QCD.root']
        sample['WmWmJJ']=['WmWmJJ.root']
        sample['DPS']=['WWTo2L2Nu_DoubleScattering.root']
        sample['WWJJ_EWK']=['WWJJToLNuLNu_EWK.root']
        sample['WGJJ']=['WGJJToLNu_EWK_QCD.root']
        sample['DY']=['DYJetsToLL_Pt-50To100.root','DYJetsToLL_Pt-100To250.root','DYJetsToLL_Pt-250To400.root','DYJetsToLL_Pt-400To650.root','DYJetsToLL_Pt-650ToInf.root','DYJetsToLL_M-50.root','DYJetsToTauTau_ForcedMuEleDecay_M-50.root','DYJetsToTauTau_ForcedMuEleDecay_M-50_ext1.root']
        sample['ZG']=['ZGTo2LG.root']
        sample['ZZ']=['ZZTo2L2Nu.root','ZZTo4L.root','ZZTo2L2Q.root']
        sample['WW']=['WWTo2L2Nu.root']
        sample['ggWW']=['GluGluWWTo2L2Nu_MCFM.root']
        sample['WZ0']=['WZTo3LNu.root','WZTo2L2Q.root']
        sample['WZ1']=['WZTo3LNu_0Jets_MLL-50.root','WZTo3LNu_1Jets_MLL-50.root','WZTo3LNu_2Jets_MLL-50.root','WZTo3LNu_3Jets_MLL-50.root','WZTo3LNu_0Jets_MLL-4to50.root','WZTo3LNu_1Jets_MLL-4to50.root','WZTo3LNu_2Jets_MLL-4to50.root','WZTo3LNu_3Jets_MLL-4to50.root','WZTo2L2Q.root']
        sample['WZ2']=['WLLJJ_WToLNu_EWK.root','WLLJJ_WToLNu_EWK_4_60.root','WZTo2L2Q.root']
        sample['top']=['TTTo2L2Nu.root','TTZToQQ.root','TTZToLLNuNu_M-10.root','TTWJetsToLNu.root','TTWJetsToQQ.root','ST_tW_top.root','ST_tW_antitop.root']
        sample['ggZZ']=['GluGluToContinToZZTo2e2mu.root','GluGluToContinToZZTo2e2nu.root','GluGluToContinToZZTo2e2tau.root','GluGluToContinToZZTo2mu2nu.root','GluGluToContinToZZTo2mu2tau.root','GluGluToContinToZZTo4e.root','GluGluToContinToZZTo4mu.root','GluGluToContinToZZTo4tau.root']
        sample['VVV']=['ZZZ.root','WZZ.root','WWZ.root','WWW.root']
        data_chain = ['SingleMuon','SingleElectron','MuonEG','DoubleMuon','DoubleEG']
        mc_chain = ['WpWpJJ_EWK','WpWpJJ_QCD','WmWmJJ','DPS','WWJJ_EWK','WGJJ','DY','ZG','ZZ','WW','ggWW','WZ0','WZ1','WZ2','top','ggZZ','VVV']
    elif _year=='2017':
        sample['SingleMuon']=['SingleMuon_Run2017B.root','SingleMuon_Run2017C.root','SingleMuon_Run2017D.root','SingleMuon_Run2017E.root','SingleMuon_Run2017F.root']
        sample['SingleElectron']=['SingleElectron_Run2017B.root','SingleElectron_Run2017C.root','SingleElectron_Run2017D.root','SingleElectron_Run2017E.root','SingleElectron_Run2017F.root']
        sample['MuonEG']=['MuonEG_Run2017B.root','MuonEG_Run2017C.root','MuonEG_Run2017D.root','MuonEG_Run2017E.root','MuonEG_Run2017F.root']
        sample['DoubleMuon']=['DoubleMuon_Run2017B.root','DoubleMuon_Run2017C.root','DoubleMuon_Run2017D.root','DoubleMuon_Run2017E.root','DoubleMuon_Run2017F.root']
        sample['DoubleEG']=['DoubleEG_Run2017B.root','DoubleEG_Run2017C.root','DoubleEG_Run2017D.root','DoubleEG_Run2017E.root','DoubleEG_Run2017F.root']
        sample['WpWpJJ_EWK']=['WpWpJJ_EWK.root']
        sample['WpWpJJ_QCD']=['WpWpJJ_QCD.root']
        sample['DY0']=['DY1JetsToLL_M-50_LHEZpT_50-150.root','DY1JetsToLL_M-50_LHEZpT_150-250.root','DY1JetsToLL_M-50_LHEZpT_250-400.root','DY1JetsToLL_M-50_LHEZpT_400-inf.root','DY2JetsToLL_M-50_LHEZpT_50-150.root','DY2JetsToLL_M-50_LHEZpT_150-250.root','DY2JetsToLL_M-50_LHEZpT_250-400.root','DY2JetsToLL_M-50_LHEZpT_400-inf.root']
        sample['DY1']=['DYJetsToLL_0J.root','DYJetsToLL_1J.root','DYJetsToLL_2J.root']
        sample['DY2']=['DY1JetsToLL_M-50.root','DY2JetsToLL_M-50.root','DY3JetsToLL_M-50.root','DY4JetsToLL_M-50.root']
        sample['DY3']=['DYJetsToLL_M-10to50.root','DYJetsToLL_M-50.root','DYJetsToTauTau_ForcedMuEleDecay_M-50.root']
        sample['ZG']=['ZGToLLG_01J_5f.root']
        sample['ZZ']=['ZZTo2L2Nu.root','ZZTo4L.root','ZZTo2L2Q.root']
        sample['WW']=['WWTo2L2Nu.root']
        sample['ggWW']=['GluGluToWWToENEN.root','GluGluToWWToENMN.root','GluGluToWWToENTN.root','GluGluToWWToMNEN.root','GluGluToWWToMNMN.root','GluGluToWWToMNTN.root','GluGluToWWToTNEN.root','GluGluToWWToTNMN.root','GluGluToWWToTNTN.root']
        sample['top']=['TTTo2L2Nu_TuneCP5_PSweights.root','TTZToQQ.root','TTZToLLNuNu_M-10.root','TTWJetsToLNu.root','TTWJetsToQQ.root','ST_tW_top.root','ST_tW_antitop.root']
        sample['ggZZ']=['GluGluToContinToZZTo2e2mu.root','GluGluToContinToZZTo2e2nu.root','GluGluToContinToZZTo2e2tau.root','GluGluToContinToZZTo2mu2nu.root','GluGluToContinToZZTo2mu2tau.root','GluGluToContinToZZTo4e.root','GluGluToContinToZZTo4mu.root','GluGluToContinToZZTo4tau.root']
        sample['DPS0']=['WW_DoubleScattering.root']
        sample['DPS1']=['WWTo2L2Nu_DoubleScattering.root']
        sample['WWJJ_EWK0']=['WWJJToLNuLNu_EWK_noTop.root']
        sample['WWJJ_EWK1']=['WWJJToLNuLNu_EWK.root']
        sample['WGJJ']=['WGJJToLNu_EWK_QCD.root']
        sample['WZ0']=['WZTo3LNu.root','WZTo2L2Q.root']
        sample['WZ1']=['WZTo3LNu_0Jets_MLL-50.root','WZTo3LNu_1Jets_MLL-50.root','WZTo3LNu_2Jets_MLL-50.root','WZTo3LNu_3Jets_MLL-50.root','WZTo3LNu_0Jets_MLL-4to50.root','WZTo3LNu_1Jets_MLL-4to50.root','WZTo3LNu_2Jets_MLL-4to50.root','WZTo3LNu_3Jets_MLL-4to50.root','WZTo2L2Q.root']
        sample['WZ2']=['WLLJJ_WToLNu_EWK.root','WZTo2L2Q.root']
        sample['VVV']=['ZZZ.root','WZZ.root','WWZ.root','WWW.root']
        data_chain = ['SingleMuon','SingleElectron','MuonEG','DoubleMuon','DoubleEG']
        mc_chain = ['WpWpJJ_EWK','WpWpJJ_QCD','DY0','DY1','DY2','DY3','ZG','ZZ','WW','ggWW','top','ggZZ','DPS0','DPS1','WWJJ_EWK0','WWJJ_EWK1','WGJJ','WZ0','WZ1','WZ2','VVV']
    else:
        sample['SingleMuon']=['SingleMuon_Run2018A.root','SingleMuon_Run2018B.root','SingleMuon_Run2018C.root','SingleMuon_Run2018D.root']
        sample['EGamma']=['EGamma_Run2018A.root','EGamma_Run2018B.root','EGamma_Run2018C.root','EGamma_Run2018D.root']
        sample['MuonEG']=['MuonEG_Run2018A.root','MuonEG_Run2018B.root','MuonEG_Run2018C.root','MuonEG_Run2018D.root']
        sample['DoubleMuon']=['DoubleMuon_Run2018A.root','DoubleMuon_Run2018B.root','DoubleMuon_Run2018C.root','DoubleMuon_Run2018D.root']
        sample['WpWpJJ_EWK']=['WpWpJJ_EWK.root']
        sample['WpWpJJ_QCD']=['WpWpJJ_QCD.root']
        sample['DY0']=['DY1JetsToLL_M-50_LHEZpT_50-150.root','DY1JetsToLL_M-50_LHEZpT_150-250.root','DY1JetsToLL_M-50_LHEZpT_250-400.root','DY1JetsToLL_M-50_LHEZpT_400-inf.root','DY2JetsToLL_M-50_LHEZpT_50-150.root','DY2JetsToLL_M-50_LHEZpT_150-250.root','DY2JetsToLL_M-50_LHEZpT_250-400.root','DY2JetsToLL_M-50_LHEZpT_400-inf.root']
        sample['DY1']=['DYJetsToLL_0J.root','DYJetsToLL_1J.root','DYJetsToLL_2J.root']
        sample['DY2']=['DY1JetsToLL_M-50.root','DY2JetsToLL_M-50.root','DY3JetsToLL_M-50.root','DY4JetsToLL_M-50.root']
        sample['DY3']=['DYJetsToLL_M-10to50','DYJetsToLL_M-50.root','DYJetsToTauTau_ForcedMuEleDecay_M-50.root']
        sample['ZG']=['ZGToLLG_01J_5f.root']
        sample['ZZ']=['ZZTo2L2Nu.root','ZZTo4L.root','ZZTo2L2Q.root']
        sample['WW']=['WWTo2L2Nu.root']
        sample['ggWW']=['GluGluToWWToENEN.root','GluGluToWWToENMN.root','GluGluToWWToENTN.root','GluGluToWWToMNEN.root','GluGluToWWToMNMN.root','GluGluToWWToMNTN.root','GluGluToWWToTNEN.root','GluGluToWWToTNMN.root','GluGluToWWToTNTN.root']
        sample['top']=['TTTo2L2Nu.root','TTZToQQ.root','TTZToLLNuNu_M-10.root','TTWJetsToLNu.root','TTWJetsToQQ.root','ST_tW_top.root','ST_tW_antitop.root']
        sample['ggZZ']=['GluGluToContinToZZTo2e2mu.root','GluGluToContinToZZTo2e2nu.root','GluGluToContinToZZTo2e2tau.root','GluGluToContinToZZTo2mu2nu.root','GluGluToContinToZZTo2mu2tau.root','GluGluToContinToZZTo4e.root','GluGluToContinToZZTo4mu.root','GluGluToContinToZZTo4tau.root']
        sample['DPS0']=['WW_DoubleScattering.root']
        sample['DPS1']=['WWTo2L2Nu_DoubleScattering.root']
        sample['WWJJ_EWK0']=['WWJJToLNuLNu_EWK_noTop.root']
        sample['WWJJ_EWK1']=['WWJJToLNuLNu_EWK.root']
        sample['WGJJ']=['WGJJToLNu_EWK_QCD.root']
        sample['WZ0']=['WZTo3LNu.root','WZTo2L2Q.root']
        sample['WZ1']=['WZTo3LNu_0Jets_MLL-50.root','WZTo3LNu_1Jets_MLL-50.root','WZTo3LNu_2Jets_MLL-50.root','WZTo3LNu_3Jets_MLL-50.root','WZTo3LNu_0Jets_MLL-4to50.root','WZTo3LNu_1Jets_MLL-4to50.root','WZTo3LNu_2Jets_MLL-4to50.root','WZTo3LNu_3Jets_MLL-4to50.root','WZTo2L2Q.root']
        sample['WZ2']=['WLLJJ_WToLNu_EWK.root','WZTo2L2Q.root']
        sample['VVV']=['ZZZ.root','WZZ.root','WWZ.root','WWW.root']
        data_chain = ['SingleMuon','SingleElectron','MuonEG','DoubleMuon','DoubleEG']
        mc_chain = ['WpWpJJ_EWK','WpWpJJ_QCD','DY0','DY1','DY2','DY3','ZG','ZZ','WW','ggWW','top','ggZZ','DPS0','DPS1','WWJJ_EWK0','WWJJ_EWK1','WGJJ','WZ0','WZ1','WZ2','VVV']

    return sample, data_chain, mc_chain


def add_files(_year,input, samples, chain, exclude, include):
    files = []
    if not len(exclude)==0 and not len(include)==0:
        try:
            sys.exit(0)
        except:
            print('>>>>>>>>>>>>>>>>>>>> include and exclude can not be used at same time')
        finally:
            print('>>>>>>>>>>>>>>>>>>>> end this run')

    exclude_flag=False
    if len(exclude)>0:
        exclude_flag=True
    include_flag=False
    if len(include)>0:
        include_flag=True

    for isample in chain:
        if exclude_flag:
            for i in exclude:
                if not i in chain:
                    print('>>>>>>>>>>>>>>>>>>>> %s not in chain') % i
            if not isample in exclude:
                for i in range(0,len(samples[isample])):
                    files.append(input+_year+'/'+samples[isample][i])
        elif include_flag:
            for i in include:
                if not i in chain:
                    print('>>>>>>>>>>>>>>>>>>>> %s not in chain') % i
            if isample in include:
                for i in range(0,len(samples[isample])):
                    files.append(input+_year+'/'+samples[isample][i])
        else:
            for i in range(0,len(samples[isample])):
                files.append(input+_year+'/'+samples[isample][i])
    return files
