import ROOT
import os
import argparse
import SAMPLE

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-s','--subtract', help='subtract real lepton',action='store_false', default= True)
group = parser.add_mutually_exclusive_group()  # type: _MutuallyExclusiveGroup
group.add_argument('-c','--channel', help='muon/electron fake rate', choices=('muon','electron'),default='muon')
group.add_argument('-a','--all', help='muon and electron fake rate',action='store_true', default= False)
args = parser.parse_args()


ROOT.ROOT.EnableImplicitMT()

def add_files(samples, chain, exclude):
    path = '/path/to/ntuple/'
    files = []
    for isample in chain:
        if not isample in exclude:
            for i in range(0,len(samples[isample])):
                files.append(path+samples[isample][i])
    return files

def get_plot(name, trigger, PID, files, isdata):

    fake_cut = trigger + '&& lepton_fakeable[0] && lepton_pdg_id[0] ==' + PID + '&& met < 30'
    tight_cut = trigger + '&& lepton_tight[0] && lepton_pdg_id[0] ==' + PID + '&& met < 30'
    real_fake = trigger + '&& lepton_real[0] && lepton_fakeable[0] && lepton_pdg_id[0] ==' + PID + '&& met < 30'
    real_tight = trigger + '&& lepton_real[0] && lepton_tight[0] && lepton_pdg_id[0] ==' + PID + '&& met < 30'
    if isdata:
        fake_selections = fake_cut
        true_selections = tight_cut
    else:
        fake_selections = real_fake
        true_selections = real_tight

    df = ROOT.ROOT.RDataFrame("Events", files)
    # For simplicity, select only events with exactly two muons and require opposite charge
    fake_template = df.Filter('nLepton == 1').Filter(fake_selections) \
        .Define('mt','sqrt(2*lepton_pt[0]*event.met*(1 - cos(met_phi - lepton_phi[0])))').Filter('mt<20') \
        .Define('abs_eta','abs(lepton_eta[0])').Define('pt_tmp','if(lepton_pt[0]>35) return 32.5; else return (double)lepton_pt[0];') \
        .Histo2D({"fake_"+name, "fake;|#eta|;p_{T} (GeV)", 5, {0., 0.5, 1., 1.479, 2., 2.5}, 3, {20, 25, 30, 35}}, "abs_eta", "pt_tmp")
    fake_template.Sumw2()

    tight_template = df.Filter('nLepton == 1').Filter(true_selections) \
        .Define('mt','sqrt(2*lepton_pt[0]*event.met*(1 - cos(met_phi - lepton_phi[0])))').Filter('mt<20') \
        .Define('abs_eta','abs(lepton_eta[0])').Define('pt_tmp','if(lepton_pt[0]>35) return 32.5; else return (double)lepton_pt[0];') \
        .Histo2D({"tight_"+name, "tight;|#eta|;p_{T} (GeV)", 5, {0., 0.5, 1., 1.479, 2., 2.5}, 3, {20, 25, 30, 35}}, "abs_eta", "pt_tmp")
    tight_template.Sumw2()

    return fake_template, tight_template

