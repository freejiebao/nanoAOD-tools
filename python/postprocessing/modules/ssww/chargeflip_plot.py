import ROOT
import SAMPLE
import numpy as np

ROOT.ROOT.EnableImplicitMT()

zmass = '91.1876'
def save_plot(df):
    print('>>>>>>>>>>>>>>>>>>>> save plots')
    #df = ROOT.ROOT.RDataFrame("Events", files)
    fout=ROOT.TFile('chargeflip_plots.root','recreate')
    df1=df.Filter('nlepton == 2 && lepton_pt[0] > 20 && lepton_pt[2] > 20 && abs(mll-%s) < 15 && lepton_tight[0] && lepton_tight[1]') % zmass
    # pt_bin=['0.','20.']
    eta_bin = ['0.','0.5','1.0','1.5','2.0','2.5']
    regions=np.zeros((5,5),dtype=np.object)
    for i in range(len(regions)):
        for j in range(len(regions[i])):
            regions[i][j]='abs(lepton_eta[0])>=%s && abs(lepton_eta[0])<%s && abs(lepton_eta[1])>=%s && abs(lepton_eta[1])<%s' %(eta_bin[i],eta_bin[i+1],eta_bin[j],eta_bin[j+1])

    # same-sign
    df_ss=df1.Filter('lepton_pdg_id[0]*lepton_pdg_id[1] == 11*11')
    for i in range(len(regions)):
        for j in range(len(regions[i])):
            df_tmp=df_ss.Filter(regions[i][j])
            histo=df_tmp.Histo1D(("ss_etabin"+str(i)+"_etabin"+str(j)+"_mll", "mll", 30, 76.1876, 106.1876), "mll","weight")
            histo.Write()

    # opposite-sign
    df_os=df1.Filter('lepton_pdg_id[0]*lepton_pdg_id[1] == -11*11')
    for i in range(len(regions)):
        for j in range(len(regions[i])):
            df_tmp=df_os.Filter(regions[i][j])
            histo=df_tmp.Histo1D(("os_etabin"+str(i)+"_etabin"+str(j)+"_mll", "mll", 40, 70, 110), "mll","weight")
            histo.Write()
    fout.Write()
    fout.Close()

def fit():
    print('>>>>>>>>>>>>>>>>>>>> perform fit')
    nEvent=10000
    nHalf=0.5*nEvent
    w = ROOT.RooWorkspace("w")
    w.factory("BreitWigner:sig_bw(x[76.1876, 106.1876], bwmean[91.1876,89,93],bwgamma[7.5,0.,30.])")
    w.factory("CBShape:sig_cb(x, cbmean[91.1876,89,93], cbsigma[7.5,0.,30.],cbalpha[1,1,10],n[1,1,5])")
    w.factory("FCONV:bxc(x,sig_bw,sig_cb)")
    w.factory("Exponential:bkg(x,exalpha[-1.,-10,-0.1])")
    # w.factory("SUM:model(sigfrac[0.5,0,1.]*bxc, bkgfrac[0.5,0,1.]*bkg)")
    w.factory("SUM:model(nsig[%s,0,%s]*bxc, nbkg[%s,0,%s]*bkg)") %(str(nEvent),str(nHalf),str(nEvent),str(nHalf))


if __name__ == '__main__':
    df = ROOT.ROOT.RDataFrame("Events", 'WpWpJJ_EWK.root')
    df_unc = save_plot(df)
    #df_unc.Snapshot("Events", "newWpWpJJ_EWK.root")
