import re
from urllib.parse import urlparse
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self, url):
        HTMLParser.__init__(self)
        self.url = url
        if self.url[-1] == "/":
            self.url = self.url[:-1]

    def getHrefList(self):
        return list(self.hrefSet)

    def handle_starttag(self, tag, attrs):
        self.hrefSet = set()
        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    if len(value) > 1:
                        if value[0] == "/" and value[1] == "/":
                            self.hrefSet.add("http:" + value)
                        elif value[0] == "/" and value[1] != "/":
                            self.hrefSet.add(self.url + value)
                        elif value[0] != "#":
                            self.hrefSet.add(value)

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation requred.
    with urlopen(url) as f:
        htmlParser = MyHTMLParser()
        htmlParser.feed(f.read().decode("utf-8"))
    return htmlParser.getHrefList()

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