import ROOT
import argparse
import SAMPLE
from array import array

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-s','--subtract', help='subtract real lepton, default is true',action='store_false', default= True)
parser.add_argument('-i','--input', help='input path', default= '/home/cmsdas/testuser01/jie/ssww_ntuple/')
parser.add_argument('-y','--year', help='which year, default is 2016', default= '2016', choices=('2016','2017','2018'))
group = parser.add_mutually_exclusive_group()  # type: _MutuallyExclusiveGroup
group.add_argument('-c','--channel', help='muon/electron fake rate', choices=('muon','electron'),default='muon')
group.add_argument('-a','--all', help='muon and electron fake rate',action='store_true', default= False)
'''
group_data = parser.add_mutually_exclusive_group()  # type: _MutuallyExclusiveGroup
group_data.add_argument('-in','--include', help='include samples only',nargs='*',default=[])
group_data.add_argument('-ex','--exclude', help='exclude samples',nargs='*',default=['SingleMuon','SingleElectron','MuonEG','DoubleEG'])
'''
group_mc = parser.add_mutually_exclusive_group()  # type: _MutuallyExclusiveGroup
group_mc.add_argument('-in','--include', help='include samples only',nargs='*',default=[])
group_mc.add_argument('-ex','--exclude', help='exclude samples',nargs='*',default=['WZ1','WZ2'])
args = parser.parse_args()


ROOT.ROOT.EnableImplicitMT(70)
ROOT.gROOT.SetBatch(ROOT.kTRUE)

run_helper_header_path = "run_helper_python.h"
ROOT.gInterpreter.Declare('#include "{}"'.format(run_helper_header_path))


def histogram_model():
    histogram_models={
        'lep1_pt':['lepton_pt[0]',ROOT.RDF.TH1DModel('', "lep1_pt;l_{1}^{pt} (GeV);Event", 5, 25,300)],
        'lep2_pt':['lepton_pt[1]',ROOT.RDF.TH1DModel('', "lep2_pt;l_{2}^{pt} (GeV);Event", 5, 20,300)],
        'lep3_pt':['lepton_pt[2]',ROOT.RDF.TH1DModel('', "lep3_pt;l_{3}^{pt} (GeV);Event", 5, 20,300)],
        'lep1_eta':['lepton_eta[0]',ROOT.RDF.TH1DModel('', "lep1_eta;l_{1}^{#eta} (GeV);Event", 10, -2.5,2.5)],
        'lep2_eta':['lepton_eta[1]',ROOT.RDF.TH1DModel('', "lep2_eta;l_{2}^{#eta} (GeV);Event", 10, -2.5,2.5)],
        'lep3_eta':['lepton_eta[2]',ROOT.RDF.TH1DModel('', "lep3_eta;l_{3}^{#eta} (GeV);Event", 10, -2.5,2.5)],
        'jet1_pt':['jet_pt[0]',ROOT.RDF.TH1DModel('', "jet1_pt;j_{1}^{pt} (GeV);Event", 5, 20,300)],
        'jet2_pt':['jet_pt[1]',ROOT.RDF.TH1DModel('', "jet2_pt;j_{2}^{pt} (GeV);Event", 5, 20,300)],
        'jet1_eta':['jet_eta[0]',ROOT.RDF.TH1DModel('', "jet1_eta;j_{1}^{#eta} (GeV);Event", 10, -2.5,2.5)],
        'jet2_eta':['jet_eta[1]',ROOT.RDF.TH1DModel('', "jet2_eta;j_{2}^{#eta} (GeV);Event", 10, -2.5,2.5)],
        'mll':['mll',ROOT.RDF.TH1DModel('', "mll;m_{ll} (GeV);Event", 5, 20,300)],
        'mjj_low':['mjj',ROOT.RDF.TH1DModel('', "mjj_low;m_{jj} (GeV);Event", 5, 100,500)],
        'mjj':['mjj',ROOT.RDF.TH1DModel('', "mjj;m_{jj} (GeV);Event", 5, 500,2000)],
    }

    return histogram_models

