import os

import argparse
import sys

import ROOT
import numpy as np
from array import array
from math import sqrt

import SAMPLE

ROOT.ROOT.EnableImplicitMT(32)
ROOT.gROOT.SetBatch(ROOT.kTRUE)

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-p','--plot', help='make mll distribution, default is false',action='store_true', default= False)
parser.add_argument('-f','--fit', help='fit to mll distribution, default is false',action='store_true', default= False)
parser.add_argument('-r','--ratio', help='get ratio h_os divided by h_ss', action='store_true', default= False)
parser.add_argument('-pt','--ptbin', help='decide which pt bin: highpt,lowpt2,lowpt1,lowpt0', choices=('highpt','lowpt2','lowpt1','lowpt0'), default= 'highpt')
parser.add_argument('-c','--count', help='count the event, not fit, default is false', action='store_true', default= False)
parser.add_argument('-y','--year', help='which year: 2016/2017/2018, default is 2016',default= '2016', choices=('2016','2017','2018'))
parser.add_argument('-i','--input', help='input path', default= '/home/cmsdas/testuser01/jie/ssww_ntuple/')
parser.add_argument('-post','--poststep', help='declare poststep path postfix', default= 'chargeflip/chargeflip_plot')
parser.add_argument('-pre','--prestep', help='declare prestep path postfix', default= 'chargeflip')
args = parser.parse_args()

args = parser.parse_args()

zmass = '91.2'

