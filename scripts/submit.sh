#!/bin/bash
### A name for the job - No spaces allowed
#PBS -N final_project
#PBS -l nodes=1:ppn=2
#PBS -l walltime=72:00:00
#PBS -l mem=32gb

# --- Load environment variables from .env file ---
set -a
source /home/project/.env # !!! adjust path if your .env lives elsewhere
set +a

#PBS -o localhost:/home/$CNAME/job.log
#PBS -e localhost:/home/$CNAME/job.err
#PBS -m bae
#PBS -M $CNAME@colgate.edu

cd "$NLP_PATH"
. .venv/bin/activate
sleep 1
python main.py "$CONFIG_PATH"
