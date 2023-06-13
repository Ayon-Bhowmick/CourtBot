#!/bin/bash

s_flag=false
e_flag=false
d_flag=false


if [ ! -d "SupremeCourtCases" ]; then
    mkdir SupremeCourtCases
fi

function help() {
    echo "$(basename $0)"
    echo "  [-s : to scrape sc decisions]"
    echo "  [-e : to embed court decisions]"
    echo "  [-d : to start vector database]"
    echo "  [-c cases|db : to delete all cases or database]"
}

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
        :)
            echo "argument required"
            help()
            ;;
        *) help() ;;
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
