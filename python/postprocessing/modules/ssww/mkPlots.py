import ROOT
import argparse
import SAMPLE
import style

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
        plots[sample+'_'+type+'_'+ihis]=histo.Clone()
    f=ROOT.TFile.Open('plots_'+region+'_'+args.year+'.root','update')

    for ihis in histogram_models:
        ROOT.gDirectory.cd(ihis)
        plots[sample+'_'+type+'_'+ihis].Write()
        ROOT.gDirectory.cd('..')
    f.Write("",ROOT.TObject.kOverwrite)
    f.Close()
    return

xoffsetstart = 0.0
yoffsetstart = 0.0
xoffset = 0.20
yoffset = 0.05

xpositions = [0.68,0.68,0.68,0.68,0.4,0.4,0.4,0.4,0.21,0.21,0.21,0.21]
ypositions = [0,1,2,3,0,1,2,3,0,1,2,3]

style.GoodStyle().cd()

def draw_legend(x1,y1,hist,label,options):

    legend = ROOT.TLegend(x1+xoffsetstart,y1+yoffsetstart,x1+xoffsetstart + xoffset,y1+yoffsetstart + yoffset)

    legend.SetBorderSize(     0)
    legend.SetFillColor (     0)
    legend.SetTextAlign (    12)
    legend.SetTextFont  (    42)
    legend.SetTextSize  ( 0.040)

    legend.AddEntry(hist,label,options)

    legend.Draw("same")

    #otherwise the legend goes out of scope and is deleted once the function finishes
    hist.label = legend

def set_axis_fonts(thstack, coordinate):

    if coordinate == "x":
        axis = thstack.GetXaxis()
    elif coordinate == "y":
        axis = thstack.GetYaxis()
    else:
        assert(0)

    axis.SetLabelFont  (   42)
    axis.SetLabelOffset(0.015)
    axis.SetLabelSize  (0.050)
    axis.SetNdivisions (  505)
    axis.SetTitleFont  (   42)
    axis.SetTitleOffset(  1.5)
    axis.SetTitleSize  (0.050)
    if (coordinate == "y"):
        axis.SetTitleOffset(1.6)

