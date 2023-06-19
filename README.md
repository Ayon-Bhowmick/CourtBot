# CourtBot

## Description

CourtBot is a chat bot which can access all decisions of the Supreme Court of the United States. It can answer questions based on the information in these decisions and cite the specific decisions which it used to answer the question.

## How to Run

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run
```
./run.sh
    [-s : scrape the supreme court cases]
    [-e : to embed court decisions]
    [-d : start backend]
    [-c cases|db : delete all cases or database]
```

1. Run `./run.sh -s` scrapes the supreme court cases from [FindLaw](https://caselaw.findlaw.com/court/us-supreme-court) and prepossesses them for embedding. The time taken to scrape the data is dependent on the number of threads which you allocate and it takes around 3 hours with 50 threads. The data is stored in `SupremeCourtCases` directory as txt files.
2. Run `./run.sh -e` to embed the court cases for the Chroma database. This process is run on the gpu but could be run on the cpu. When running on the gpu this process takes about 14 hours to embed all 21 thousand cases. The Chroma database is saved in the `.chroma` directory.
3. Run `./run.sh -d` to start the server.

## Sources

- The data for the Supreme Court cases is scraped from [FindLaw](https://caselaw.findlaw.com/court/us-supreme-court) using [Selenium](https://www.selenium.dev/) and a chromium web driver.
- The embeddings are calculated using [all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) which is a fine tuned version of Microsoft's [Masked and Permuted Language Modeling (MPNet)](https://huggingface.co/microsoft/mpnet-base) ([arXiv](https://arxiv.org/abs/2004.09297)).
- The vector database used is [Chroma](https://www.trychroma.com/). Chroma is a vector database which allows you to search for similar vectors. It is built on top of DuckDB and Apache Parquet.
- The chat bot is built using Microsoft's [Grounded Open Dialogue Language Model (GODEL)](https://huggingface.co/microsoft/GODEL-v1_1-large-seq2seq) ([arXiv](https://arxiv.org/abs/2206.11309)). This model is trained on 551 million dialogs from Reddit and 5 million instruction and knowledge dialogs.
- The api is built using [FastAPI](https://fastapi.tiangolo.com/) which uses a [uvicorn](https://www.uvicorn.org/) web server.
