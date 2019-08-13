#!/bin/bash
echo "Analyzing the files"
mainfolder=$1
cd $mainfolder/data_to_analyze
path_report=$mainfolder/report_autoSaint
for file in ./*
	do
		echo "Analizing file" ${file:2}
		out="$(rms_pipeline ${file:2})"
		echo $out > id.txt
		rms_autoSaint $(cat id.txt) &> $path_report/$file.txt
		echo "FILE: "${file:2}" - ID: "$out >> $mainfolder/files_processed.txt
	done
echo "DONE"
