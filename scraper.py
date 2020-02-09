import re
from urllib.parse import urlparse
from html.parser import HTMLParser
from urllib.request import urlopen
from lxml import etree
from bs4 import BeautifulSoup


# class MyHTMLParser(HTMLParser):
#     def __init__(self, url):
#         HTMLParser.__init__(self)
#         self.hrefSet = set()
#         self.url = url
#         if self.url[-1] == "/":
#             self.url = self.url[:-1]

#     def getHrefList(self):
#         return list(self.hrefSet)

#     def handle_starttag(self, tag, attrs):
#         if tag == "a":
#             for name, value in attrs:
#                 if name == "href":
#                     if len(value) > 1:
#                         domain_url = "https://" + urlparse(self.url).netloc
#                         crawled_url = ""
#                         if value[0] == "/" and value[1] == "/":
#                             crawled_url = "https:" + value
#                         elif value[0] == "/" and value[1] != "/":
#                             crawled_url = domain_url + value
#                         elif value[0] != "#":
#                             crawled_url = value
#                         parsedObj = urlparse(crawled_url)
#                         crawled_url = parsedObj.scheme + "://" + parsedObj.netloc + parsedObj.path
#                         if re.search(r".ics.uci.edu", crawled_url) != None \
#                             or re.search(r".cs.uci.edu", crawled_url) != None \
#                             or re.search(r".stat.uci.edu", crawled_url) != None \
#                             or re.search(r".informatics.uci.edu", crawled_url) != None \
#                             or re.search(r"today.uci.edu/department/information_computer_sciences", crawled_url) != None:
#                             self.hrefSet.add(crawled_url)
# def getAnchorHrefList(resp):
#     url = resp.url
#     print(str(resp.raw_response.content)[:50])
#     tree = etree.XMLPullParser(tag="a")
#     tree.feed(str(resp.raw_response.content)[2:])
#     hrefSet = set()
#     anchorList = [el.get("href") for _, el in parser.read_events()]
#     for href in hrefSet:
#         crawled_url = ""
#         domain = "https://" + urlparse(url).netloc
#         if len(href) > 1:
#             if href[0] == "/" and href[1] == "/":
#                 crawled_url = "https:" + href
#             elif href[0] == "/" and href[1] != "/":
#                 crawled_url = domain + valhrefue
#             elif href[0] != "#":
#                 crawled_url = href
#             parsedObj = urlparse(crawled_url)
#             crawled_url = parsedObj.scheme + "://" + parsedObj.netloc + parsedObj.path
#             if re.search(r".ics.uci.edu", crawled_url) != None \
#                 or re.search(r".cs.uci.edu", crawled_url) != None \
#                 or re.search(r".stat.uci.edu", crawled_url) != None \
#                 or re.search(r".informatics.uci.edu", crawled_url) != None \
#                 or re.search(r"today.uci.edu/department/information_computer_sciences", crawled_url) != None:
#                 hrefSet.add(crawled_url)
#     return list(hrefSet)

def scraper(url, resp):
    #print(f"from scraper: {url} Status: {resp.status}")
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation requred.
    if 200 <= resp.status < 400:
        # htmlParser = MyHTMLParser(resp.url)
        # htmlParser.feed(str(resp.raw_response.content))
        html_text = str(resp.raw_response.content)
        soup = BeautifulSoup(html_text, "lxml")
        hrefSet = set()
        for link in soup.find_all("a"):
            href = link.get("href")
            crawled_url = ""
            domain = "https://" + urlparse(url).netloc
            if href != None and len(href) > 1:
                if href[0] == "/" and href[1] == "/":
                    crawled_url = "https:" + href
                elif href[0] == "/" and href[1] != "/":
                    crawled_url = domain + href
                elif href[0] != "#":
                    crawled_url = href
                parsedObj = urlparse(crawled_url)
                crawled_url = parsedObj.scheme + "://" + parsedObj.netloc + parsedObj.path
                if re.search(r".ics.uci.edu", crawled_url) != None \
                    or re.search(r".cs.uci.edu", crawled_url) != None \
                    or re.search(r".stat.uci.edu", crawled_url) != None \
                    or re.search(r".informatics.uci.edu", crawled_url) != None \
                    or re.search(r"today.uci.edu/department/information_computer_sciences", crawled_url) != None:
                    if re.search(r"wics.ics.uci.edu/events/", crawled_url) == None \
                        and re.search(r"/calendar/", crawled_url) == None:
                        hrefSet.add(crawled_url)
        return list(hrefSet)
    return []

def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise




