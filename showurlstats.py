from os import path

def getMaxWordCount(filepath):
    maxCount = 0
    maxCountURL = ""
    with open(filepath) as f:
        for line in f:
            el = line.split()
            num = int(el[0])
            url = el[1]
            if num > maxCount:
                maxCount = num
                maxCountURL = url
    print(f"Web Page with most number of words:\n{maxCountURL} {maxCount} words")



if __name__ == "__main__":
    if path.exists("word-count.txt"):
        getMaxWordCount("word-count.txt")
    if path.exists("word-token.txt"):
        pass
    if path.exists("url-group.txt"):
        pass
