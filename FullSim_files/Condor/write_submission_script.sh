#!/bin/bash

# Write the HTCondor submission script for sample generation

work_space=$1
gen_frag_path=$2
lhe_file_path=$3
model_name=$4
n_events=$5
seed=$6
submission_dir=$7

echo "# HTCondor submission script
Universe   = vanilla
cmd        = $submission_dir/runFullSim_condor.sh
args       = $work_space $gen_frag_path $lhe_file_path $model_name $n_events $seed
Log        = $work_space/logs/condor_job_${seed}.log
Output     = $work_space/logs/condor_job_${seed}.out
Error      = $work_space/logs/condor_job_${seed}.error
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT_OR_EVICT
" > $work_space/submission_scripts/condor_submission_${seed}.job

if [[ "$HOSTNAME" == "soolin"* ]]; then          
    echo "use_x509userproxy = true" >> $work_space/run_scripts/condor_submission_${seed}.job
fi

echo "# Resource requests (disk storage in kB, memory in MB)
request_cpus = 1
request_disk = 1000000
request_memory = 2500
+MaxRuntime = 14400
# Number of instances of job to run
queue 1
" >> $work_space/submission_scripts/condor_submission_${seed}.job

chmod +x $work_space/submission_scripts/condor_submission_${seed}.job