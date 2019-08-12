#!/bin/bash

echo "Analyzing the files"
cd ~/data_analysis/data_to_analyze
file2=""
path_report=~/data_analysis/report_autoSaint
for file in ./*
	do
		out="$(rms_pipeline ${file:2})"
		echo $out > id.txt
		rms_autoSaint $(cat id.txt) &> $path_report/$file.txt
		echo "FILE: "${file:2}" - ID: "$out >> files_processed.txt
	done

function create_report_arr(){
	cd ~/data_analysis/report_arr
	python3.6 ../report_arr.py
	cd ~/data_analysis
}

#TODO make the autoSain
#Continue with this
