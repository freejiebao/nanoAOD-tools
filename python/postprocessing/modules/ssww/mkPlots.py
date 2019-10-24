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

def plot_variables(sample,region,df):
    plots=[]
    plots.append(df.Histo1D(('lep1_pt', "lep1_pt;l_{1}^{pt} (GeV);Event", 5, 20,300), "lepton_pt[0]","weight"))
    plots.append(df.Histo1D(('lep2_pt', "lep2_pt;l_{2}^{pt} (GeV);Event", 5, 20,300), "lepton_pt[1]","weight"))
    plots.append(df.Histo1D(('jet1_pt', "jet1_pt;j_{1}^{pt} (GeV);Event", 5, 20,300), "jet_pt[0]","weight"))
    plots.append(df.Histo1D(('jet2_pt', "jet2_pt;j_{2}^{pt} (GeV);Event", 5, 20,300), "jet_pt[1]","weight"))

    plots.append(df.Histo1D(('lep1_eta', "lep1_eta;l_{1}^{#eta} (GeV);Event", 10, -2.5,2.5), "lepton_eta[0]","weight"))
    plots.append(df.Histo1D(('lep2_eta', "lep2_eta;l_{2}^{#eta} (GeV);Event", 10, -2.5,2.5), "lepton_eta[1]","weight"))
    plots.append(df.Histo1D(('jet1_eta', "jet1_eta;j_{1}^{#eta} (GeV);Event", 10, -2.5,2.5), "jet_eta[0]","weight"))
    plots.append(df.Histo1D(('jet2_eta', "jet2_eta;j_{2}^{#eta} (GeV);Event", 10, -2.5,2.5), "jet_eta[1]","weight"))

    plots.append(df.Histo1D(('mll', "mll;m_{ll} (GeV);Event", 5, 20,300), "mll","weight"))
    plots.append(df.Histo1D(('mjj_low', "mjj_low;m_{jj} (GeV);Event", 5, 150,500), "mjj","weight"))
    plots.append(df.Histo1D(('mjj', "mjj;m_{jj} (GeV);Event", 5, 500,2000), "mjj","weight"))

    f=ROOT.TFile.Open('plots_'+args.year+'.root','update')
    try:
        f.cd(region)
    except:
        f.mkdir(region)
        f.cd(region)

    for i in range(0,len(plots)):
        plot_name=plots[i].GetName()
        try:
            ROOT.gDirectory.cd(plot_name)
        except:
            ROOT.gDirectory.mkdir(plot_name)
            ROOT.gDirectory.cd(plot_name)
        plots[i].SetName(sample)
        #plots[i].SetTitle(sample)
        plots[i].Write()
        ROOT.gDirectory.cd('..')
    return

def get_stack():
    print '>>>>>>>>>>>>>>>>>>>>>>> get stack'

def ssww_region(sample,df):
    print '>>>>>>>>>>>>>>>>>>>>>>> ssww region'
    df1=df.Filter('nlepton==2 && njet>1','basic selection') \
        .Filter('lepton_pt[0]>25 && lepton_pt[1]>20 && mll>20','lepton selection') \
        .Filter('lepton_pdg_id[0]*lepton_pdg_id[1]>0','same sign')\
        .Filter('(lepton_pdg_id[0]*lepton_pdg_id[1]!=11*11 || abs(mll-91.2)>15)','zveto selection')\
        .Filter('jet_pt[0]>30 && jet_pt[1]>30 && mjj>500 && abs(detajj)>2.5','jet selection') \
        .Filter('met>40','met selection')\
        .Filter('lepton_zep[0]<0.75 && lepton_zep[1]<0.75','zepp selection')\
        .Filter('!tauTag','tau veto')\
        .Define('bveto','bveto_helper(jet_pt,jet_eta,jet_btagCSVV2,0.8484)').Filter('bveto')

    allCutsReport = df.Report()
    allCutsReport.Print()
    plot_variables(sample,'ssww_region',df1)
    return

def top_region(sample,df):
    df1=df.Filter('nlepton==2 && njet>1','basic selection') \
        .Filter('lepton_pt[0]>25 && lepton_pt[1]>20 && mll>20','lepton selection') \
        .Filter('lepton_pdg_id[0]*lepton_pdg_id[1]>0','same sign') \
        .Filter('jet_pt[0]>30 && jet_pt[1]>30 && mjj>500 && abs(detajj)>2.5','jet selection') \
        .Filter('met>40','met selection')

    allCutsReport = df.Report()
    allCutsReport.Print()
    plot_variables(sample,'top_region',df1)
    return

def lowmjj_region(sample,df):
    df1=df.Filter('nlepton==2 && njet>1','basic selection') \
        .Filter('lepton_pt[0]>25 && lepton_pt[1]>20 && mll>20','lepton selection') \
        .Filter('lepton_pdg_id[0]*lepton_pdg_id[1]>0','same sign') \
        .Filter('jet_pt[0]>30 && jet_pt[1]>30 && mjj<500 && mjj>150 && abs(detajj)>2.5','jet selection') \
        .Filter('met>40','met selection')

    allCutsReport = df.Report()
    allCutsReport.Print()
    plot_variables(sample,'lowmjj_region',df1)
    return

def wz_region(sample,df):
    df1=df.Filter('nlepton==3 && njet>1','basic selection') \
        .Filter('lepton_pt[0]>25 && lepton_pt[1]>20 && lepton_pt[2]>10','lepton selection') \
        .Filter('lepton_pdg_id[0]*lepton_pdg_id[1]>0','same sign') \
        .Filter('jet_pt[0]>30 && jet_pt[1]>30 && mjj>500 && abs(detajj)>2.5','jet selection') \
        .Filter('met>40','met selection')

    allCutsReport = df.Report()
    allCutsReport.Print()
    plot_variables(sample,'wz_region',df1)
    return

def zz_region(sample,df):
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

    for idata in data_chain:
        data_chain_single = []
        data_chain_single.append(idata)
        files = SAMPLE.add_files(_year,args.input, samples, data_chain_single,[],[],'skim')
        data_files = ROOT.std.vector("string")(len(files))
        if not len(files)==0:
            for i in range(0,len(files)):
                data_files[i] = files[i]
            ssww_region(idata, data_files)
            #top_region(idata, data_files)
            #lowmjj_region(idata, data_files)
            #wz_region(idata, data_files)
            #zz_region(idata, data_files)

    for imc in mc_chain:
        mc_chain_single = []
        mc_chain_single.append(imc)
        files = SAMPLE.add_files(_year,args.input, samples, mc_chain_single,[],[],'skim')
        mc_files = ROOT.std.vector("string")(len(files))
        if not len(files)==0:
            for i in range(0,len(files)):
                mc_files[i] = files[i]
            ssww_region(imc, data_files)
            #top_region(imc, data_files)
            #lowmjj_region(imc, data_files)
            #wz_region(imc, data_files)
            #zz_region(imc, data_files)

if __name__ == '__main__':

    #print ('>>>>>>>>>>>>>>>>>>>> exclude: ',args.exclude)
    print ('>>>>>>>>>>>>>>>>>>>> include: ',args.include)
    calc(args.year)
