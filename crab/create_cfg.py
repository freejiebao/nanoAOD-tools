import argparse
import os

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-v','--version', help='which version should be', default='4')
group = parser.add_mutually_exclusive_group()  # type: _MutuallyExclusiveGroup
group.add_argument('-y','--year', help='run on which year', choices=('2016','2017','2018'))
group.add_argument('-a','--all', help='chose all jobs',action='store_true', default= False)
args = parser.parse_args()

path = '/pnfs/ihep.ac.cn/data/cms/store/user/jixiao/'
version = '_v%s/' %args.version


def new_py(year):

    if year == '2017':
        b = os.getcwd() + '/cfg2017/'
        file_name = 'dataset_2017_nano_v4_new.py'
        outdir = '/store/user/%s/nano2017' + version
        golden_json = "\'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt\'"
    elif year == '2018':
        b = os.getcwd() + '/cfg2018/'
        file_name = 'dataset_2018_nano_v4_new.py'
        outdir = '/store/user/%s/nano2018' + version
        golden_json = "\'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt\'"
    elif year == '2016':
        b = os.getcwd() + '/cfg2016/'
        file_name = 'dataset_2016_nano_v4_new.py'
        outdir = '/store/user/%s/nano2016' + version
        golden_json = "\'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt\'"
    else:
        return

    handle = open(file_name, "r")
    exec (handle)
    _Samples = Samples

    #site = "T2_CN_Beijing"
    site = "T2_CH_CERNBOX"

    print(">>>>>>>>>>>>>>>>>>>> created directory for %s :" + b) % year
    print(">>>>>>>>>>>>>>>>>>>> the created configuration files:")
    if not os.path.exists(b):
        os.makedirs(b)
    for iSample in _Samples:
        file = iSample + '_cfg.py'
        print(file)
        # str_list={}
        bsh = 'crab_script_%s.sh' % year
        script = 'crab_script_%s.py' % year
        split = 'FileBased'
        unitsPerJob = '20'
        lumiMask = "config.Data.totalUnits = -1"
        for iiSample in _Samples[iSample]:
            # print(iiSample)
            if iiSample == "nanoAOD":
                bsh = 'crab_script_data_%s.sh' % year
                script = 'crab_script_data_%s.py' % year
                split = 'LumiBased'
                unitsPerJob = '100'
                lumiMask = "config.Data.lumiMask = %s" % golden_json
            tmp_str = _Samples[iSample][iiSample]  # dataset
            # str_list.append(iSample)    # sample name
            # str_list.append(script_name)   # crab_data_script.py or crab_script.py
            # str_list.append(lumiMask)    # lumiMask or totalUnits
            # str_list.append(outdir)
            # str_list.append(iSample)
            # str_list.append(site)
            # str_list=(iSample,script,_Samples[iSample][iiSample],split,lumiMask,outdir,iSample,site)
            break  # just need to exec once
        file_content = ""
        file_content += "from WMCore.Configuration import Configuration\n"
        file_content += "from CRABClient.UserUtilities import config, getUsernameFromSiteDB\n"
        file_content += "\n"
        file_content += "config = Configuration()\n"
        file_content += "\n"
        file_content += "config.section_(\"General\")\nconfig.General.requestName = \'%s\'\n" % (iSample + '_' + year)
        file_content += "config.General.transferLogs= False\n"
        file_content += "config.section_(\"JobType\")\n"
        file_content += "config.JobType.pluginName = \'Analysis\'\n"
        file_content += "config.JobType.psetName = \'PSet.py\'\n"
        file_content += "config.JobType.scriptExe = \'%s\'\n" % bsh
        file_content += "config.JobType.inputFiles = [\'%s\',\'%s/src/PhysicsTools/NanoAODTools/scripts/haddnano.py\',\'%s/src/PhysicsTools/NanoAODTools/interface/\',\'%s/src/PhysicsTools/NanoAODTools/src/\'] #hadd nano will not be needed once nano tools are in cmssw\n" % (script, os.environ['CMSSW_BASE'], os.environ['CMSSW_BASE'], os.environ['CMSSW_BASE'])
        file_content += "config.JobType.sendPythonFolder  = True\n"
        file_content += "config.section_(\"Data\")\nconfig.Data.inputDataset = \'%s\'\n" % _Samples[iSample][iiSample]
        file_content += "#config.Data.inputDBS = \'phys03\'\n"
        file_content += "config.Data.inputDBS = \'global\'\n"
        file_content += "config.Data.splitting = \'%s\'\n" % split
        file_content += "#config.Data.splitting = \'EventAwareLumiBased\'\n"
        file_content += "config.Data.unitsPerJob = %s\n" % unitsPerJob
        file_content += "%s\n" % lumiMask
        file_content += "\n"
        file_content += "config.Data.outLFNDirBase =\'%s\'" % outdir
        file_content += " % (getUsernameFromSiteDB())\n"
        file_content += "config.Data.publication = False\n"
        file_content += "config.Data.outputDatasetTag = \'%s\'\n" % (iSample + '_' + year)
        file_content += "config.section_(\"Site\")\n"
        file_content += "config.Site.storageSite = \"%s\"\n" % site
        file_content += "\n"

        tmp = open(b + str(file), "w")
        tmp.write(file_content)


if __name__ == '__main__':
    if args.all:
        new_py('2016')
        new_py('2017')
        new_py('2018')
    else:
        new_py(args.year)