def plot_variables(sample,region,df,type='base'):
    plots={}
    histogram_models=histogram_model()
    for ihis in histogram_models:
        histo=df.Define("variable",histogram_models[ihis][0]).Histo1D(histogram_models[ihis][1],'variable','weight')
        histo.SetName(sample+'_'+type+'_'+ihis)
        histo.Sumw2()
        plots[sample+'_'+type+'_'+ihis]=histo
    f=ROOT.TFile.Open('plots_'+region+'_'+args.year+'.root','update')

    for ihis in histogram_models:
        ROOT.gDirectory.cd(ihis)
        plots[sample+'_'+type+'_'+ihis].Write()
        ROOT.gDirectory.cd('..')
    f.Write("",ROOT.TObject.kOverwrite)
    f.Close()
    return

def get_stack(region):
    print '>>>>>>>>>>>>>>>>>>>>>>> get stack'
    f=ROOT.TFile.Open('plots_'+region+'_'+args.year+'.root')
    plot_scheme=SAMPLE.plot_scheme(args.year)
    histogram_models=histogram_model()
    for tkey in f.GetListOfKeys():
        key=tkey.GetName()
        #htmp=ROOT.TH1F
        #print(key)
        dir=f.cd(key)
        plots=[]
        for i in dir.GetListOfKeys():
            print '>>>>> variable:',dir
            hs=ROOT.THStack("hs","")
            htotal=histogram_models[key].GetHistogram()
            htotal.SetName('total_'+key)
            for j in plot_scheme:
                htmp=histogram_models[key].GetHistogram()
                htmp.SetName(j+'_'+key)
                for k in plot_scheme[j]['sample']:
                    htmp.Add(k+'_'+key)
                    htotal.Add(k+'_'+key)
                #plots.append(htmp)
                hs.Add(htmp)

def ssww_region(datasets,sample,df):
    print '>>>>>>>>>>>>>>>>>>>>>>> %s in ssww region' % sample
    df1=df.Filter('nlepton==2 && njet>1','basic selection') \
        .Filter('lepton_pt[0]>25 && lepton_pt[1]>20 && mll>20','lepton selection') \
        .Filter('(lepton_pdg_id[0]*lepton_pdg_id[1]!=11*11 || abs(mll-91.2)>15)','zveto selection')\
        .Filter('jet_pt[0]>30 && jet_pt[1]>30 && mjj>500 && abs(detajj)>2.5','jet selection') \
        .Filter('met>40','met selection')\
        .Filter('lepton_zep[0]<0.75 && lepton_zep[1]<0.75','zepp selection')\
        .Filter('!tauTag','tau veto')\
        .Define('bveto','bveto_helper(jet_pt,jet_eta,jet_btagCSVV2,0.8484)').Filter('bveto')\
        .Filter('!softmuonTag','softmuon veto')

    allCutsReport = df.Report()
    allCutsReport.Print()

    if sample in datasets['data']:
        df2=df1.Filter('lepton_pdg_id[0]*lepton_pdg_id[1]>0','same sign')
        df_base=df2.Filter("lepton_tight[0] && lepton_tight[1]")\
            .Define("weight","1.;")
        df_single_fake=df2.Filter("(lepton_fakeable[0] && !lepton_tight[0] && lepton_tight[1]) || (lepton_fakeable[1] && !lepton_tight[1] && lepton_tight[0])")\
            .Define('fake_weight',"lepton_fake_weight[0]*lepton_fake_weight[1]")\
            .Define("weight","fake_weight")
        df_double_fake=df2.Filter("lepton_fakeable[0] && !lepton_tight[0] && lepton_fakeable[1] && !lepton_tight[1]") \
            .Define('fake_weight',"-1*lepton_fake_weight[0]*lepton_fake_weight[1]")\
            .Define("weight","fake_weight")

        plot_variables(sample,'ssww_region',df_base)
        plot_variables(sample,'ssww_region',df_single_fake,'1fake')
        plot_variables(sample,'ssww_region',df_double_fake,'2fake')

    elif sample in datasets['mc']:
        df2=df1.Filter('lepton_pdg_id[0]*lepton_pdg_id[1]>0','same sign')
        df_base=df2.Filter("lepton_real[0] && lepton_real[1] && lepton_tight[0] && lepton_tight[1]").Define("weight","xsweight*lepton_sf[0]*lepton_sf[1]")
        df_single_fake=df2.Filter("lepton_real[0] && lepton_real[1] && ((lepton_fakeable[0] && !lepton_tight[0] && lepton_tight[1]) || (lepton_fakeable[1] && !lepton_tight[1] && lepton_tight[0]))") \
            .Define('fake_weight',"-1*lepton_fake_weight[0]*lepton_fake_weight[1]").Define("weight","xsweight*lepton_sf[0]*lepton_sf[1]*fake_weight")
        df_double_fake=df2.Filter("lepton_real[0] && lepton_real[1] && lepton_fakeable[0] && !lepton_tight[0] && lepton_fakeable[1] && !lepton_tight[1]") \
            .Define('fake_weight',"lepton_fake_weight[0]*lepton_fake_weight[1]").Define("weight","xsweight*lepton_sf[0]*lepton_sf[1]*fake_weight")

        plot_variables(sample,'ssww_region',df_base)
        plot_variables(sample,'ssww_region',df_single_fake,'1fake')
        plot_variables(sample,'ssww_region',df_double_fake,'2fake')

    elif sample in datasets['vgamma']:
        df2=df1.Filter('lepton_pdg_id[0]*lepton_pdg_id[1]>0','same sign')
        df_base=df2.Filter("lepton_tight[0] && lepton_tight[1]").Define("weight","xsweight*lepton_sf[0]*lepton_sf[1]")
        df_single_fake=df2.Filter("((lepton_fakeable[0] && !lepton_tight[0] && lepton_tight[1]) || (lepton_fakeable[1] && !lepton_tight[1] && lepton_tight[0]))") \
            .Define('fake_weight',"-1*lepton_fake_weight[0]*lepton_fake_weight[1]").Define("weight","xsweight*lepton_sf[0]*lepton_sf[1]*fake_weight")
        df_double_fake=df2.Filter("lepton_fakeable[0] && !lepton_tight[0] && lepton_fakeable[1] && !lepton_tight[1]") \
            .Define('fake_weight',"lepton_fake_weight[0]*lepton_fake_weight[1]").Define("weight","xsweight*lepton_sf[0]*lepton_sf[1]*fake_weight")

        plot_variables(sample,'ssww_region',df_base)
        plot_variables(sample,'ssww_region',df_single_fake,'1fake')
        plot_variables(sample,'ssww_region',df_double_fake,'2fake')

    elif sample in datasets['chargeflip']:
        df2=df1.Filter('lepton_pdg_id[0]*lepton_pdg_id[1]<0','opposite sign')
        df_base=df2.Filter("lepton_real[0] && lepton_real[1] && lepton_tight[0] && lepton_tight[1]")\
            .Define('chargeflip_weight',"lepton_chargeflip_weight[0]*lepton_chargeflip_weight[1]").Define("weight","1.")

        plot_variables(sample,'ssww_region',df_base,'chargeflip')

    return

