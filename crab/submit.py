import os
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
group = parser.add_mutually_exclusive_group()  # type: _MutuallyExclusiveGroup
group.add_argument('-y','--year', help='run on which year', choices=('2016','2017','2018'))
group.add_argument('-a','--all', help='chose all jobs',action='store_true', default= False)

args = parser.parse_args()


def submit(_year):
    b = './cfg%s/' %_year
    file_name='dataset_%s_nano_v5_new.py' %_year
    handle=open(file_name,"r")
    exec(handle)
    _Samples = Samples

    for iSample in _Samples :
        file=iSample+'_cfg.py'
        os.system('crab submit -c '+b+file)
        #print('crab submit -c '+b+file)

if __name__ == '__main__':
    if args.all:
        submit('2016')
        submit('2017')
        submit('2018')
    else:
        submit(args.year)
