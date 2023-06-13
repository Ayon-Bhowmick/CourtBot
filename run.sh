#!/bin/bash

s_flag=false
e_flag=false
d_flag=false

if [ ! -d "SupremeCourtCases" ]; then
    mkdir SupremeCourtCases
fi

while getopts 'sec:' OPTIONS; do
    case "$OPTIONS" in
        s) s_flag=true ;;
        c)
            if [ $OPTARG == "cases" ]; then
                echo "removing cases"
                rm -rf SupremeCourtCases
            elif [ $OPTARG == "db" ]; then
                echo "removing embeddings"
                rm -rf VectorDB/.chroma
            else
                error "Unexpected option ${OPTIONS}"
            fi
            ;;
        e) e_flag=true ;;
        d) d_flag=true ;;
        *) error "Unexpected option ${OPTIONS}" ;;
    esac
done

if $s_flag; then
    echo "Scraping Supreme Court Cases"
    cd WebScraper
    python -u FindLawScraper.py > FindLawScraper.log
    cd ..
fi

if $e_flag; then
    echo "Embedding cases"
    cd VectorDB
    python -u embed.py > embed.log
fi

if $d_flag; then
    echo "Starting database"
    cd VectorDB
    uvicorn api:api --reload
    cd ..
fi
