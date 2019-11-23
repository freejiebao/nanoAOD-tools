import os

import ROOT
import argparse
from array import array
import SAMPLE
ROOT.ROOT.EnableImplicitMT(8)

import numpy
from math import sqrt
import math

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-d','--dataset', help='which dataset to use [SingleMuon,SingleElectron,DoubleMuon,DoubleEG,MuonEG,DY...]',default= 'DoubleEG')
parser.add_argument('-t','--type', help='which type of the dataset: data/mc, default is mc',default= 'mc', choices=('data','mc'))
parser.add_argument('-y','--year', help='which year: 2016/2017/2018, default is 2016',default= '2016', choices=('2016','2017','2018'))
parser.add_argument('-i','--input', help='input path', default= '/home/cmsdas/testuser01/jie/ssww_ntuple/')
parser.add_argument('-post','--poststep', help='declare poststep path postfix', default= 'chargeflip')
parser.add_argument('-pre','--prestep', help='declare prestep path postfix', default= '')
args = parser.parse_args()

ROOT.ROOT.EnableImplicitMT(32)

def KeepColumns():
    branchList = ROOT.vector('string')()

    branches_data_2016=['run','lumi','event','lep1_pt','lep1_eta','lep1_pdgId','lep1_tight','lep1_mishits','lep1_tkIsoId','lep2_pt','lep2_eta','lep2_pdgId','lep2_tight','lep2_mishits','lep2_tkIsoId','mll']
    branches_mc_2016=['run','lumi','event','lep1_pt','lep1_eta','lep1_pdgId','lep1_tight','lep1_mishits','lep1_tkIsoId','lep2_pt','lep2_eta','lep2_pdgId','lep2_tight','lep2_mishits','lep2_tkIsoId','genmatch2l','mll']

    branches_data_2017=['run','lumi','event','lep1_pt','lep1_eta','lep1_pdgId','lep1_tight','lep1_mishits','lep1_tkIsoId','lep2_pt','lep2_eta','lep2_pdgId','lep2_tight','lep2_mishits','lep2_tkIsoId','mll']
    branches_mc_2017=['run','lumi','event','lep1_pt','lep1_eta','lep1_pdgId','lep1_tight','lep1_mishits','lep1_tkIsoId','lep2_pt','lep2_eta','lep2_pdgId','lep2_tight','lep2_mishits','lep2_tkIsoId','genmatch2l','mll']

    branches_data_2018=['run','lumi','event','lep1_pt','lep1_eta','lep1_pdgId','lep1_tight','lep1_mishits','lep1_tkIsoId','lep2_pt','lep2_eta','lep2_pdgId','lep2_tight','lep2_mishits','lep2_tkIsoId','mll']
    branches_mc_2018=['run','lumi','event','lep1_pt','lep1_eta','lep1_pdgId','lep1_tight','lep1_mishits','lep1_tkIsoId','lep2_pt','lep2_eta','lep2_pdgId','lep2_tight','lep2_mishits','lep2_tkIsoId','genmatch2l','mll']

    if args.type=='data':
        if args.year=='2016':
            for i in range(0,len(branches_data_2016)):
                branchList.push_back(branches_data_2016[i])
        elif args.year=='2017':
            for i in range(0,len(branches_data_2017)):
                branchList.push_back(branches_data_2017[i])
        elif args.year=='2018':
            for i in range(0,len(branches_data_2018)):
                branchList.push_back(branches_data_2018[i])
    elif args.type=='mc':
        if args.year=='2016':
            for i in range(0,len(branches_mc_2016)):
                branchList.push_back(branches_mc_2016[i])
        elif args.year=='2017':
            for i in range(0,len(branches_mc_2017)):
                branchList.push_back(branches_mc_2017[i])
        elif args.year=='2018':
            for i in range(0,len(branches_mc_2018)):
                branchList.push_back(branches_mc_2018[i])

    return branchList

#ROOT.gInterpreter.Declare('#include "{}"'.format("zcutModule_rdf.h"))
#ROOT.loadfile()
if __name__ == '__main__':
    samples, data_chain, mc_chain = SAMPLE.set_samples(args.year)
    if not os.path.exists(args.input+'/'+args.year+'/'+args.poststep):
        os.mkdir(args.input+'/'+args.year+'/'+args.poststep)
    for i in range(0,len(samples[args.dataset])):
            print '>>>>>>>>>>>>>>>>>>>> chargeflip: skim %s' % samples[args.dataset][i]
            df = ROOT.ROOT.RDataFrame("Events", args.input+args.year+'/'+args.prestep+'/'+samples[args.dataset][i])

            if args.type=='data':
                df1=df.Filter('nlepton==2','nlepton cut') \
                    .Filter('lepton_pt[0]>=23 && lepton_pt[1]>=10','lepton pt cut') \
                    .Filter('abs(lepton_pdg_id[0]*lepton_pdg_id[1])==11*11','ee channel') \
                    .Filter('mll>60 && mll<120','mll cut')\
                    .Filter('HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ','trigger cut')\
                    .Define('lep1_pt','lepton_pt[0]') \
                    .Define('lep1_eta','lepton_eta[0]') \
                    .Define('lep1_pdgId','lepton_pdg_id[0]') \
                    .Define('lep1_tight','lepton_tight[0]') \
                    .Define('lep1_mishits','lepton_mishits[0]') \
                    .Define('lep1_tkIsoId','lepton_tkIsoId[0]') \
                    .Define('lep2_pt','lepton_pt[1]') \
                    .Define('lep2_eta','lepton_eta[1]') \
                    .Define('lep2_pdgId','lepton_pdg_id[1]') \
                    .Define('lep2_tight','lepton_tight[1]') \
                    .Define('lep2_mishits','lepton_mishits[1]') \
                    .Define('lep2_tkIsoId','lepton_tkIsoId[1]')
                df1.Snapshot("Events",args.input+'/'+args.year+'/'+args.poststep+'/'+samples[args.dataset][i],KeepColumns())

            elif args.type=='mc':
                df1=df.Filter('nlepton==2','nlepton cut')\
                    .Filter('lepton_pt[0]>=23 && lepton_pt[1]>=10','lepton pt cut')\
                    .Filter('abs(lepton_pdg_id[0]*lepton_pdg_id[1])==11*11','ee channel')\
                    .Filter('mll>60 && mll<120','mll cut') \
                    .Filter('HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ','trigger cut') \
                    .Define('lep1_pt','lepton_pt[0]') \
                    .Define('lep1_eta','lepton_eta[0]') \
                    .Define('lep1_pdgId','lepton_pdg_id[0]') \
                    .Define('lep1_tight','lepton_tight[0]') \
                    .Define('lep1_mishits','lepton_mishits[0]') \
                    .Define('lep1_tkIsoId','lepton_tkIsoId[0]') \
                    .Define('lep2_pt','lepton_pt[1]') \
                    .Define('lep2_eta','lepton_eta[1]') \
                    .Define('lep2_pdgId','lepton_pdg_id[1]') \
                    .Define('lep2_tight','lepton_tight[1]') \
                    .Define('lep2_mishits','lepton_mishits[1]') \
                    .Define('lep2_tkIsoId','lepton_tkIsoId[1]') \
                    .Define('genmatch2l','lepton_real[0]*lepton_real[1]')
                df1.Snapshot("Events",args.input+'/'+args.year+'/'+args.poststep+'/'+samples[args.dataset][i],KeepColumns())

            allCutsReport = df.Report()
            allCutsReport.Print()
