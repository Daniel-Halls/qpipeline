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


## Setup
---------------------------------------------------------------------------
This is to set up a qunex folder. The input data must be in bids format.
```
usage: qpipeline setup [-h] -s STUDY_FOLDER -r RAW_DATA -i ID

options:
  -h, --help            show this help message and exit
  -s STUDY_FOLDER, --study_folder STUDY_FOLDER
                        Path to study folder
  -r RAW_DATA, --raw_data RAW_DATA
                        Path to raw data
  -i ID, --id ID        Subject ID
```

## HCP Structural pipeline
---------------------------
This is to run prefreesurfer, freesurfer and postfreesurfer

```
usage: qpipeline structural [-h] -s STUDY_FOLDER [-F] -i ID [-q QUEUE]

options:
  -h, --help            show this help message and exit
  -s STUDY_FOLDER, --study_folder STUDY_FOLDER
                        Path to study folder
  -F, --FLAIR           Is T2 a FLAIR image
  -i ID, --id ID        Subject ID
  -q QUEUE, --queue QUEUE
                        Which queue to submit to. Leave this as none if not running on cluster

```