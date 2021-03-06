import ROOT
import argparse
import SAMPLE
from array import array

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-s','--subtract', help='subtract real lepton, default is false',action='store_true', default= False)
parser.add_argument('-i','--input', help='input path', default= '/home/cmsdas/testuser01/jie/ssww_ntuple/')
parser.add_argument('-y','--year', help='which year, default is 2016', default= '2016', choices=('2016','2017','2018'))
parser.add_argument('-post','--poststep', help='declare poststep path postfix', default= 'fakelepton')
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
group_mc.add_argument('-ex','--exclude', help='exclude samples',nargs='*',default=['WZ0','WZ2'])
args = parser.parse_args()


ROOT.ROOT.EnableImplicitMT(70)
ROOT.gROOT.SetBatch(ROOT.kTRUE)

def get_plot(name, trigger, PID, files, isdata):
    eta_bin = array('f',[0., 0.5, 1., 1.479, 2., 2.5])
    pt_bin = array('f',[20, 25, 30, 35, 45])
    '''
    fake_cut = trigger + '&& lepton_fakeable[0] && abs(lepton_pdgId[0]) ==' + PID + '&& met < 30'
    tight_cut = trigger + '&& lepton_tight[0] && abs(lepton_pdgId[0]) ==' + PID + '&& met < 30'
    real_fake = trigger + '&& lepton_real[0] && lepton_fakeable[0] && abs(lepton_pdgId[0]) ==' + PID + '&& met < 30'
    real_tight = trigger + '&& lepton_real[0] && lepton_tight[0] && abs(lepton_pdgId[0]) ==' + PID + '&& met < 30'
    '''
    fake_cut = 'lepton_fakeable[0] && abs(lepton_pdgId[0]) ==' + PID + '&& met < 30'
    tight_cut = 'lepton_tight[0] && abs(lepton_pdgId[0]) ==' + PID + '&& met < 30'
    real_fake = 'lepton_real[0] && lepton_fakeable[0] && abs(lepton_pdgId[0]) ==' + PID + '&& met < 30'
    real_tight = 'lepton_real[0] && lepton_tight[0] && abs(lepton_pdgId[0]) ==' + PID + '&& met < 30'

    tight_plot = []
    fake_plot = []
    if not isdata:
        with open('xs_' + args.year + '_nano_v4_v1.py','r') as collect:
            exec (collect)
            _XSDB = XSDB


    for i in range(0,len(files)):
        if isdata:
            fake_selections = fake_cut
            true_selections = tight_cut
            weight='1.'
        else:
            fake_selections = real_fake
            true_selections = real_tight
            tmp_name=files[i].split('/')
            sample_name=tmp_name[len(tmp_name)-1]
            xsweight=str(_XSDB[sample_name[:len(sample_name)-5]]['xsweight'])
            weight=str(xsweight)+'*(gen_weight/abs(gen_weight))'
            #tmpfile=ROOT.TFile(files[i])
            #xsweight=tmpfile.Get("xsweight").GetBinContent(1)
            #tmpfile.Close()

        df = ROOT.ROOT.RDataFrame("Events", files[i])
        # df.Count().GetValue()
        print '>>>>>>>>>>>>>>>>>>>> the opened file: ',files[i]
        # For simplicity, select only events with exactly two muons and require opposite charge
        tmpplot=df.Filter('nlepton == 1').Filter(fake_selections).Filter('mt<20') \
            .Define('abs_eta','abs(lepton_eta[0])').Define('pt_tmp','if(lepton_pt[0]>44.9) return 40.; else return (double)lepton_pt[0];') \
            .Define('weight',weight) \
            .Histo2D(("fake_"+name+"_"+str(i), "fake;|#eta|;p_{T} (GeV)", 5, eta_bin, 4, pt_bin), "abs_eta", "pt_tmp","weight")
        tmpplot.Sumw2()
        fake_plot.append(tmpplot)

        tmpplot = df.Filter('nlepton == 1').Filter(true_selections).Filter('mt<20')\
            .Define('abs_eta','abs(lepton_eta[0])').Define('pt_tmp','if(lepton_pt[0]>44.9) return 40.; else return (double)lepton_pt[0];') \
            .Define('weight',weight) \
            .Histo2D(("tight_"+name+"_"+str(i), "tight;|#eta|;p_{T} (GeV)", 5, eta_bin, 4, pt_bin), "abs_eta", "pt_tmp","weight")
        tmpplot.Sumw2()
        tight_plot.append(tmpplot)

    fake_template=fake_plot[0].Clone()
    tight_template=tight_plot[0].Clone()
    fake_template.SetName("fake_"+name)
    tight_template.SetName("tight_"+name)
    for i in range(0,len(tight_plot)-1):
        fake_template.Add(fake_plot[i+1].GetPtr())
        tight_template.Add(tight_plot[i+1].GetPtr())

    return fake_template, tight_template

