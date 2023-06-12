#!/bin/bash

s_flag=false

if [ ! -d "SupremeCourtCases" ]; then
    mkdir SupremeCourtCases
fi

while getopts 'sc' OPTIONS; do
    case "$OPTIONS" in
        s) s_flag=true ;;
        c)
            echo "Cleaning Supreme Court Cases"
            rm -rf SupremeCourtCases
            ;;
        *) error "Unexpected option ${OPTIONS}" ;;
    esac
done

if $s_flag; then
    echo "Scraping Supreme Court Cases"
    cd WebScraper
    python -u FindLawScraper.py > FindLawScraper.log
    cd ..
fi