def save_plot(files,weight,prefix):
    print('>>>>>>>>>>>>>>>>>>>> save plots')
    fout=ROOT.TFile(args.input+'/'+args.year+'/'+args.poststep+'/'+'plots_'+args.year+'_'+args.ptbin+'.root','update')
    #df = ROOT.ROOT.RDataFrame("Events", files)
    '''
    if args.year=='2016':
        lep1_pt='23'
    elif args.year=='2017':
        lep1_pt='23'
    else:
        lep1_pt='23'
    '''
    pt_cut=''
    if args.ptbin=='highpt':
        pt_cut='lep1_pt > 23 &&  lep2_pt > 23 && lep1_tight && lep2_tight && abs(mll-91.2)<15'
    elif args.ptbin=='lowpt2':
        pt_cut='lep1_pt > 23 &&  lep2_pt <= 50 && lep2_pt > 35 && lep1_tight && lep2_tight && abs(mll-91.2)<15'
    elif args.ptbin=='lowpt1':
        pt_cut='lep1_pt > 23 &&  lep2_pt <= 35 && lep2_pt > 23 && lep1_tight && lep2_tight && abs(mll-91.2)<15'
    elif args.ptbin=='lowpt0':
        pt_cut='lep1_pt > 23 &&  lep2_pt <= 23 && lep2_pt > 12 && lep1_tight && lep2_tight && abs(mll-91.2)<15'
    #df1=df.Filter('lep1_pt > 30 &&  lep2_pt > 30 && abs(mll-'+zmass+') < 15')

    eta_bin = ['0.','0.5','1.0','1.5','2.0','2.5']
    regions=np.zeros((5,5),dtype=np.object)
    for i in range(len(regions)):
        for j in range(len(regions[i])):
            regions[i][j]='abs(lep1_eta)>='+eta_bin[i]+' && abs(lep1_eta)<'+eta_bin[i+1]+' && abs(lep2_eta)>='+eta_bin[j]+' && abs(lep2_eta)<'+eta_bin[j+1]
    h_os={
        0:{0:[],1:[],2:[],3:[],4:[]},
        1:{0:[],1:[],2:[],3:[],4:[]},
        2:{0:[],1:[],2:[],3:[],4:[]},
        3:{0:[],1:[],2:[],3:[],4:[]},
        4:{0:[],1:[],2:[],3:[],4:[]},
    }

    h_ss={
        0:{0:[],1:[],2:[],3:[],4:[]},
        1:{0:[],1:[],2:[],3:[],4:[]},
        2:{0:[],1:[],2:[],3:[],4:[]},
        3:{0:[],1:[],2:[],3:[],4:[]},
        4:{0:[],1:[],2:[],3:[],4:[]},
    }

    for ifile in range(0,len(files)):
        df=ROOT.ROOT.RDataFrame('Events',args.input+'/'+args.year+'/'+args.prestep+'/'+files[ifile])
        df1=df.Filter(pt_cut)
        # pt_bin=['0.','20.']
        #eta_bin = ['0.','0.5','1.0','1.5','2.0','2.5']

        # same-sign
        df_ss=df1.Filter('lep1_pdgId*lep2_pdgId == 11*11').Define('weight',weight[ifile])
        for i in range(len(regions)):
            for j in range(len(regions[i])):
                df_tmp=df_ss.Filter(regions[i][j])
                histo=df_tmp.Histo1D((prefix+"_ss_etabin"+str(i)+"_etabin"+str(j)+"_mll"+str(ifile), "mll", 30, 76.2, 106.2), "mll","weight")
                h_ss[i][j].append(histo)

        # opposite-sign, actually the total number of dielectron
        df_os=df1.Filter('lep1_pdgId*lep2_pdgId == -11*11').Define('weight',weight[ifile])
        for i in range(len(regions)):
            for j in range(len(regions[i])):
                df_tmp=df_os.Filter(regions[i][j])
                histo=df_tmp.Histo1D((prefix+"_os_etabin"+str(i)+"_etabin"+str(j)+"_mll"+str(ifile), "mll", 30, 76.2, 106.2), "mll","weight")
                h_os[i][j].append(histo)

    for i in range(len(regions)):
        for j in range(len(regions[i])):
            h_ss_total=h_ss[i][j][0].GetPtr().Clone()
            h_ss_total.SetName(prefix+"_ss_etabin"+str(i)+"_etabin"+str(j)+"_mll")
            h_ss_total.Reset()
            h_os_total=h_os[i][j][0].GetPtr().Clone()
            h_os_total.SetName(prefix+"_os_etabin"+str(i)+"_etabin"+str(j)+"_mll")
            h_os_total.Reset()

            for k in range(0,len(h_ss[i][j])):
                h_ss_total.Add(h_ss[i][j][k].GetPtr())
                h_os_total.Add(h_os[i][j][k].GetPtr())

            fout.cd()
            h_ss_total.Write()
            h_os_total.Write()

    fout.Write("",ROOT.TObject.kOverwrite)
    fout.Close()

