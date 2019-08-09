import os

path = '/afs/cern.ch/work/j/jixiao/ssww/CMSSW_10_2_13/src/PhysicsTools/NanoAODTools/crab/'
def create_txt(file_name):
    handle = open(file_name, "r")
    exec (handle)
    _Samples = Samples

    for i in _Samples:
        try:
            print _Samples[i]['nanoAODSIM']
        except:
            continue

if __name__ == '__main__':
    create_txt(path+'dataset_2016_nano_v4_new.py')
    create_txt(path+'dataset_2017_nano_v4_new.py')
    create_txt(path+'dataset_2018_nano_v4_new.py')