def calc(_channel):
    # Enable multi-threading
    # Create dataframe from NanoAOD files

    # include = []
    # exclude = []
    fout = ROOT.TFile('fakerate_'+_channel+'.root','recreate')
    samples, data_chain, mc_chain = SAMPLE.set_samples()
    if _channel == 'muon':
        trigger = 'HLT_Mu17_TrkIsoVVL'
        PID = '13'
        files = add_files(samples, data_chain,['SingleMuon','SingleElectron','MuonEG','DoubleEG'])
        sig = ROOT.std.vector("string")(len(files))
        for i in range(0,len(files)):
            sig[i]=files[i]
    elif _channel == 'electron':
        trigger = 'HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 && HLT_Ele17_CaloIdL_TrackIdL_IsoVL_PFJet30 && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30'
        PID = '11'
        files = add_files(samples, data_chain,['SingleMuon','SingleElectron','MuonEG','DoubleMuon'])
        sig = ROOT.std.vector("string")(len(files))
        for i in range(0,len(files)):
            sig[i]=files[i]
    else:
        return
    h2_fake_data, h2_true_data = get_plot('data',trigger, PID, sig,True)
    h2_fake_data.Write()
    h2_true_data.Write()
    h2_ratio= h2_true_data
    h2_ratio.SetName('fakerate')
    h2_ratio.SetTitle('fakerate')
    h2_ratio.Divide(h2_fake_data)

    ROOT.gStyle.SetPaintTextFormat("4.2f")
    c1=ROOT.TCanvas("c1", "c1", 1200, 900)
    h2_ratio.Draw("texte colz")
    c1.SaveAs("fakerate.pdf")

    if args.subtract:
        h2_fake_tmp, h2_true_tmp = h2_fake_data, h2_true_data
        h2_fake_tmp.SetName('fake_data_subtrct')
        h2_true_tmp.SetName('true_data_subtrct')
        for imc in mc_chain:
            mc_chain_single = []
            mc_chain_single.append(imc)
            files = add_files(samples, mc_chain_single,['WZ1','WZ2'])
            bkg = ROOT.std.vector("string")(len(files))
            for i in range(0,len(files)):
                bkg[i]=files[i]
            h2_fake_mc, h2_true_mc = get_plot(imc,trigger, PID, bkg, False)
            h2_fake_mc.Write()
            h2_true_mc.Write()
            h2_fake_tmp.Add(h2_fake_mc,-1)
            h2_true_tmp.Add(h2_true_mc,-1)
        h2_fake_tmp.Write()
        h2_true_tmp.Write()
        h2_ratio_subtract= h2_true_tmp
        h2_ratio_subtract.SetName('fakerate_subtract')
        h2_ratio_subtract.SetTitle('fakerate_subtract')
        h2_ratio_subtract.Divide(h2_fake_tmp)
        h2_ratio_subtract.Write()

        c2=ROOT.TCanvas("c2", "c2", 1200, 900)
        h2_ratio_subtract.Draw("texte colz")
        c2.SaveAs("fakerate_subtract.pdf")

'''
    if args.subtract:
        real_fake_sub = df.Filter('nLepton == 1').Filter(real_fake) \
            .Define('mt','sqrt(2*lepton_pt[0]*event.met*(1 - cos(met_phi - lepton_phi[0])))').Filter('mt<20') \
            .Define('abs_eta','abs(lepton_eta[0])').Define('pt_tmp','if(lepton_pt[0]>35) return 32.5; else return (double)lepton_pt[0];') \
            .Histo2D({"real_fake", "real_fake;|#eta|;p_{T}", 5, {0., 0.5, 1., 1.479, 2., 2.5}, 3, {20, 25, 30, 35}}, "abs_eta", "pt_tmp","-1.*scale")
        real_fake_sub.Sumw2()

        real_tight_sub =  df.Filter('nLepton == 1').Filter(real_tight) \
            .Define('mt','sqrt(2*lepton_pt[0]*event.met*(1 - cos(met_phi - lepton_phi[0])))').Filter('mt<20') \
            .Define('abs_eta','abs(lepton_eta[0])').Define('pt_tmp','if(lepton_pt[0]>35) return 32.5; else return (double)lepton_pt[0];') \
            .Histo2D({"real_tight", "real_tight;|#eta|;p_{T}", 5, {0., 0.5, 1., 1.479, 2., 2.5}, 3, {20, 25, 30, 35}}, "abs_eta", "pt_tmp","-1.*scale")
        real_tight_sub.Sumw2()

        tight_template.Add(real_tight_sub.GetPtr())
        fake_template.Add(real_fake_sub.GetPtr())
        tight_template.Divide(fake_template.GetPtr())
    else:
        tight_template.Divide(fake_template.GetPtr())
'''


if __name__ == '__main__':
    if args.all:
        calc('muon')
        calc('electron')
    else:
        calc(args.channel)