def count(filename):
    print('>>>>>>>>>>>>>>>>>>>> just count')
    eta_bin_array = array('f',[0.,0.5,1.0,1.5,2.0,2.5])
    fin=ROOT.TFile.Open(filename)
    histos=[]
    count={}
    count_err={}
    for tkey in fin.GetListOfKeys():
        key=tkey.GetName()
        #print(key)
        histos.append(key)
    for ihis in histos:
        print('fit to: ',ihis)
        htmp=fin.Get(ihis)
        err=ROOT.Double()
        count[ihis]=htmp.IntegralAndError(1,60,err)
        count_err[ihis]=err
        print '>>>>>> values:',count[ihis], err
    fout=ROOT.TFile('onlycount_'+filename,'recreate')
    h_ss_sub=ROOT.TH2D()
    h_os_sub=ROOT.TH2D()
    #samples=['DPS','WW_strong','FAKE','VVV','VZ','Vg','WW_EWK','TTV','DATA','DY']
    samples=['DATA','DY']
    ss_plots=[]
    os_plots=[]
    for isample in samples:
        #h_ss=ROOT.TH2D('h_ss_'+isample,'h_ss_'+isample,5,0.,2.5,5,0.,2.5)
        #h_os=ROOT.TH2D('h_os_'+isample,'h_os_'+isample,5,0.,2.5,5,0.,2.5)
        h_ss=ROOT.TH2D('h_ss_'+isample,'h_ss_'+isample,5,eta_bin_array,5,eta_bin_array)
        h_os=ROOT.TH2D('h_os_'+isample,'h_os_'+isample,5,eta_bin_array,5,eta_bin_array)
        for i in ['0','1','2','3','4']:
            for j in ['0','1','2','3','4']:
                h_ss.SetBinContent(int(i)+1,int(j)+1,count[isample+'_'+args.year+'_'+args.ptbin+"_ss_etabin"+i+"_etabin"+j+"_mll"])
                h_ss.SetBinError(int(i)+1,int(j)+1,count_err[isample+'_'+args.year+'_'+args.ptbin+"_ss_etabin"+i+"_etabin"+j+"_mll"])
                h_os.SetBinContent(int(i)+1,int(j)+1,count[isample+'_'+args.year+'_'+args.ptbin+"_os_etabin"+i+"_etabin"+j+"_mll"])
                h_os.SetBinError(int(i)+1,int(j)+1,count_err[isample+'_'+args.year+'_'+args.ptbin+"_os_etabin"+i+"_etabin"+j+"_mll"])
        if isample=='DATA':
            h_ss_sub=h_ss.Clone()
            h_ss_sub.SetName('h_ss_DATASUB')
            h_ss_sub.SetTitle('h_ss_DATASUB')
            h_os_sub=h_os.Clone()
            h_os_sub.SetName('h_os_DATASUB')
            h_os_sub.SetTitle('h_os_DATASUB')

        ss_plots.append(h_ss)
        os_plots.append(h_os)
    for i in range(0,len(ss_plots)):
        if ss_plots[i].GetName() != 'h_ss_DATA' and ss_plots[i].GetName() != 'h_ss_DY' and ss_plots[i].GetName() != 'h_ss_FAKE':
            h_ss_sub.Add(ss_plots[i],-1)
    for i in range(0,len(os_plots)):
        if os_plots[i].GetName() != 'h_os_DATA' and os_plots[i].GetName() != 'h_os_DY' and ss_plots[i].GetName() != 'h_os_FAKE':
            h_os_sub.Add(os_plots[i],-1)
    ss_plots.append(h_ss_sub)
    os_plots.append(h_os_sub)

    for i in range(0,len(ss_plots)):
        ss_plots[i].Write()
        os_plots[i].Write()
    fout.Close()

