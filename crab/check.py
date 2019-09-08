import os
import re
import shutil
import argparse
import ROOT

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-y','--year', help='run over which year', dest='chosenyear', default = '2022', choices=('2016','2017','2018','2022'))
parser.add_argument('-d','--checkdir', help='check files in which directory', default='/home/cmsdas/testuser01/jie/ssww_ntuple/')
args = parser.parse_args()

def status(year):
    file_name = 'crab_collection%s.py' % year

    handle = open(file_name, "r")
    exec (handle)
    _Success = Success

    files= os.listdir(args.checkdir+year)
    notin=[]
    for iSuccess in _Success:
        if iSuccess+'.root' in files:
            fin=ROOT.TFile(iSuccess+'.root')
            print '===================== is ', iSuccess, 'IsZombie: ', fin.IsZombie()
            fin.Close()
        else:
            notin.append(iSuccess)
    if len(notin)>0:
        print '<<<<<<<<<<<<<<<<<<<< list of not in files:'
    else:
        print '>>>>>>>>>>>>>>>>>>>> COMPLETED: all files done!'
    for i in range(0,len(notin)):
        print notin[i]
if __name__ == '__main__':
    if args.chosenyear == '2022':
        status('2016')
        status('2017')
        status('2018')
    else:
        status(args.chosenyear)