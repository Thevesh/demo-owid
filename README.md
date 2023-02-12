# demo-owid
Fully working example of an 'end-to-end' open data pipeline, which (in this conditional sequence):
- ingests publicly available daily-updated data from the Malaysian Ministry of Health, then
- checks if the data has been updated, then
- transforms the data in multiple ways to produce 3 different analyses, then
- summarises the analysis with clear and appropriate dataviz, then
- sends the dataviz to the end-user via a bot in a Telegram group.

The entire pipeline is modularised, with errors handled and communicated to the same Telegram group so that the developer can monitor and intervene if required. Furthermore, the structure of the files lends itself to modular testing - the `cron.py` file stitches everything together, but each `cron_` file can be tested in isolation to ensure that the various steps in the pipeline are working as intended.

This exact repository has been deployed on a Ubuntu 22.04 LTS server; to view the output, please message Thevesh on Telegram @ Thevesh and ask to be added to the group where output and status messages are sent.

## Installation
```
cd <local_dev_folder>
git clone https://github.com/Thevesh/demo-owid.git

cd <local_venv_folder>
python -m venv demo-owid
source demo-owid/bin/activate # this should work on a Unix-based system; amend accordingly for your OS

cd <local_dev_folder>/demo-owid
pip3 install -r requirements.txt 
```

And you're set!

## Deployment
I have two shell scripts. The first is `demo-owid.sh`:
```
#!/bin/bash
# activate Python venv and run daily script
source <local_venv_folder>/demo-owid/bin/activate
cd <local_dev_folder>/demo-owid
python3 cron.py
```
The second is `demo-owid-restart.sh`:
```
#!/bin/bash
# activate Python venv and run daily script
source <local_venv_folder>/demo-owid/bin/activate
cd <local_dev_folder>/demo-owid
python3 cron_restart.py
```
In the Linux Crontab on my server, these are deployed as follows:
```
0,5,10 0 * * * ~/demo-owid-restart.sh
0,30 4-10 * * * ~/demo-owid.sh
```
Together, these ensure that the cron is triggered daily. Note that the times are in `GMT+08:00`, you may amend them based on your specific timezone. The times I chose were derived by studying the daily update time of the [source data](https://github.com/MoH-Malaysia/data-darah-public).
