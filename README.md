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
2. Run `./run.sh -e` to embed the court cases for the Chroma database. This process is run on the gpu but could be run on the gpu. When running on the gpu this process takes !!!!!!. The Chroma database is saved in the `.chroma` directory.
3. Run `./run.sh -d` to start the server. 