def fit(filename):
    print('>>>>>>>>>>>>>>>>>>>> perform fit')
    eta_bin_array = array('f',[0.,0.5,1.0,1.5,2.0,2.5])
    fin=ROOT.TFile.Open(filename)
    histos=[]
    count={}
    count_err={}
    for tkey in fin.GetListOfKeys():
        key=tkey.GetName()
        #print(key)
        histos.append(key)
    for ihis in histos:
        print('fit to: ',ihis)
        htmp=fin.Get(ihis)
        for ibin in range(0,30):
            if htmp.GetBinContent(ibin+1)<0:
                htmp.SetBinContent(ibin+1,0)
        # rebin
        #htmp.Rebin(2)
        nEvent=htmp.Integral()
        nHalf=0.8*nEvent
        w = ROOT.RooWorkspace("w")
        w.factory("BreitWigner:sig_bw(mll[76, 106], bwmean[91.1876,89,93],bwgamma[2.4952,2.4,2.6])")
        #w.factory("Landau:sig_lau(mll[76, 106], laumean[91.1876,89,93],lausigma[1,0.1,10])")
        w.factory("Gaussian:sig_gau(mll,gaumean[0,-100,100],gausigma[2.5,0.1,5])")
        #w.factory("CBShape:sig_cb(x, cbmean[0.,1.,10.], cbsigma[2.4952,2.4,2.6],cbalpha[20,0.,10],n[10,0.5,20])")
        w.factory("FCONV:bxc(mll,sig_bw,sig_gau)")
        w.factory("Exponential:bkg(mll,exalpha[-1.,-10,1])")
        # w.factory("SUM:model(sigfrac[0.5,0,1.]*bxc, bkgfrac[0.5,0,1.]*bkg)")
        w.factory("SUM:model(nsig["+str(nHalf)+",0,"+str(nEvent)+"]*bxc, nbkg["+str(nEvent-nHalf)+",0,"+str(nEvent)+"]*bkg)")
        mll=w.var('mll')
        pdf=w.pdf('model')
        dh=ROOT.RooDataHist('d'+ihis,'d'+ihis,ROOT.RooArgList(mll),htmp)
        getattr(w,'import')(dh)
        r = pdf.fitTo(dh, ROOT.RooFit.Save(True),ROOT.RooFit.Minimizer("Minuit2","Migrad"))
        #r = pdf.fitTo(dh, ROOT.RooFit.Save(True))
        #print('r.Print()       --------------------------------------------------------',w.var("nsig").getVal())
        #r.Print()
        c = ROOT.TCanvas()
        plot = mll.frame(ROOT.RooFit.Title(""))
        dh.plotOn(plot)
        pdf.plotOn(plot)
        pdf.plotOn(plot, ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineStyle(2))
        pdf.plotOn(plot, ROOT.RooFit.Components("bxc"), ROOT.RooFit.LineColor(2), ROOT.RooFit.LineStyle(2))
        pdf.paramOn(plot,ROOT.RooFit.Layout(0.57,0.97,0.85))
        plot.Draw()
        c.GetPrimitive("model_paramBox").SetFillStyle(0)
        c.GetPrimitive("model_paramBox").SetBorderSize(0)
        '''
        c.GetPrimitive("model_paramBox").SetTextFont(102)
        tbox_title_old=['bwgamma','bwmean','exalpha','gaumean','gausigma','nbkg','nsig']
        tbox_title_old=['bwgamma','bwmean','exalpha','gaumean','gausigma','nbkg','nsig']
        tbox_title_new=['#Gamma_{BW}','mean_{BW}','#alpha_{Exp}','mean_{Gau}','#sigma_{Gau}','n_{Bkg}','n_{Sig}']
        for i in range(0,7):
            _str=c.GetPrimitive("model_paramBox").GetLine(i).GetTitle()
            _str=_str.replace(tbox_title_old[i],tbox_title_new[i])
            c.GetPrimitive("model_paramBox").GetLine(i).SetTitle(_str)
        '''

        c.SaveAs('c_'+ihis+'.png')
        mc = ROOT.RooStats.ModelConfig("ModelConfig_"+ihis,w)
        mc.SetPdf(pdf)
        mc.SetParametersOfInterest(ROOT.RooArgSet(w.var("nsig")))
        mc.SetSnapshot(ROOT.RooArgSet(w.var("nsig")))
        mc.SetObservables(ROOT.RooArgSet(w.var("mll")))
        #w.defineSet("nuisParams","nbkg,laumean,lausigma,gaumean,gausigma,exalpha")
        w.defineSet("nuisParams","nbkg,bwmean,bwgamma,gaumean,gausigma,exalpha")
        nuis = getattr(w,'set')("nuisParams")
        mc.SetNuisanceParameters(nuis)
        getattr(w,'import')(mc)
        w.writeToFile(ihis+"_config.root",True)
        count[ihis]=w.var("nsig").getVal()
        count_err[ihis]=w.var("nsig").getError()
    #print(count)
    #print(count_err)
    fout=ROOT.TFile('count_'+filename,'recreate')
    h_ss_sub=ROOT.TH2D()
    h_os_sub=ROOT.TH2D()
    #samples=['DPS','WW_strong','FAKE','VVV','VZ','Vg','WW_EWK','TTV','DATA','DY']
    samples=['DATA','DY']
    ss_plots=[]
    os_plots=[]
    for isample in samples:
        #h_ss=ROOT.TH2D('h_ss_'+isample,'h_ss_'+isample,5,0.,2.5,5,0.,2.5)
        #h_os=ROOT.TH2D('h_os_'+isample,'h_os_'+isample,5,0.,2.5,5,0.,2.5)
        h_ss=ROOT.TH2D('h_ss_'+isample,'h_ss_'+isample,5,eta_bin_array,5,eta_bin_array)
        h_os=ROOT.TH2D('h_os_'+isample,'h_os_'+isample,5,eta_bin_array,5,eta_bin_array)
        for i in ['0','1','2','3','4']:
            for j in ['0','1','2','3','4']:
                h_ss.SetBinContent(int(i)+1,int(j)+1,count[isample+'_'+args.year+'_'+args.ptbin+"_ss_etabin"+i+"_etabin"+j+"_mll"])
                h_ss.SetBinError(int(i)+1,int(j)+1,count_err[isample+'_'+args.year+'_'+args.ptbin+"_ss_etabin"+i+"_etabin"+j+"_mll"])
                h_os.SetBinContent(int(i)+1,int(j)+1,count[isample+'_'+args.year+'_'+args.ptbin+"_os_etabin"+i+"_etabin"+j+"_mll"])
                h_os.SetBinError(int(i)+1,int(j)+1,count_err[isample+'_'+args.year+'_'+args.ptbin+"_os_etabin"+i+"_etabin"+j+"_mll"])
        if isample=='DATA':
            h_ss_sub=h_ss.Clone()
            h_ss_sub.SetName('h_ss_DATASUB')
            h_ss_sub.SetTitle('h_ss_DATASUB')
            h_os_sub=h_os.Clone()
            h_os_sub.SetName('h_os_DATASUB')
            h_os_sub.SetTitle('h_os_DATASUB')

        ss_plots.append(h_ss)
        os_plots.append(h_os)
    for i in range(0,len(ss_plots)):
        if ss_plots[i].GetName() != 'h_ss_DATA' and ss_plots[i].GetName() != 'h_ss_DY' and ss_plots[i].GetName() != 'h_ss_FAKE':
            h_ss_sub.Add(ss_plots[i],-1)
    for i in range(0,len(os_plots)):
        if os_plots[i].GetName() != 'h_os_DATA' and os_plots[i].GetName() != 'h_os_DY' and ss_plots[i].GetName() != 'h_os_FAKE':
            h_os_sub.Add(os_plots[i],-1)
    ss_plots.append(h_ss_sub)
    os_plots.append(h_os_sub)

    for i in range(0,len(ss_plots)):
        ss_plots[i].Write()
        os_plots[i].Write()
    fout.Close()

    #print(count)
