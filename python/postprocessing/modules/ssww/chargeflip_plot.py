import argparse
import ROOT
import SAMPLE
import numpy as np

ROOT.ROOT.EnableImplicitMT(8)
ROOT.gROOT.SetBatch(ROOT.kTRUE)

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-p','--plot', help='make mll distribution, default is true',action='store_false', default= True)
parser.add_argument('-f','--fit', help='fit to mll distribution, default is true',action='store_false', default= True)
args = parser.parse_args()

zmass = '91.1876'
def save_plot(df):
    print('>>>>>>>>>>>>>>>>>>>> save plots')
    #df = ROOT.ROOT.RDataFrame("Events", files)
    fout=ROOT.TFile('chargeflip_plots.root','recreate')
    df1=df.Filter('nlepton == 2 && lepton_pt[0] > 20 && lepton_pt[2] > 20 && abs(mll-'+zmass+') < 15 && lepton_tight[0] && lepton_tight[1]')
    # pt_bin=['0.','20.']
    eta_bin = ['0.','0.5','1.0','1.5','2.0','2.5']
    regions=np.zeros((5,5),dtype=np.object)
    for i in range(len(regions)):
        for j in range(len(regions[i])):
            regions[i][j]='abs(lepton_eta[0])>='+eta_bin[i]+' && abs(lepton_eta[0])<'+eta_bin[i+1]+' && abs(lepton_eta[1])>='+eta_bin[j]+' && abs(lepton_eta[1])<'+eta_bin[j+1]

    # same-sign
    df_ss=df1.Filter('lepton_pdg_id[0]*lepton_pdg_id[1] == 11*11')
    for i in range(len(regions)):
        for j in range(len(regions[i])):
            df_tmp=df_ss.Filter(regions[i][j])
            histo=df_tmp.Histo1D(("ss_etabin"+str(i)+"_etabin"+str(j)+"_mll", "mll", 30, 76.1876, 106.1876), "mll")
            histo.Write()

    # opposite-sign
    df_os=df1.Filter('lepton_pdg_id[0]*lepton_pdg_id[1] == -11*11')
    for i in range(len(regions)):
        for j in range(len(regions[i])):
            df_tmp=df_os.Filter(regions[i][j])
            histo=df_tmp.Histo1D(("os_etabin"+str(i)+"_etabin"+str(j)+"_mll", "mll", 30, 76.1876, 106.1876), "mll","weight")
            histo.Write()
    fout.Write()
    fout.Close()

def fit():
    print('>>>>>>>>>>>>>>>>>>>> perform fit')
    fin=ROOT.TFile('chargeflip_plots.root')
    histos=[]
    for tkey in fin.GetListOfKeys():
        key=tkey.GetName()
        #print(key)
        histos.append(key)
    for ihis in histos:
        print 'fit to: ',ihis
        htmp=fin.Get(ihis)
        nEvent=htmp.Integral()
        nHalf=0.5*nEvent
        w = ROOT.RooWorkspace("w")
        w.factory("BreitWigner:sig_bw(x[76.1876, 106.1876], bwmean[91.1876,89,93],bwgamma[2.4952,2.4,2.6])")
        w.factory("CBShape:sig_cb(x, cbmean[0.,-1.,1.], cbsigma[2.4952,2.4,2.6],cbalpha[1.2,1,10],n[0.81,0.5,5])")
        w.factory("FCONV:bxc(x,sig_bw,sig_cb)")
        w.factory("Exponential:bkg(x,exalpha[-1.,-10,-0.1])")
        # w.factory("SUM:model(sigfrac[0.5,0,1.]*bxc, bkgfrac[0.5,0,1.]*bkg)")
        w.factory("SUM:model(nsig["+str(nHalf)+",0,"+str(nEvent)+"]*bxc, nbkg["+str(nHalf)+",0,"+str(nEvent)+"]*bkg)")
        x=w.var('x')
        pdf=w.pdf('model')
        dh=ROOT.RooDataHist('d'+ihis,'d'+ihis,ROOT.RooArgList(x),htmp)
        getattr(w,'import')(dh)
        r = pdf.fitTo(dh, ROOT.RooFit.Save(True), ROOT.RooFit.Minimizer("Minuit2","Migrad"))
        r.Print()
        c = ROOT.TCanvas()
        plot = x.frame(ROOT.RooFit.Title("Fit to: "+ihis))
        dh.plotOn(plot)
        pdf.plotOn(plot)
        pdf.plotOn(plot, ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineStyle(2))
        pdf.plotOn(plot, ROOT.RooFit.Components("bxc"), ROOT.RooFit.LineColor(2), ROOT.RooFit.LineStyle(2))
        pdf.paramOn(plot,ROOT.RooFit.Layout(0.5,0.9,0.85))
        plot.Draw()
        c.SaveAs('c_'+ihis+'.pdf')
        mc = ROOT.RooStats.ModelConfig("ModelConfig_"+ihis,w)
        mc.SetPdf(pdf)
        mc.SetParametersOfInterest(ROOT.RooArgSet(w.var("nsig")))
        mc.SetSnapshot(ROOT.RooArgSet(w.var("nsig")))
        mc.SetObservables(ROOT.RooArgSet(w.var("x")))
        w.defineSet("nuisParams","nbkg,bwmean,bwgamma,cbmean,cbsigma,cbalpha,exalpha")
        nuis = getattr(w,'set')("nuisParams")
        mc.SetNuisanceParameters(nuis)
        getattr(w,'import')(mc)
        w.writeToFile("output/"+ihis+"_config.root",True)

if __name__ == '__main__':
    if args.plot:
        df = ROOT.ROOT.RDataFrame("Events", '/eos/user/l/llinwei/jie/ssww_ntuple/2016/WpWpJJ_EWK.root')
        save_plot(df)
    if args.fit:
        fit()
    #df_unc.Snapshot("Events", "newWpWpJJ_EWK.root")
