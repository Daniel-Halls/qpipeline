               .__                 .__   .__
  ____________  |__|______    ____  |  |  |__|  ____    ____
 / ____/\____ \ |  |\____ \ _/ __ \ |  |  |  | /    \ _/ __ \
< <_|  ||  |_> >|  ||  |_> >\  ___/ |  |__|  ||   |  \\  ___/
 \__   ||   __/ |__||   __/  \___  >|____/|__||___|  / \___  >
    |__||__|        |__|         \/                \/      \/
---------------------------------------------------------------------------

qpipeline is a set of warpper scripts around
qunex/hcp pipelines to make it easier to use.

It consists of the following subcommands:
    - setup (qunex folder HCP set up)

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
