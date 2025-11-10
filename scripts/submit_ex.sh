#!/bin/bash
### A name for the job - No spaces allowed
PBS -N final_project
### Specify how many nodes and how many processors
PBS -l nodes=1:ppn=2
### Specify the maximum time allowed for the job to run in each node
PBS -l walltime=72:00:00
### Specify Memory Limit
PBS -l mem=32gb
### Specify a file for the console output - if any # create dir  ~/proj
PBS -o localhost:/home/$CNAME/job.log
### Specify a file for the console error output - if any  # create dir  ~/proj
PBS -e localhost:/home/$CNAME/job.err 
### Receive an email when the job begins execution (b), when it ends (e), and when it encounters an error (a)
PBS -m bae
### Specify an email for pds@colgate.edu to send notifications
PBS -M $CNAME@colgate.edu
### Start job from the directory it was submitted.
cd $NLP_PATH
### Do you need a virtual environment?
. .venv/bin/activate && sleep 1
### Run your script with relative or absolute path - consider having the python and pbs scripts in the same directory (~/NLP).
python main.py $CONFIG_PATH

run qsub final_project