def get_stack(region):
    print '>>>>>>>>>>>>>>>>>>>>>>> get stack'
    f=ROOT.TFile.Open('plots_'+region+'_'+args.year+'.root')
    plot_scheme=SAMPLE.plot_scheme(args.year)
    histogram_models=histogram_model()
    for tkey in f.GetListOfKeys():
        print '>>>>> variable:',tkey

        key=tkey.GetName()
        dir=f.Get(key)

        c1 = ROOT.TCanvas("c1", "c1",5,50,500,500)
        hdata=dir.Get(plot_scheme['Data']['sample'][0]+'_base_'+key)
        hdata.Scale(0)
        hdata.SetName('data_'+key)

        htotal=hdata.Clone()
        htotal.SetName('mc_'+key)

        hs=ROOT.THStack("hs","")



        for iisample in plot_scheme['Data']['sample']:
            hdata.Add(dir.Get(iisample+'_base_'+key))

        plots={}
        for iplot in plot_scheme:
            htmp=hdata.Clone()
            htmp.Scale(0)
            htmp.SetName(iplot+'_'+key)

            if not iplot=='Data':
                for iisample in plot_scheme[iplot]['sample']:
                    if iplot=='Non-prompt':
                        htotal.Add(dir.Get(iisample+'_1fake_'+key))
                        htotal.Add(dir.Get(iisample+'_2fake_'+key))
                        htmp.Add(dir.Get(iisample+'_1fake_'+key))
                        htmp.Add(dir.Get(iisample+'_2fake_'+key))
                    else:
                        htotal.Add(dir.Get(iisample+'_base_'+key))
                        htmp.Add(dir.Get(iisample+'_base_'+key))
                htmp.SetFillColor(plot_scheme[iplot]['color'])
                plots[iplot]=htmp
                hs.Add(htmp)

        if hdata.GetMaximum() < htotal.GetMaximum():
            hdata.SetMaximum(htotal.GetMaximum()*1.55)
        else:
            hdata.SetMaximum(hdata.GetMaximum()*1.55)

        hdata.SetMinimum(0)
        hs.SetMinimum(0)
        htotal.SetMinimum(0)

        hdata.Draw("")
        hs.Draw("hist same")

        legend_count=0
        draw_legend(xpositions[legend_count],0.84 - ypositions[legend_count]*yoffset,hdata,"Data","lp")

        for iplot in plots:
            legend_count+=1
            draw_legend(xpositions[legend_count],0.84 - ypositions[legend_count]*yoffset,plots[iplot],plot_scheme[iplot].name,"f")

        set_axis_fonts(hdata,"x")
        #set_axis_fonts(hstack,"x","pt_{l}^{max} (GeV)")
        #set_axis_fonts(data_hist,"y","Events / bin")
        #set_axis_fonts(hstack,"y","Events / bin")

        gstat = ROOT.TGraphAsymmErrors(htotal)

        for j in range(0,gstat.GetN()):
            gstat.SetPointEYlow (j, htotal.GetBinError(j+1))
            gstat.SetPointEYhigh(j, htotal.GetBinError(j+1))

        gstat.SetFillColor(12)
        gstat.SetFillStyle(3345)
        gstat.SetMarkerSize(0)
        gstat.SetLineWidth(0)
        gstat.SetLineColor(ROOT.kWhite)
        gstat.Draw("E2same")

        hdata.Draw("same")

        cmslabel = ROOT.TLatex (0.18, 0.93, "")
        cmslabel.SetNDC ()
        cmslabel.SetTextAlign (10)
        cmslabel.SetTextFont (42)
        cmslabel.SetTextSize (0.040)
        cmslabel.Draw ("same")

        s=str(SAMPLE.get_lumi(args.year))+" fb^{-1} (13 TeV)"
        lumilabel = ROOT.TLatex (0.95, 0.93, s)
        lumilabel.SetNDC ()
        lumilabel.SetTextAlign (30)
        lumilabel.SetTextFont (42)
        lumilabel.SetTextSize (0.040)
        lumilabel.Draw("same")

        c1.Update()
        c1.ForceUpdate()
        c1.Modified()

        c1.SaveAs(args.year+'_plots/'+args.year+'_'+region+'_'+key+".png")


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
        df_base=df2.Filter("lepton_real[0] && lepton_real[1] && lepton_tight[0] && lepton_tight[1]").Define("weight","xsweight*lepton_sf[0]*lepton_sf[1]*puWeight*PrefireWeight")
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

    #data_chain = ['SingleMuon','SingleElectron','MuonEG','DoubleMuon','DoubleEG']
    #mc_chain = ['WpWpJJ_EWK','WpWpJJ_QCD','WmWmJJ','DPS','WWJJ_EWK','WGJJ','ZG','ZZ','WW','ggWW','WZ0','WZ1','WZ2','top','ggZZ','VVV','WJets','DY1','DY2','DY3','DY4']

    datasets={
        'data':['SingleMuon','SingleElectron','MuonEG','DoubleMuon','DoubleEG'],
        'non-prompt':['SingleMuon','SingleElectron','MuonEG','DoubleMuon','DoubleEG'],
        'mc':['WpWpJJ_EWK','WpWpJJ_QCD','WmWmJJ','DPS','ZZ','WZ0','WZ1','WZ2','top','ggZZ','VVV','WJets'],
        'vgamma':['WGJJ','ZG'],
        'chargeflip':['WWJJ_EWK','WW','ggWW','DY1','DY2','DY3','DY4']
    }

    sample_chain=data_chain+mc_chain

    f=ROOT.TFile.Open('plots_ssww_region_'+args.year+'.root','recreate')
    histogram_models=histogram_model()
    for ihis in histogram_models:
        ROOT.gDirectory.mkdir(ihis)
    f.Close()

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
    get_stack('ssww_region')

if __name__ == '__main__':

    #print ('>>>>>>>>>>>>>>>>>>>> exclude: ',args.exclude)
    #print ('>>>>>>>>>>>>>>>>>>>> include: ',args.include)
    calc(args.year)
