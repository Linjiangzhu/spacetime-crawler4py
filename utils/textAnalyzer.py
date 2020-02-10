from bs4 import BeautifulSoup
import re
from collections import defaultdict
# def pageTextExtract(rawText):
#     decode_text = ""
#     try:
#         decode_text = rawText.decode("utf8")
#     except UnicodeDecodeError:
#         decode_text = rawText.decode("iso8859")    
#     soup = BeautifulSoup(decode_text, 'lxml')
#     return soup.get_text()


# def wordCounter(text):
#     wc = 0
#     for line in text.splitlines():
#         for w in re.findall(r"[a-zA-Z0-9]+", line):
#             wc += 1
#     return wc
    
class TextAnalyzer:
    def __init__(self, rawText):
        self.rawText = rawText
        self.text = ""
        self.wordCount = 0
        self.tokenDict = defaultdict(int)
    def textExtract(self):
        decode_text = ""
        try:
            decode_text = self.rawText.decode("utf8")
        except UnicodeDecodeError:
            decode_text = self.rawText.decode("iso8859")    
        soup = BeautifulSoup(decode_text, 'lxml')
        self.text = soup.get_text()
    def execute(self):
        self.textExtract()
        for line in self.text.splitlines():
            for w in re.findall(r"[a-zA-Z0-9]+", line):
                self.wordCount += 1
                self.tokenDict[w] += 1
    def getWordCount(self):
        return self.wordCount
    def updateOldDict(self, d):
        for k, v in self.tokenDict.items():
            d[k] += v
            
