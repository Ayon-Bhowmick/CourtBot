import os
import concurrent.futures

def remove_lines():
    while len(cases) > 0:
        case = cases.pop()
        with open(f"../SupremeCourtCases/{case}", "r+") as file:
            text = file.read()
            text = text.split("\n")
            keep = [line for line in text if len(line.split(" ")) >= 16]
            file.seek(0)
            file.write("\n".join(keep))
            file.truncate()



if __name__ == "__main__":
    cases = os.listdir("../SupremeCourtCases")
    while len(cases) > 0:
        print(len(cases))
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=100)
        clean_futures = [pool.submit(remove_lines) for _ in range(100)]
        pool.shutdown(wait=True)
    print("done", len(cases))