def top_region(datasets,sample,df):
    df1=df.Filter('nlepton==2 && njet>1','basic selection') \
        .Filter('lepton_pt[0]>25 && lepton_pt[1]>20 && mll>20','lepton selection') \
        .Filter('lepton_pdg_id[0]*lepton_pdg_id[1]>0','same sign') \
        .Filter('jet_pt[0]>30 && jet_pt[1]>30 && mjj>500 && abs(detajj)>2.5','jet selection') \
        .Filter('met>40','met selection')

    allCutsReport = df.Report()
    allCutsReport.Print()
    plot_variables(sample,'top_region',df1)
    return

def lowmjj_region(datasets,sample,df):
    df1=df.Filter('nlepton==2 && njet>1','basic selection') \
        .Filter('lepton_pt[0]>25 && lepton_pt[1]>20 && mll>20','lepton selection') \
        .Filter('lepton_pdg_id[0]*lepton_pdg_id[1]>0','same sign') \
        .Filter('jet_pt[0]>30 && jet_pt[1]>30 && mjj<500 && mjj>150 && abs(detajj)>2.5','jet selection') \
        .Filter('met>40','met selection')

    allCutsReport = df.Report()
    allCutsReport.Print()
    plot_variables(sample,'lowmjj_region',df1)
    return

def wz_region(datasets,sample,df):
    df1=df.Filter('nlepton==3 && njet>1','basic selection') \
        .Filter('lepton_pt[0]>25 && lepton_pt[1]>20 && lepton_pt[2]>10','lepton selection') \
        .Filter('lepton_pdg_id[0]*lepton_pdg_id[1]>0','same sign') \
        .Filter('jet_pt[0]>30 && jet_pt[1]>30 && mjj>500 && abs(detajj)>2.5','jet selection') \
        .Filter('met>40','met selection')

    allCutsReport = df.Report()
    allCutsReport.Print()
    plot_variables(sample,'wz_region',df1)
    return

