from os import path
from urllib.parse import urlparse
from collections import defaultdict

def getNumOfUniquePage(filepath):
    num = 0
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            num += 1
    print(f"Number of unique page:\n{num}\n")
def getMaxWordCount(filepath):
    maxCount = 0
    maxCountURL = ""
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            el = line.split()
            num = int(el[0])
            url = el[1]
            if num > maxCount:
                maxCount = num
                maxCountURL = url
    print(f"Web Page with most number of words:\n{maxCountURL} {maxCount} words\n")

def getWordFreq(filepath, stopwordpath):
    stop_words = set()
    with open(stopwordpath, encoding="utf-8")as f:
        for line in f:
            stop_words.add(line.strip().lower())
    token_list = []
    with open(filepath, encoding="utf=8") as f:
        for line in f:
            split_line = line.split()
            word, count = split_line[0] , int(split_line[1])
            token_list.append((word, count))
    sorted_list = sorted(token_list, key=lambda e: e[1], reverse=True)
    i = 0
    tokenStr = "50 most common words:\n"
    for e in sorted_list:
        if i >= 50:
            break
        try:
            int(e[0])
        except:
            if e[0] not in stop_words:
                tokenStr += f"{e[0]} {e[1]}\n"
                i += 1
    print(tokenStr)
    
def getSubDomain(filepath):
    sub_dict = defaultdict(int)
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            url = line.strip()
            sub_dict[urlparse(url).netloc] += 1
    domain_list = []
    dictStr = "Subdomain List:\n"
    for k, v in sub_dict.items():
        domain_list.append(k.lower())
    sorted_list = sorted(domain_list)
    for u in sorted_list:
        dictStr += f"http://{u} {sub_dict[u]}\n"
    print(dictStr)
if __name__ == "__main__":
    # question 1: unique page
    if path.exists("url-group.txt"):
        getNumOfUniquePage("url-group.txt")

    # question 2: page has the most number of words
    if path.exists("word-count.txt"):
        getMaxWordCount("word-count.txt")

    # question 3: 50 most common words frequencies no stop words
    if path.exists("word-token.txt"):
        getWordFreq("word-token.txt", "stop-words.txt")
    
    # question 4: subdomains with number of pages
    if path.exists("url-group.txt"):
        getSubDomain("url-group.txt")

