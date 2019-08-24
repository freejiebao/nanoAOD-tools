import os
import shutil
import argparse
from argparse import _MutuallyExclusiveGroup

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-r','--resubmit', help='resubmit after killing jobs, default just kill',action='store_true', default= False)
group = parser.add_mutually_exclusive_group()  # type: _MutuallyExclusiveGroup
group.add_argument('-s','--sample', help='give explicit sample names',nargs='*')
group.add_argument('-y','--year', help='chose all jobs in this year', choices=('2016','2017','2018'))
group.add_argument('-a','--all', help='chose all jobs',action='store_true', default= False)

args = parser.parse_args()


def kill_sample(_sample):
    for i in range(0,len(_sample)):
        if os.path.exists(_sample[i]):
            os.system('crab kill -d ' + _sample[i])
            shutil.rmtree(_sample[i])
        if args.resubmit:
            if '2016' in _sample[i]:
                os.system('crab submit -c ./cfg2016/'+_sample[i][5:len(_sample[i])-5]+'_cfg.py')
            elif '2017' in _sample[i]:
                os.system('crab submit -c ./cfg2017/'+_sample[i][5:len(_sample[i])-5]+'_cfg.py')
            elif '2018' in _sample[i]:
                os.system('crab submit -c ./cfg2018/'+_sample[i][5:len(_sample[i])-5]+'_cfg.py')
            else:
                pass

def kill_year(_year):
    b = ''
    file_name = ''
    if _year=='2017':
        b = os.getcwd() + '/cfg2017/'
        file_name='dataset_2017_nano_v5_new.py'
    elif _year=='2018':
        b = os.getcwd() + '/cfg2018/'
        file_name='dataset_2018_nano_v5_new.py'
    elif _year=='2016':
        b = os.getcwd() + '/cfg2016/'
        file_name='dataset_2016_nano_v5_new.py'

    handle=open(file_name,"r")
    exec(handle)
    _Samples = Samples

    for iSample in _Samples :
        if os.path.exists('crab_'+iSample+'_'+_year):
            os.system('crab kill -d crab_'+iSample+'_'+_year)
            shutil.rmtree('crab_'+iSample+'_'+_year)
        if args.resubmit:
            os.system('crab submit -c '+b+iSample+'_cfg.py')


def kill_all(_all):

    _year = ['2016','2017','2018']

    for i in range(0,len(_year)):
        b = os.getcwd() + '/cfg%s/' %_year[i]
        file_name='dataset_%s_nano_v5_new.py' %_year[i]

        handle=open(file_name,"r")
        exec(handle)
        _Samples = Samples

        for iSample in _Samples :
            if os.path.exists('crab_'+iSample+'_'+_year[i]):
                os.system('crab kill -d crab_'+iSample+'_'+_year[i])
                shutil.rmtree('crab_'+iSample+'_'+_year[i])
            if args.resubmit:
                os.system('crab submit -c '+b+iSample+'_cfg.py')


if __name__ == '__main__':
    '''
    print args.resubmit
    print args.sample
    print args.year
    print args.all
    '''
    if not (args.sample == None):
        print '>>>>>>>>>>>>>>>>>>>> sample'
        kill_sample(args.sample)
    elif not (args.year == None):
        print '>>>>>>>>>>>>>>>>>>>> year'
        kill_year(args.year)
    elif args.all:
        print '>>>>>>>>>>>>>>>>>>>> all'
        kill_all(args.all)
    else:
        pass