def calc(_channel,_year):
    # Enable multi-threading
    # Create dataframe from NanoAOD files

    # include = []
    # exclude = []
    samples, data_chain, mc_chain = SAMPLE.set_samples(_year)
    if _channel == 'muon':
        trigger = 'HLT_Mu17_TrkIsoVVL'
        PID = '13'
        if _year=='2018':
            exdata=['SingleMuon','EGamma','MuonEG']
        else:
            exdata=['SingleMuon','SingleElectron','MuonEG','DoubleEG']

        files = SAMPLE.add_files(_year,args.input, samples, data_chain,exdata,[],args.poststep)
        # files = ['DoubleMuon_Run2017C.root']
        sig = ROOT.std.vector("string")(len(files))
        for i in range(0,len(files)):
            sig[i]=files[i]
    elif _channel == 'electron':
        trigger = '(HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 || HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 || HLT_Ele17_CaloIdL_TrackIdL_IsoVL_PFJet30 || HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30)'
        PID = '11'
        if _year=='2018':
            exdata=['SingleMuon','DoubleMuon','MuonEG']
        else:
            exdata=['SingleMuon','SingleElectron','MuonEG','DoubleMuon']
        files = SAMPLE.add_files(_year,args.input, samples, data_chain,exdata,[],args.poststep)
        sig = ROOT.std.vector("string")(len(files))
        for i in range(0,len(files)):
            sig[i]=files[i]
    else:
        return
    h2_fake_data, h2_true_data = get_plot('data',trigger, PID, sig,True)
    h2_ratio= h2_true_data.Clone()
    h2_ratio.SetName('fakerate')
    h2_ratio.SetTitle('fakerate')
    h2_ratio.Divide(h2_fake_data)
    h2_fake_tmp=h2_fake_data.Clone()
    h2_true_tmp=h2_true_data.Clone()
    h2_fake_tmp.SetName('fake_data_subtrct')
    h2_fake_tmp.SetTitle('fake_data_subtrct')
    h2_true_tmp.SetName('true_data_subtrct')
    h2_true_tmp.SetTitle('true_data_subtrct')
    h2_fake_mc_plot=[]
    h2_true_mc_plot=[]

    ROOT.gStyle.SetPaintTextFormat("4.2f")
    c1=ROOT.TCanvas("c1", "c1", 1200, 900)
    h2_ratio.Draw("texte colz")
    c1.SaveAs("fakerate.pdf")
    c2=ROOT.TCanvas("c2", "c2", 1200, 900)

    if args.subtract:
        for imc in mc_chain:
            mc_chain_single = []
            mc_chain_single.append(imc)
            files = SAMPLE.add_files(_year,args.input, samples, mc_chain_single,args.exclude,args.include,args.poststep)
            bkg = ROOT.std.vector("string")(len(files))
            if not len(files)==0:
                for i in range(0,len(files)):
                    print ">>>>>>>> i", files[i]
                    bkg[i] = files[i]
                print ">>>>>>>", imc, PID, bkg
                h2_fake_mc, h2_true_mc = get_plot(imc,trigger, PID, bkg, False)
                h2_fake_mc_plot.append(h2_fake_mc)
                h2_true_mc_plot.append(h2_true_mc)
                h2_fake_tmp.Add(h2_fake_mc,-1)
                h2_true_tmp.Add(h2_true_mc,-1)
        h2_ratio_subtract= h2_true_tmp.Clone()
        h2_ratio_subtract.SetName('fakerate_subtract')
        h2_ratio_subtract.SetTitle('fakerate_subtract')
        h2_ratio_subtract.Divide(h2_fake_tmp)

        h2_ratio_subtract.Draw("texte colz")
        c2.SaveAs("fakerate_subtract.pdf")

    fout = ROOT.TFile(_year+'_'+'fakerate_'+_channel+'.root','recreate')
    h2_fake_data.Write()
    h2_true_data.Write()
    h2_ratio.Write()

    if args.subtract:
        for i in range(0,len(h2_fake_mc_plot)):
            h2_fake_mc_plot[i].Write()
            h2_true_mc_plot[i].Write()
        h2_fake_tmp.Write()
        h2_true_tmp.Write()
        h2_ratio_subtract.Write()

    fout.Write()
    fout.Close()
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

    #print ('>>>>>>>>>>>>>>>>>>>> exclude: ',args.exclude)
    #print ('>>>>>>>>>>>>>>>>>>>> include: ',args.include)

    if args.all:
        calc('muon',args.year)
        calc('electron',args.year)
    else:
        calc(args.channel,args.year)
