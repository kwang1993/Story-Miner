#!/bin/bash
#$ -l h_data=4G,h_rt=11:00:00
#$ -o $HOME/job_output.txt
#$ -e $HOME/job_errors.txt
#$ -t 1-50:1
. /u/local/Modules/default/init/modules.sh

dataset="Mothering_Complete"

projectDataDir="$SCRATCH/RelEx"
projectDir="$HOME/RelEx"
outdir="$projectDir/output"
inputFile1="$projectDataDir/$dataset/sents_$((4*${SGE_TASK_ID}-3)).txt"
inputFile2="$projectDataDir/$dataset/sents_$((4*${SGE_TASK_ID}-2)).txt"
inputFile3="$projectDataDir/$dataset/sents_$((4*${SGE_TASK_ID}-1)).txt"
inputFile4="$projectDataDir/$dataset/sents_$((4*${SGE_TASK_ID})).txt"
outputFile1="$outdir/${dataset}/rels_$((4*${SGE_TASK_ID}-3)).txt"
outputFile2="$outdir/${dataset}/rels_$((4*${SGE_TASK_ID}-2)).txt"
outputFile3="$outdir/${dataset}/rels_$((4*${SGE_TASK_ID}-1)).txt"
outputFile4="$outdir/${dataset}/rels_$((4*${SGE_TASK_ID})).txt"

module load python/2.7
nohup python $projectDir/code/relEx.py $inputFile1 $outFile1 &
nohup python $projectDir/code/relEx.py $inputFile2 $outFile2 &
nohup python $projectDir/code/relEx.py $inputFile3 $outFile3 & 
nohup python $projectDir/code/relEx.py $inputFile4 $outFile4 & 

echo "Tasks $((4*${SGE_TASK_ID}-3))-$((4*${SGE_TASK_ID})) started."