def ratio(filename):
    fin=ROOT.TFile.Open(filename)
    h_ss=fin.Get('h_ss_DATASUB')
    h_os=fin.Get('h_os_DATASUB')
    '''
    h_ratio=ROOT.TH2D('h2','N_{SS}/N_{OS}',5,0.,2.5,5,0.,2.5)
    for i in range(0,5):
        for j in range(0,5):
            ssVal=h_ss.GetBinContent(i+1,j+1)
            osVal=h_os.GetBinContent(i+1,j+1)
            ssErr=h_ss.GetBinError(i+1,j+1)
            osErr=h_os.GetBinError(i+1,j+1)
            h_ratio.SetBinContent(i+1,j+1,ssVal/osVal)
            h_ratio.SetBinError(i+1,j+1,sqrt(pow(ssErr*osVal,2)+pow(osErr*ssVal,2)))
    '''
    h_ratio=h_ss.Clone()
    h_ratio.Divide(h_os)
    for i in range(0,h_ratio.GetNbinsX()):
        for j in range(0,h_ratio.GetNbinsY()):
            if h_ss.GetBinContent(i+1,j+1)<10:
                h_ratio.SetBinContent(i+1,j+1,0)
                h_ratio.SetBinError(i+1,j+1,0)
    h_ratio.SetName('h2_DATASUB')
    h_ratio.SetTitle('N_{SS}/N_{OS}')
    fout=ROOT.TFile('ratio_DATASUB'+filename,'recreate')
    h_ratio.Write()
    fout.Write()
    fout.Close()

    c=ROOT.TCanvas()
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPaintTextFormat("1.4f")
    h_ss.Draw("colz texte")
    c.SaveAs('h_ss_DATASUB_'+args.year+'_'+args.ptbin+'.png')
    c.Clear()
    h_os.Draw("colz texte")
    c.SaveAs('h_os_DATASUB_'+args.year+'_'+args.ptbin+'.png')
    c.Clear()
    h_ratio.Draw("colz texte")
    c.SaveAs('h_ratio_DATA_'+args.year+'_'+args.ptbin+'.png')

    h_ss=fin.Get('h_ss_DY')
    h_os=fin.Get('h_os_DY')
    h_ratio=h_ss.Clone()
    h_ratio.Divide(h_os)
    for i in range(0,5):
        for j in range(0,5):
            if h_ss.GetBinContent(i+1,j+1)<10:
                h_ratio.SetBinContent(i+1,j+1,0)
                h_ratio.SetBinError(i+1,j+1,0)
    h_ratio.SetName('h2_DY')
    h_ratio.SetTitle('N_{SS}/N_{OS}')
    fout=ROOT.TFile('ratio_DY'+filename,'recreate')
    h_ratio.Write()
    fout.Write()
    fout.Close()

    h_ss.Draw("colz texte")
    c.SaveAs('h_ss_DY_'+args.year+'_'+args.ptbin+'.png')
    c.Clear()
    h_os.Draw("colz texte")
    c.SaveAs('h_os_DY_'+args.year+'_'+args.ptbin+'.png')
    c.Clear()
    h_ratio.Draw("colz texte")
    c.SaveAs('h_ratio_DY_'+args.year+'_'+args.ptbin+'.png')

