
import datetime
import json
from logging import raiseExceptions
import time
from urllib import request
from urllib.parse import urljoin
from aiohttp import ClientSession
from requests.models import PreparedRequest
from warcio.archiveiterator import ArchiveIterator
import asyncio
import gzip
from web_archive_get.utils import prepare_url
from web_archive_get.services.cdx import CDX
from io import BytesIO
import tldextract


class web_archive_url():
    def __init__(self, data):
        self.data = data

    def get_length(self):
        return self.data["length"]

    def get_statuscode(self, roles=[]):
        try:
            return int(self.data["statuscode"])
        except:
            return 200

    def get_mimetype(self, roles=[]):
        try:
            return self.data["mimetype"]
        except:
            return None

    def get_url(self, roles=[]):
        return self.data["original"]

    async def request(self):
        url_dir = urljoin("http://web.archive.org/web/",
                          self.data["timestamp"]) + "/" + self.data["original"]
        async with ClientSession() as client:
            async with client.get(url_dir, timeout=9999999) as response:
                try:
                    return await response.text()
                except:
                    return await response.content.read()


class web_archive(CDX):
    def __init__(self) -> None:
        self.endpoints = [
            "http://web.archive.org/cdx/search/cdx"
        ]

    async def lookup(self, url, params):
        params.append(("output", "json"))
        params.append(("url", url))
        for endpoint in self.endpoints:
            req_page = PreparedRequest()
            req_page.prepare_url(endpoint, params)
            x = []
            async with ClientSession() as client:
                async with client.get(req_page.url, timeout=9999999) as response:
                    data = await response.json()
            for i in data[1:]:
                l = {}
                for count, item in enumerate(data[0], start=0):
                    l[item] = i[count]
                yield web_archive_url(l)

    async def async_bulk_lookup(self, parameter, session):
        parameter.append(("output", "json"))
        for endpoint in self.endpoints:
            parameter_page_Count = list(parameter)
            parameter_page_Count.append(("showNumPages", "true"))
            pach = [
                ("^timestamp:",  "timestamp:"),
                ("^original:",   "url:"),
                ("^mime:",   "mimetype:"),
                ("^statuscode:", "status:"),
                ("^=timestamp:",  "=timestamp:"),
                ("^=original:",   "=url:"),
                ("^=mimetype:",   "=:mime"),
                ("^=statuscode:", "=status:"),
                ("^~timestamp:",  "~timestamp:"),
                ("^~original:",   "~url:"),
                ("^~mime:",   "~mimetype:"),
                ("^~statuscode:", "~status:"),
                ("^!=timestamp:",  "!=timestamp:"),
                ("^!=original:",   "!=url:"),
                ("^!=mime:",   "!=mimetype:"),
                ("^!=statuscode:", "!=status:"),
                ("^!=timestamp:",  "!=timestamp:"),
                ("^!=original:",   "!=url:"),
                ("^!=mime:",   "!=mimetype:"),
                ("^!=statuscode:", "!=status:"),
                ("^!timestamp:",  "!timestamp:"),
                ("^!original:",   "!url:"),
                ("^!mime:",   "!mimetype:"),
                ("^!statuscode:", "!status:"),
                ("^!~timestamp:",  "!~timestamp:"),
                ("^!~original:",   "!~url:"),
                ("^!~mime:",   "!~mimetype:"),
                ("^!~statuscode:", "!~status:"),
            ]
            url_count = prepare_url(endpoint, parameter_page_Count, pach)
            async with lock:
                async with session.get(url_count, timeout=9999999) as response:
                    count_ = int(await response.text())
                for i in range(count_):
                    parameter_page_n = parameter[0:-1]
                    parameter_page_n.append(("page", str(i)))
                    parameter_page_n.append(("output", "json"))
                    url_ = prepare_url(endpoint, parameter_page_n)
                    while True:
                        async with session.get(url_, timeout=9999999) as response:
                            if response.ok:
                                data = await response.json()
                                for i in data[1:]:
                                    l = {}
                                    for count, item in enumerate(data[0], start=0):
                                        l[item] = i[count]
                                    yield web_archive_url(l)
                                break


lock = asyncio.Lock()

if __name__ == '__main__':
    cc = web_archive()
    loop = asyncio.get_event_loop()
    a = cc.async_search_url_subpath("www.pirateparty.org.uk/blog/")
    s = loop.run_until_complete(a)
    text = loop.run_until_complete(s[0].request())
    #
