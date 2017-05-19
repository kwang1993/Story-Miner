#!/bin/bash
#$ -l h_data=8G,h_rt=4:00:00
#$ -o $HOME/job_output.txt
#$ -e $HOME/job_errors.txt
#$ -t 1-50:1

. /u/local/Modules/default/init/modules.sh

#dataset="Vaccination/mothering_chunks_sent_sep_clean"

projectDataDir="/u/home/v/vahabpou/behnam/output"
projectDir="$HOME/relation_extraction"
outdir="$HOME/relation_extraction/data/Twitter_output"

inputFile1="$projectDataDir/sents_$((4*${SGE_TASK_ID}-3)).txt"
inputFile2="$projectDataDir/sents_$((4*${SGE_TASK_ID}-2)).txt"
inputFile3="$projectDataDir/sents_$((4*${SGE_TASK_ID}-1)).txt"
inputFile4="$projectDataDir/sents_$((4*${SGE_TASK_ID})).txt"

outputFile="$outdir/"

module load python/2.7
python $projectDir/Story-Miner/final_version_relex/relEx_parse_tree.py $inputFile1 $outputFile 
python $projectDir/Story-Miner/final_version_relex/relEx_parse_tree.py $inputFile2 $outputFile 
python $projectDir/Story-Miner/final_version_relex/relEx_parse_tree.py $inputFile3 $outputFile
python $projectDir/Story-Miner/final_version_relex/relEx_parse_tree.py $inputFile4 $outputFile

echo "Tasks $((4*${SGE_TASK_ID}-3))-$((4*${SGE_TASK_ID})) finished."

