import argparse
import sys
try:
    from checkConfig import performBasicChecks
except ImportError:
    sys.exit('Please source the setup script first.')
from colorama import Fore, init
import glob
from loadYamlConfig import loadYamlConfig
import os
import random
import re
import shutil
from splitLHE import splitLHE
from subprocess import call
import yaml


# Reset text colours after colourful print statements
init(autoreset=True)

parser = argparse.ArgumentParser()
parser.add_argument("config", type=str, help="Path to YAML config to parse")
args = parser.parse_args()



def main():
    """
    Handle the input and parsing from a YAML config file. Run gridpack to retrieve LHE file, then split it and move output to directory specified by user.
    """

    # Load YAML config into a dictionary and assign values to variables for cleanliness
    input_params = loadYamlConfig(args.config)

    model_name = input_params['model_name']
    total_events = input_params['total_events']
    n_jobs = input_params['n_jobs']
    split_lhe_file_path = input_params['lhe_file_path']

    # Check arguments in config file
    performBasicChecks(input_params)

    # Set up some path variables for use later
    svj_top_dir = os.environ['SVJ_TOP_DIR']
    genprod_dir = os.environ['MG_GENPROD_DIR']
    default_gridpack_dir = os.path.join(genprod_dir, model_name)
    lhe_gen_dir = os.path.join(default_gridpack_dir, model_name+'_gridpack', 'work', 'gridpack')

    # Get cross section from gridpack generation log file
    log_file = open(os.path.join(lhe_gen_dir, 'gridpack_generation.log'), 'r')
    log_str = log_file.read()
    x_sec = re.search("(?<=Cross-section :   )(\d*.\d+)", log_str).group(0)
    log_file.close()

    # Append cross section to config file if not included already
    read_config_file = open(args.config, 'r')
    config_orig_str = read_config_file.read()
    read_config_file.close()
    if str(x_sec) in config_orig_str:
        print "No need to append config file with new cross section!"
    else:
        print Fore.CYAN + "Appending config file with cross section as calculated by MadGraph..."
        appended_cfg = open(args.config, 'r+')
        original_str = appended_cfg.readlines()
        appended_cfg.seek(0)
        appended_cfg.truncate()

        for i in xrange( len(original_str) ):
            if 'x_sec' in original_str[i]:
                continue
            else:
                appended_cfg.write(original_str[i])

        appended_cfg.write("x_sec: {0}\n".format(x_sec))
        appended_cfg.close()


    # Copy gridpack tarball to gridpacks/
    for tarball in glob.glob( os.path.join(genprod_dir, model_name+'*.xz') ):
        print Fore.CYAN + "Copying {0} to gridpacks/".format( os.path.basename(tarball) )
        shutil.copyfile( tarball, os.path.join(svj_top_dir, 'gridpacks', os.path.basename(tarball)) )
        os.remove(tarball)
        

    # Run the script produced with the gridpack to get the LHE file out and copy to gridpacks/ dir
    random_seed = random.randint(0, 1000000)
    call("cd {0}; ./runcmsgrid.sh {1} {2}".format(lhe_gen_dir, total_events, random_seed), shell = True)

    lhe_output_path = os.path.join(svj_top_dir, 'gridpacks', model_name+'_LHE.lhe')
    shutil.copyfile( os.path.join(lhe_gen_dir, 'cmsgrid_final.lhe'), lhe_output_path )

    # Delete untarred gridpack as it takes up unnecessary space
    shutil.rmtree(default_gridpack_dir)
    print Fore.MAGENTA + "Removed untarred version of gridpack!"


    # Split the LHE file, the output files being stored in the current directory
    print Fore.CYAN + "Splitting LHE file..."
    splitLHE(inputFile=lhe_output_path, outFileNameBase=model_name+'_split', numFiles=n_jobs)
    os.remove(lhe_output_path)

    # Copy the split LHE files to directory specified by user
    if not os.path.exists(split_lhe_file_path):
        os.mkdir(split_lhe_file_path)
    for splitFile in glob.glob( os.path.join(os.getcwd(), model_name+'_split*.lhe') ):
        shutil.copy(splitFile, split_lhe_file_path)
        os.remove(splitFile)
    print Fore.MAGENTA + "Split LHE files copied to", Fore.MAGENTA + split_lhe_file_path

    print "In case you forgot, your config file is", os.path.abspath(args.config)



if __name__ == '__main__':
    main()

