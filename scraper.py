import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from encodings.aliases import aliases

# turn href into a valid request url
def handleHref(href: str, domain: str) -> str:
    #print(f"NOW HANDLE DOMAIN: {domain} HREF: {href}")
    parsedUrl = urlparse(href)
    if parsedUrl.netloc == "":
        return "http://" + domain + parsedUrl.path
    return "http://" + parsedUrl.netloc + parsedUrl.path


# a implement of url validity
def isValidUrl(url: str) -> bool:
    parsedUrl = urlparse(url)
    return (".ics.uci.edu" in parsedUrl.netloc \
        or ".cs.uci.edu" in parsedUrl.netloc \
        or ".informatics.uci.edu" in parsedUrl.netloc \
        or ".stat.uci.edu" in parsedUrl.netloc \
        or "today.uci.edu/department/information_computer_sciences" in parsedUrl.netloc) \
        and "wics.ics.uci.edu/events" not in (parsedUrl.netloc + parsedUrl.path)\
        and "/calendar/" not in parsedUrl.path \
        and "/pdf/" not in parsedUrl.path
                        
def scraper(url, resp):
    #print(f"from scraper: {url} Status: {resp.status}")
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    if 200 <= resp.status < 400:
        links = set()
        domain = urlparse(resp.url).netloc
        try:
            crawled_text = resp.raw_response.content.decode("utf8")
        except UnicodeDecodeError:
            crawled_text = resp.raw_response.content.decode("iso8859")     
        soup = BeautifulSoup(crawled_text, 'lxml')
        for atag in soup.find_all('a'):
            href = atag.get("href")
            if href != None:
                url = handleHref(href, domain)
                if isValidUrl(url):
                    links.add(url)
        return list(links)
    return []
    # Implementation requred.

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
            + r"|sql|txt|odc"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise




