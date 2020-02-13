from bs4 import BeautifulSoup
from bs4.element import Comment
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
    def isVisibleTag(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True
    def textExtract(self):
        decode_text = ""
        try:
            decode_text = self.rawText.decode("utf8")
        except UnicodeDecodeError:
            decode_text = self.rawText.decode("iso8859")    
        soup = BeautifulSoup(decode_text, 'lxml')
        rawBodyText = soup.findAll(text=True)
        visibleText = filter(self.isVisibleTag, rawBodyText)
        self.text = u" ".join(t.strip() for t in visibleText)
        # print("from text extract", self.text)
    def execute(self):
        self.text = ""
        self.wordCount = 0
        self.tokenDict = defaultdict(int)
        self.textExtract()
        for line in self.text.splitlines():
            for w in re.findall(r"[a-zA-Z0-9']+", line):
                self.wordCount += 1
                self.tokenDict[w.lower()] += 1
    def getWordCount(self):
        return self.wordCount
    def updateOldDict(self, d):
        for k, v in self.tokenDict.items():
            d[k] += v
            
