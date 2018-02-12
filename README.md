# Semi-visible Jets

[![arXiv](https://img.shields.io/badge/arXiv-1707.05326%20-green.svg)](https://arxiv.org/abs/1707.05326)

This repository contains model files necessary for generation of semi-visible jet Monte Carlo signal events in `MadGraph`. 
Please see [1707.05326](https://arxiv.org/abs/1707.05326) and [1503.00009](https://arxiv.org/abs/1503.00009) for
for further details. Please note that a recent version of `PYTHIA` (> 8.226) including the Hidden Valley module 
and running of the dark coupling is required when implementing the subsequent dark hadronization.

UFO files associated with two UV completions are provided:

## s-channel production

An s-channel production (`DMsimp_s_spin1`) mediated through a new heavy Z'. The model provided is a modified version of the spin-1 `DMsimp` model (http://feynrules.irmp.ucl.ac.be/wiki/DMsimp) 
implemented through `FeynRules`.

## t-channel production

A t-channel production (`DMsimp_tchannel`) where the dark and visible sectors interact through a new scalar bi-fundamental.

The bi-fundamentals are denoted with `su11, su12, su21, su22...`, where `u` etc explicitly specifies the QCD flavour index 
and the numbers are the explicit dark non-Abelian group indices. Similarly, the dark quarks are labeled as `qv11, qv12, qv21, qv22`.

Please note that a modified version of `MadGraph` using the patch included [here](https://bugs.launchpad.net/mg5amcnlo/+bug/1702712) 
is required to ensure a stable cross section for event generation using this model.

A `FeynRules` model file (`DMsimp_tchannel.fr`) as well as the `Mathematica` notebook (`DMsimp_tchannel.nb`) used to generated the UFO output 
are also provided.

## LHE production with `MadGraph` (interactive)

Make a directory to store the programs and output. Then, clone the semi-visible jets files required with

```bash
git clone git@github.com:eshwen/SemivisibleJets.git
```

Download a recent release of `MadGraph` with

```bash
wget https://launchpad.net/mg5amcnlo/2.0/2.6.x/+download/MG5_aMC_v2.6.1.tar.gz
```

Unzip the tar ball with

```bash
tar -xvzf MG5_aMC_v2.6.1.tar.gz
```

In the folder created, the run command is `./bin/mg5_aMC`. Copy the model files from `SemivisibleJets/` into `models/` with

```bash
cp -r ../SemivisibleJets/MG_models/DMsimp_* ./models/
```

The input/config files for the s- and t-channel processes are specified in `SemivisibleJets/MG_input/`. In these files, the number of events, output directory, as well as other parameters, can be changed.

Run one of the configs with

```bash
./bin/mg5_aMC ../SemivisibleJets/MG_input/<file>
```

This will create lots of output files in the directory specified by the config. The LHE file will be zipped in `<Output dir>/Events/run_01/`, which you can unzip with

```bash
gunzip <file>
```

Other information like the cross section and Feynman diagrams can also be viewed.

_N.B._: MadGraph can be a bit erratic and sometimes fail at the "Working on SubProcesses" stage. Just delete the output directory and try again.

## Generating `MadGraph` gridpacks

For central production, gridpacks will be needed as external LHE generators don't cooperate with CMSSW. These gridpacks are made on the grid, with monitoring output such that it looks like you're running locally.

First, clone this repo with

```bash
git clone git@github.com:eshwen/SemivisibleJets.git
```

All the necessary files for spin1-s- and t-channel production are in `MG_gridpack_files/`, and a tutorial can be found at https://twiki.cern.ch/twiki/bin/view/CMS/QuickGuideMadGraph5aMCatNLO. More models can be added if needed, but it is cumbersome. The file  names need to be specific, with the same prefix of `<model name>` and have the suffixes as shown in the existing models (e.g., `<model name>_proc_card.dat`). If adding models, use the existing files as templates. The model files also need to be zipped with

```bash
tar -cf <output file name>.tar <input file(s)>
```

and be copied to the generator web repository on `/afs/cern.ch/cms/generators/www/`. Note that you will need to contact Cms.Computing@cern.ch and cms.generators@cern.ch to request write access to the directory.

Once the models are in place and the input cards have been written, clone the `genproductions` repo somewhere with a lot of storage. The gridpacks end up in directories within the repository, and so its size can grow considerably. Clone my fork of the repo (which includes some minor fixes for bugs I was receiving) with

```bash
git clone git@github.com:eshwen/genproductions.git genproductions -b mg26x
```

The branch specified above is necessary to run MadGraph versions 2.6.x, with some slight bug fixes present in the fork.

Validate the input cards you have with

```bash
cd genproductions/bin/MadGraph5_aMCatNLO/Utilities/parsing_code
python parsing.py <path to process card directory/name of process card without _proc_card.dat>
```

Once validated, run the gridpack generation with

```bash
cd genproductions/bin/MadGraph5_aMCatNLO/
./gridpack_generation.sh <name of process card without _proc_card.dat> <relative path to cards directory> <queue selection>
```

where `<queue selection>` options can be found by typing `bqueues`. If instead, you would like to run on Condor (either at lxplus or at a T2/T3 site), run

```bash
cd genproductions/bin/MadGraph5_aMCatNLO/
./submit_condor_gridpack_generation.sh <name of process card without _proc_card.dat> <relative path to cards directory> 
```

Note that the architecture, and CMSSW and MadGraph versions are all hardcoded into `gridpack_generation.sh`. They be changed either from within, or with command-line arguments (which only work for arch and CMSSW versions). As with interactive running, MadGraph can be unruly on the "Working on Subprocesses" bit. Just resubmit if that's the case.

Your grid certificate may also be required to run. To initialise a proxy that lasts a week, type

```bash
voms-proxy-init --voms cms --valid 168:00
```

Once completed, the gridpack (in a .tar.xz file) will be located in the current directory. An untarred version is also available for viewing and validation. Just repeat the procedure for other parameters and models.

## Hadronization with `PYTHIA` and detector simulation with `Delphes` (UNNEEDED???)

As noted above, a recent version of `PYTHIA` (> 8.226) including the Hidden Valley (HV) module and running of the dark coupling is required when implementing the subsequent dark hadronization.

In order to be able to use the HV module, the PDG IDs of the dark particles must be changed in the LHE files for `PYTHIA` to be able to recognize and shower these properly. This can be done as follows:

- For the s-channel model
```bash
sed -i 's/5000521/4900101/g' <LHE filename>
```
- For the t-channel model
```bash
sed -i 's/49001010/4900101/g' <LHE filename>	
sed -i 's/49001011/4900101/g' <LHE filename>	
sed -i 's/49001012/4900101/g' <LHE filename>	
sed -i 's/49001013/4900101/g' <LHE filename>	
sed -i 's/49001014/4900101/g' <LHE filename>	
```
or
```bash
./tChannelPIDChange.sh <LHE filename>
```

from this directory. Once the PIDs have been changed, it is possible to run `PYTHIA` and `Delphes` concurrently on the LHE file. See the README in https://github.com/eshwen/mc-production/tree/master/run_delphes for the installation commands and how to run everything. On subsequent sessions, you can just `source delphes_pythia8_setup.sh` in that directory to set up the environment.

## Contact

For questions or issues please contact:

-  Tim Lou; hlou@berkeley.edu
-  Siddharth Mishra-Sharma; smsharma@princeton.edu
-  Eshwen Bhal (for implementation, not theory); eshwen.bhal@cern.ch

## To do

- See if `sed` commands are still needed in gridpacks before they're tarred and processed. If so, find a way to incorporate them.
- Make sure commands and code are robust and validate output