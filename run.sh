#!/bin/bash

s_flag=false
e_flag=false
d_flag=false


if [ ! -d "SupremeCourtCases" ]; then
    mkdir SupremeCourtCases
fi

function help() {
    echo "$(basename $0)"
    echo "  [-s : scrape the supreme court cases]"
    echo "  [-e : embed court decisions]"
    echo "  [-d : start backend]"
    echo "  [-c cases|db : delete all cases or database]"
}

while getopts ':sec:d' OPTIONS; do
    case "$OPTIONS" in
        s) s_flag=true ;;
        c)
            if [ $OPTARG == "cases" ]; then
                echo "removing cases"
                rm -rf SupremeCourtCases
            elif [ $OPTARG == "db" ]; then
                echo "removing embeddings"
                rm -rf Backend/chromadb
            else
                error "Unexpected option ${OPTIONS}"
            fi
            ;;
        e) e_flag=true ;;
        d) d_flag=true ;;
        :)
            echo "argument required"
            help
            ;;
        ?)
            help
            ;;
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
    cd Backend
    python -u VectorDB.py > VectorDB.log
fi

if $d_flag; then
    echo "Starting backend"
    cd Backend
    uvicorn API:api --reload
    cd ..
fi
