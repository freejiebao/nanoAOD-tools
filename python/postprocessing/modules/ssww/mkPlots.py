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
    plots={}
    histogram_models=[
        ['lep1_pt','lepton_pt[0]',ROOT.RDF.TH1DModel('', "lep1_pt;l_{1}^{pt} (GeV);Event", 5, 25,300)],
        ['lep2_pt','lepton_pt[1]',ROOT.RDF.TH1DModel('', "lep2_pt;l_{2}^{pt} (GeV);Event", 5, 20,300)],
        ['lep3_pt','lepton_pt[2]',ROOT.RDF.TH1DModel('', "lep3_pt;l_{3}^{pt} (GeV);Event", 5, 20,300)],
        ['lep1_eta','lepton_eta[0]',ROOT.RDF.TH1DModel('', "lep1_eta;l_{1}^{#eta} (GeV);Event", 10, -2.5,2.5)],
        ['lep2_eta','lepton_eta[1]',ROOT.RDF.TH1DModel('', "lep2_eta;l_{2}^{#eta} (GeV);Event", 10, -2.5,2.5)],
        ['lep3_eta','lepton_eta[2]',ROOT.RDF.TH1DModel('', "lep3_eta;l_{3}^{#eta} (GeV);Event", 10, -2.5,2.5)],
        ['jet1_pt','jet_pt[0]',ROOT.RDF.TH1DModel('', "jet1_pt;j_{1}^{pt} (GeV);Event", 5, 20,300)],
        ['jet2_pt','jet_pt[1]',ROOT.RDF.TH1DModel('', "jet2_pt;j_{2}^{pt} (GeV);Event", 5, 20,300)],
        ['jet1_eta','jet_eta[0]',ROOT.RDF.TH1DModel('', "jet1_eta;j_{1}^{#eta} (GeV);Event", 10, -2.5,2.5)],
        ['jet2_eta','jet_eta[1]',ROOT.RDF.TH1DModel('', "jet2_eta;j_{2}^{#eta} (GeV);Event", 10, -2.5,2.5)],
        ['mll','mll',ROOT.RDF.TH1DModel('', "mll;m_{ll} (GeV);Event", 5, 20,300)],
        ['mjj_low','mjj',ROOT.RDF.TH1DModel('', "mjj_low;m_{jj} (GeV);Event", 5, 100,500)],
        ['mjj','mjj',ROOT.RDF.TH1DModel('', "mjj;m_{jj} (GeV);Event", 5, 500,2000)],
    ]
    for i in range(0,len(histogram_models)):
        histo=histogram_models[i][2].GetHistogram()
        histo.Sumw2()
        histo.SetName(sample+'_'+histogram_models[i][0])
        plots[sample+'_'+histogram_models[i][0]]=df.Histo1D(histogram_models[i][2],histogram_models[i][1],'weight')

    f=ROOT.TFile.Open('plots_'+region+'_'+args.year+'.root','update')

    for i in range(0,len(histogram_models)):
        try:
            ROOT.gDirectory.cd(histogram_models[i][0])
        except:
            ROOT.gDirectory.mkdir(histogram_models[i][0])
            ROOT.gDirectory.cd(histogram_models[i][0])
        plots[sample+'_'+histogram_models[i][0]].Write()
        ROOT.gDirectory.cd('..')
    f.Write("",ROOT.TObject.kOverwrite)
    f.Close()
    return

def get_stack(region):
    print '>>>>>>>>>>>>>>>>>>>>>>> get stack'
    f=ROOT.TFile.Open('plots_'+region+'_'+args.year+'.root')
    plot_scheme=SAMPLE.plot_scheme(args.year)
    # which directory to go
    dirs=[]
    for tkey in f.GetListOfKeys():
        key=tkey.GetName()
        #htmp=ROOT.TH1F
        #print(key)
        dir=f.cd(key)
        for i in dir.GetListOfKeys():
            print '>>>>> variable:',dir
            for j in plot_scheme:
                for k in plot_scheme[j]['sample']:
                    htmp.Add(k+'_'+key)


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
    #print ('>>>>>>>>>>>>>>>>>>>> include: ',args.include)
    calc(args.year)