def zz_region(datasets,sample,df):
    df1=df.Filter('nlepton==4 && njet>1','basic selection') \
        .Filter('lepton_pt[0]>25 && lepton_pt[1]>20 && lepton_pt[2]>10','lepton selection') \
        .Filter('lepton_pdg_id[0]*lepton_pdg_id[1]>0','same sign') \
        .Filter('jet_pt[0]>30 && jet_pt[1]>30 && mjj>500 && abs(detajj)>2.5','jet selection') \
        .Filter('met>40','met selection')

    allCutsReport = df.Report()
    allCutsReport.Print()
    plot_variables(sample,'wz_region',df1)
    return

def calc(_year):
    # Enable multi-threading
    # Create dataframe from NanoAOD files

    # include = []
    # exclude = []
    samples, data_chain, mc_chain = SAMPLE.set_samples(_year)

    datasets={
        'data':['SingleMuon','SingleElectron','MuonEG','DoubleMuon','DoubleEG'],
        'non-prompt':['SingleMuon','SingleElectron','MuonEG','DoubleMuon','DoubleEG'],
        'mc':['WpWpJJ_EWK','WpWpJJ_QCD','WmWmJJ','DPS','ZZ','WZ0','WZ1','WZ2','top','ggZZ','VVV','WJets'],
        'vgamma':['WGJJ','ZG'],
        'chargeflip':['WWJJ_EWK','WW','ggWW','DY1','DY2','DY3','DY4']
    }

    sample_chain=data_chain+mc_chain
    #data_chain = ['SingleMuon','SingleElectron','MuonEG','DoubleMuon','DoubleEG']
    #mc_chain = ['WpWpJJ_EWK','WpWpJJ_QCD','WmWmJJ','DPS','WWJJ_EWK','WGJJ','ZG','ZZ','WW','ggWW','WZ0','WZ1','WZ2','top','ggZZ','VVV','WJets','DY1','DY2','DY3','DY4']
    for isample in sample_chain:

        files_l2 = SAMPLE.add_files(_year,args.input, samples, [isample],[],[],'skim_l2')
        files_l3 = SAMPLE.add_files(_year,args.input, samples, [isample],[],[],'skim_l3')
        files_l4 = SAMPLE.add_files(_year,args.input, samples, [isample],[],[],'skim_l4')
        sample_files_l2 = ROOT.std.vector("string")(len(files_l2))
        sample_files_l3 = ROOT.std.vector("string")(len(files_l3))
        sample_files_l4 = ROOT.std.vector("string")(len(files_l4))

        if not len(files_l2)==0:
            for i in range(0,len(files_l2)):
                sample_files_l2[i] = files_l2[i]
            df=ROOT.ROOT.RDataFrame("Events",sample_files_l2)

            f=ROOT.TFile.Open('plots_ssww_region_'+args.year+'.root','recreate')
            histogram_models=histogram_model()
            for ihis in histogram_models:
                ROOT.gDirectory.mkdir(ihis)
            f.Close()
            ssww_region(datasets,isample, df)

            #top_region(datasets,isample, df)
            #lowmjj_region(datasets,isample, df)
            #wz_region(datasets,isample, df)
            #zz_region(datasets,isample, df)
        '''
        if not len(files_l3)==0:
            for i in range(0,len(files_l3)):
                sample_files_l3[i] = files_l3[i]
            df=ROOT.ROOT.TFile("Events",sample_files_l3)
            wz_region(datasets,isample, df)
            #zz_region(datasets,isample, df)

        if not len(files_l4)==0:
            for i in range(0,len(files_l4)):
                sample_files_l4[i] = files_l4[i]
            df=ROOT.ROOT.TFile("Events",sample_files_l4)
            zz_region(datasets,isample, df)
        '''

if __name__ == '__main__':

    #print ('>>>>>>>>>>>>>>>>>>>> exclude: ',args.exclude)
    #print ('>>>>>>>>>>>>>>>>>>>> include: ',args.include)
    calc(args.year)