if __name__ == '__main__':
    path=args.input+'/'+args.year+'/'+args.poststep
    if not os.path.exists(path):
        os.mkdir(path)
    samples, data_chain, mc_chain = SAMPLE.set_samples(args.year)

    with open('xs_' + args.year + '_nano_v4_v1.py','r') as collect:
        exec (collect)
        _XSDB = XSDB

    if args.plot:
        fout_plots=ROOT.TFile(path+'/'+'plots_'+args.year+'_'+args.ptbin+'.root','recreate')
        fout_plots.Write()
        fout_plots.Close()

        for sample_name in ['DY4','DoubleEG']:
            files=samples[sample_name]
            weight=[]
            if 'DY' in sample_name:
                for i in range(0,len(samples[sample_name])):
                    tmp_name=files[i]
                    xsweight=str(_XSDB[tmp_name[:len(tmp_name)-5]]['xsweight'])
                    weight.append(str(xsweight)+'*gen_weight/abs(gen_weight)')
            else:
                for i in range(0,len(samples[sample_name])):
                    weight.append('1.')
            print ">>>>>>>>>>>>>>>>>>>>> start plot: ",sample_name
            save_plot(files,weight,sample_name+'_'+args.year+'_'+args.ptbin)
    if args.count:
        count('chargeflip_plots_'+args.year+'_'+args.ptbin+'.root')
    if args.fit:
        fit('chargeflip_plots_'+args.year+'_'+args.ptbin+'.root')
    if args.ratio:
        ratio('justcount_chargeflip_plots_'+args.year+'_'+args.ptbin+'.root')

    #df_unc.Snapshot("Events", "newWpWpJJ_EWK.root")
