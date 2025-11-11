#!/bin/bash
### A name for the job - No spaces allowed
#PBS -N final_project
#PBS -l nodes=1:ppn=2:gpus=1
#PBS -l walltime=72:00:00
#PBS -l mem=32gb

# --- Load environment variables from .env file ---

#PBS -o localhost:/home/<colgate user id>/job.log
#PBS -e localhost:/home/<colgate user id>/job.err
#PBS -m bae
#PBS -M <your_cname>@colgate.edu

cd <your/NLPScholar/path>
. .venv/bin/activate
sleep 1
python main.py <your/config/path>
