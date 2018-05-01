#!/usr/bin/env python2
import argparse
import os
from subprocess import call

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--work_space", type = str, default = os.getcwd(), help = "Work space containing CMSSW releases, input and output files")
parser.add_argument("-m", "--model_name", type = str, default = "testModel", help = "Identifying name of model")
args = parser.parse_args()

def main():
    """
    Write bash script to hadd output nanoAOD files
    """

    work_space = args.work_space
    model_name = args.model_name

    filePath = os.path.join(work_space, "combineOutput_{0}.sh".format(model_name))
    writeFile = open(filePath, "w")

    # Write bash combine script
    writeFile.write("""#!/bin/bash
echo "Warning: May take a while to hadd if many files are present"
source /cvmfs/cms.cern.ch/cmsset_default.sh 
cd {0}/CMSSW_9_4_4/src
cmsenv
cd {0}
{1}/Utils/haddnano.py {0}/output/{1}_nanoAOD_final.root {0}/output/{1}*NANOAOD*.root
mkdir {0}/output/components
mv {0}/output/{1}*NANOAOD*.root {0}/output/components
    """.format(work_space, model_name)
    )
    writeFile.close()

    call("chmod +x {0}".format(filePath), shell = True)
    print "Hadding script written!"


if __name__ == '__main__':
    main()

