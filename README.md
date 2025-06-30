```
                .__                 .__   .__
  ____________  |__|______    ____  |  |  |__|  ____    ____
 / ____/\____ \ |  |\____ \ _/ __ \ |  |  |  | /    \ _/ __ \
< <_|  ||  |_> >|  ||  |_> >\  ___/ |  |__|  ||   |  \\  ___/
 \__   ||   __/ |__||   __/  \___  >|____/|__||___|  / \___  >
    |__||__|        |__|         \/                \/      \/
```
---------------------------------------------------------------------------

qpipeline is a set of warpper scripts around
qunex/hcp pipelines to make it easier to use.

It consists of the following subcommands:
    - setup (qunex folder HCP set up)
    - strucutral (pre-freesurfer, freesurfer, post-freesurfer)

## Installation
---------------------------------------------------------------------------
At the moment this is very much a work in progress set of pipelines and will be updated a lot.
Therefore to save having to keep installing it is probably best
to install in editable mode.

```
git clone git@github.com:Daniel-Halls/qpipeline.git
cd qpipeline
pip install -e .
```

## Setup
---------------------------------------------------------------------------
This is to set up a qunex folder. The input data must be in bids format.

qpipeline works by importing all the subjects in the raw data folder into a qunex study folder

```
usage: qpipeline setup [-h] [-s STUDY_FOLDER] [-L] [-O] -r RAW_DATA [-d {hcp,biobank}] [-b BATCH]

options:
  -h, --help            show this help message and exit
  -s STUDY_FOLDER, --study_folder STUDY_FOLDER
                        Path to study folder
  -L, --Load_env        Use this option to load qunex enviorment (currently only works on nottingham cluster)
  -O, --overwrite       Overwrite exsiting study folder
  -r RAW_DATA, --raw_data RAW_DATA
                        Path to raw data
  -d {hcp,biobank}, --data_type {hcp,biobank}
                        Which type of data (HCP style or biobank) is being processed. Either HCP or biobank (case insensitive)
  -b BATCH, --batch BATCH
                        Full path to a custom batch file with parameters for the hcp pipeline. Must be called hcp_batch.txt

```

## HCP Structural pipeline
---------------------------
This is to run prefreesurfer, freesurfer and postfreesurfer

```
usage: qpipeline structural [-h] [-s STUDY_FOLDER] [-L] [-q QUEUE] [-F]

options:
  -h, --help            show this help message and exit
  -s STUDY_FOLDER, --study_folder STUDY_FOLDER
                        Path to study folder
  -L, --Load_env        Use this option to load qunex enviorment (currently only works on nottingham cluster)
  -q QUEUE, --queue QUEUE
                        Which queue to submit to. Leave this as none if not running on cluster
  -F, --FLAIR           Is T2 a FLAIR image


```

## HCP Diffusion pipeline
---------------------------
This is to runs the HCP diffusion pipeline

```
usage: qpipeline diffusion [-h] [-s STUDY_FOLDER] [-L] [-q QUEUE] [-N]

options:
  -h, --help            show this help message and exit
  -s STUDY_FOLDER, --study_folder STUDY_FOLDER
                        Path to study folder
  -L, --Load_env        Use this option to load qunex enviorment (currently only works on nottingham cluster)
  -q QUEUE, --queue QUEUE
                        Which queue to submit to. Leave this as none if not running on cluster
  -N, --no_gpu          Don't use eddy GPU

```
