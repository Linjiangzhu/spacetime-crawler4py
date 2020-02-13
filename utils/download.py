import requests
import cbor
import time

from utils.response import Response
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

def download(url, config, logger=None):
    host, port = config.cache_server
    try:
        robotStatusCode = 404
        robotPath = urlparse(url).netloc + "/robots.txt"
        try:
            robotStatusCode = requests.get(robotPath).status_code
        except:
            pass
        if robotStatusCode == 200:
            r = RobotFileParser()
            r.set_url(robotPath)
            r.read()
            if r.can_fetch(url, f"{config.user_agent}"):
                 resp = requests.get(
                    f"http://{host}:{port}/",
                    params=[("q", f"{url}"), ("u", f"{config.user_agent}")], timeout=2)
            else:
                raise ConnectionError
        else:
            resp = requests.get(
                f"http://{host}:{port}/",
                params=[("q", f"{url}"), ("u", f"{config.user_agent}")], timeout=2)
    except:
        return Response({
        "error": "",
        "status": 408,
        "url": ""})
    if resp:
        return Response(cbor.loads(resp.content))
    logger.error(f"Spacetime Response error {resp} with url {url}.")
    return Response({
        "error": f"Spacetime Response error {resp} with url {url}.",
        "status": resp.status_code,
        "url": url})
