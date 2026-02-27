# EXAMPLE OF RUNNING PCM

INTEL PCM: https://github.com/intel/pcm

Follow the instructions for how to build, ensure you have a "~/pcm/build/bin" folder and it has the pcm executable

Run the following cmd:
```console
# format: pcm_exec sampling_freq -i=num_of_samples -log=log_file_csv
foo@bar:sudo ~/pcm/build/bin/pcm 1 -i=10 -csv=test.csv
```

The shells scripts in the following directories are to be used to generate data.
``` console
# Directories for the DDR4 and DDR5 rig, copy scripts to be launched in CWD
foo@bar: cp ./DDR4_PAMPAR_SCRIPTS/*.sh ./
foo@bar: cp ./DDR5_PAMPAR_SCRIPTS/*.sh ./
# To launch the master file
foo@bar: ./master_PAMPAR_DDR4.sh
foo@bar: ./master_DROOP_PAMPAR_DRR4.sh
foo@bar: ./master_PAMPAR_DDR5.sh
foo@bar: ./master_DROOP_PAMPAR_DDR5.sh
# NOTE: please run the $just_droop$ shell script with V being 23 (19) for the DDR5 (DDR4)
# The current workloads will need to be adjusted as they are more sensitives for V DROOPs
# PAMPAR workloads: gl, sh, mm
```

All relative shell scripts must be executed locally in order to be properly executed

# TODO
Completed? | Task
- [ ] Adjust automation so we just run one bash shell script
- [ ] Ensure input into just droop, update all files
