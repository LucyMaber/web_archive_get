
import datetime
import json
from logging import raiseExceptions
import time
from urllib import request
from urllib.parse import urljoin
from aiohttp import ClientSession
from warcio.archiveiterator import ArchiveIterator
import asyncio
import gzip
from web_archive_get.utils import prepare_url
from web_archive_get.services.cdx import CDX
from io import BytesIO
import tldextract

fls = [
    ("urlkey", "urlkey"),
    ("timestamp", "timestamp"),
    ("url", "original"),
    ("mime", "mimetype"),
    ("status", "statuscode"),
    ("digest", "digest"),
    ("length", "length"),
    ("offset", "offset"),
    ("filename", "filename")
]
fliter_fliters = []
for fl in fls:
    fliter_fliters.append({
        "start": "",
        "end": "",
        "operator": "",
        "parameter": fl[0],
        "replace_parameter": fl[1],
        "replace_operator": ""
    })
    fliter_fliters.append({
        "start": "",
        "end": "",
        "operator": "~",
        "parameter": fl[0],
        "replace_parameter": fl[1],
        "replace_operator": "~"
    })
    fliter_fliters.append({
        "start": "",
        "end": "",
        "operator": "=",
        "parameter": fl[0],
        "replace_parameter": fl[1],
        "replace_operator": "="
    })
    fliter_fliters.append({
        "start": "",
        "end": "",
        "operator": "!",
        "parameter": fl[0],
        "replace_parameter": fl[1],
        "replace_operator": "!"
    })
    fliter_fliters.append({
        "start": "",
        "end": "",
        "operator": "!=",
        "parameter": fl[0],
        "replace_parameter": fl[1],
        "replace_operator": "!="
    })
    fliter_fliters.append({
        "start": ".*",
        "end": "",
        "operator": "!~",
        "parameter": fl[0],
        "replace_parameter": fl[1],
        "replace_operator": "!~"
    })


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

    async def async_bulk_lookup(self, perator, session):
        for endpoint in self.endpoints:
            url_count = perator.gen_page_count(
                endpoint, filter_ps=fliter_fliters)
            async with lock:
                while True:
                    async with session.get(url_count, timeout=9999999) as response:
                        if response.ok:
                            count_ = int(await response.text())
                            break
                        else:
                            print("web_archive Error:", await response.text())
                            await asyncio.sleep(10)
            for i in range(count_):
                url_ = perator.parameter_page_n(
                    endpoint, filter_ps=fliter_fliters, count=i)
            async with lock:
                while True:
                    async with session.get(url_, timeout=9999999) as response:
                        if response.ok:
                            try:
                                data = await response.json()
                                if len(data) == 0:
                                    break
                                for i in data[1:]:
                                    l = {}
                                    for count, item in enumerate(data[0], start=0):
                                        l[item] = i[count]
                                    yield web_archive_url(l)
                                break
                            except:
                                print("web_archive Error:", await response.text())
                        else:
                            print("web_archive Error:", await response.text())


lock = asyncio.Lock()

if __name__ == '__main__':
    cc = web_archive()
    loop = asyncio.get_event_loop()
    a = cc.async_search_url_subpath("www.pirateparty.org.uk/blog/")
    s = loop.run_until_complete(a)
    text = loop.run_until_complete(s[0].request())
    #
