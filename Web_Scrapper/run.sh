#!/bin/bash
clear
if [ -f "output.csv" ]
then
    rm 'output.csv'
fi

#if [ -f "sample" ]
#then
#    rm 'sample'
#fi


scrapy crawl thelearningpoint -o output.csv 
