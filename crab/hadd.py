import os
import shutil
import argparse

from argparse import _MutuallyExclusiveGroup

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-t','--transfer', help='transfer to some site by scp, defalut is False', action='store_true', default=False)
parser.add_argument('-s','--sever', help='transfer to the sever', default='xiaoj@hepfarm02.phy.pku.edu.cn')
parser.add_argument('-o','--output', help='output path', default='/eos/user/l/llinwei/jie/ssww_ntuple/')
group = parser.add_mutually_exclusive_group()  # type: _MutuallyExclusiveGroup
# group.add_argument('-s', '--sample', help='give explicit sample names', nargs='*')
group.add_argument('-y', '--year', help='chose all jobs in this year', choices=('2016', '2017', '2018'))
group.add_argument('-a', '--all', help='chose all jobs', action='store_true', default=False)
args = parser.parse_args()

server = args.sever


def get_FileSize(filePath):
    # filePath = unicode(filePath,'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)


def submit(year):
    # destiny = '/home/pku/xiaoj/ssww_ntuple/'+year
    destiny = args.output+year
    file_name = 'crab_collection%s.py' % year

    if not os.path.exists('hadd_collection' + year + '.py'):
        collect = open('hadd_collection' + year + '.py', "a+")
        collect.write('Hadd = {} \n')
        collect.close()
    else:
        pass

    handle = open(file_name, "r")
    exec (handle)
    _Success = Success

    for iSample in _Success:
        with open('hadd_collection' + year + '.py', 'a+') as collect:
            exec(collect)
            _Hadd = Hadd

        try:
            _Hadd[iSample]
        except KeyError:
            hadd_all = 'haddnano.py ' + iSample + '.root '
            for iiSample in _Success[iSample]:
                tmp_str = _Success[iSample][iiSample]  # dataset
                hadd_all += tmp_str + '*.root '
            os.system(hadd_all)
            size = get_FileSize(iSample + '.root')
            if args.transfer:
                os.system('ssh ' + server + ' mkdir -p ' + destiny)
                os.system('scp ' + iSample + '.root ' + server + ':' + destiny)
                os.remove(iSample + '.root')
            else:
                os.system('mv ' + iSample + '.root '+destiny)
            new = 'Hadd[\'' + iSample + '\'] = ' + str(size) + '\n'
            with open('hadd_collection' + year + '.py', 'a+') as collect:
                collect.write(new)
            # print hadd_all
            print '>>>>>>>>>>>>>>>>>>>> successfully hadd ', iSample
        else:
            pass


if __name__ == '__main__':
    if args.all:
        submit('2016')
        submit('2017')
        submit('2018')
    else:
        submit(args.year)

