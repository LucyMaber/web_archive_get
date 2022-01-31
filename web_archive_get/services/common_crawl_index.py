
import gzip
from io import BytesIO
import json
from urllib.parse import urljoin
from aiohttp import ClientSession
from web_archive_get.utils import prepare_url
from warcio.archiveiterator import ArchiveIterator
import asyncio

from web_archive_get.services.cdx import CDX
import requests
fls = [
    "urlkey",
    "timestamp",
    "url",
    "mime",
    "status",
    "digest",
    "length",
    "offset",
    "filename"
]
fliter_fliters = []
for fl in fls:
    fliter_fliters.append({
        "start": ".*",
        "end": "",
        "operator": "~",
        "parameter": fl,
        "replace_parameter": fl,
        "replace_operator": "~"
    })
    fliter_fliters.append({
        "start": "",
        "end": "",
        "operator": "=",
        "parameter": fl,
        "replace_parameter": fl,
        "replace_operator": "="
    })
    fliter_fliters.append({
        "start": "",
        "end": "",
        "operator": "!",
        "parameter": fl,
        "replace_parameter": fl,
        "replace_operator": "!"
    })
    fliter_fliters.append({
        "start": "",
        "end": "",
        "operator": "!=",
        "parameter": fl,
        "replace_parameter": fl,
        "replace_operator": "!="
    })
    fliter_fliters.append({
        "start": ".*",
        "end": "",
        "operator": "!~",
        "parameter": fl,
        "replace_parameter": fl,
        "replace_operator": "!~"
    })


class common_crawl_index_url():
    def __init__(self, data):
        self.data = data

    def get_length(self):
        return self.data["length"]

    def get_statuscode(self):
        return self.data["statuscode"]

    def get_mimetype(self):
        return self.data["mimetype"]

    def get_url(self):
        return self.data["original"]

    async def request(self):
        url_dir = urljoin("https://commoncrawl.s3.amazonaws.com/",
                          self.data["filename"])
        ok = False
        while not ok:
            async with ClientSession() as client:
                async with client.get(url_dir, timeout=9999999) as response:
                    if response.ok:
                        ok = response.ok
                        outstr = gzip.decompress(await response.content.read())
                        for record in ArchiveIterator(BytesIO(outstr), arc2warc=True):
                            if record.rec_type == "response":
                                header = {}
                                rec_headers = {}
                                return record.content_stream().read()


lock = asyncio.Lock()


class common_crawl_index(CDX):
    def __init__(self) -> None:
        self.endpoints = [
            "https://index.commoncrawl.org/CC-MAIN-2014-49-index"
        ]
        self.setup = False

    async def init_2(self):
        # self.endpoints = []
        # async with ClientSession() as client:
        #     async with client.get("https://index.commoncrawl.org/collinfo.json", timeout=9999999) as response:
        #         for i in await response.json():
        #             self.endpoints.append(i["cdx-api"])
        pass

    async def init_2m(self, client):
        # self.endpoints = []
        # async with client.get("https://index.commoncrawl.org/collinfo.json", timeout=9999999) as response:
        #     for i in await response.json():
        #         self.endpoints.append(i["cdx-api"])
        pass

    def n_init_2(self):
        self.endpoints = []
        response = requests.get(
            "https://index.commoncrawl.org/collinfo.json", timeout=9999999)
        for i in response.json():
            self.endpoints.append(i["cdx-api"])

    async def async_bulk_lookup(self, parameter, session):
        if not self.setup:
            self.setup = True
            await self.init_2m(session)
        # RUN IN EVIL MODE
        page_f = {}
        for endpoint in self.endpoints:
            url = parameter.gen_page_count(endpoint)
            ok = False
            async with lock:
                while not ok:
                    try:
                        async with session.get(url) as response:
                            if response.ok:
                                page_f = json.loads(await response.text())
                            ok = response.ok
                    except:
                        pass
            for pageNum in (range(page_f["pages"])):
                url = parameter.parameter_page_n(endpoint, count=pageNum)
                ok = False
                async with lock:
                    while not ok:
                        try:
                            async with session.get(url) as response:
                                if response.ok:
                                    links = (await response.text()).split("\n")
                                    for link in links:
                                        try:
                                            x = json.loads(link)
                                            yield common_crawl_index_url(x)
                                        except:
                                            pass
                                ok = response.ok
                        except:
                            pass

    async def lookup(self, url, params):
        if not self.setup:
            self.setup = True
            await self.init_2()
        # RUN IN EVIL MODE
        list_url = []
        async with ClientSession() as client:
            page_f = {}
            params.append(("output", "json"))
            params.append(("url", url))
            for endpoint in self.endpoints:
                params.append(("showNumPages", "true"))

                pach = [
                    ("timestamp", "timestamp"),
                    ("url", "original"),
                    ("mime", "mimetype"),
                    ("status", "statuscode"),
                ]
                url = prepare_url(endpoint, params, pach)
                ok = False
                while not ok:
                    async with client.get(url) as response:
                        if response.ok:

                            page_f = await response.text()

                    ok = response.ok
                params.append(("showNumPages", "false"))
                page_f = json.loads(page_f)
                for pageNum in (range(page_f["pages"])):
                    params.append(("showNumPages", "false"))
                    params.append(("page", pageNum))
                    print("page:", pageNum)
                    url = prepare_url(endpoint, params)
                    ok = False
                    while not ok:
                        async with client.get(url) as response:
                            if response.ok:
                                links = (await response.text()).split("\n")
                                for link in links:
                                    try:
                                        x = json.loads(link)
                                        yield common_crawl_index_url(x)
                                    except:
                                        pass
                            ok = response.ok

    def blocking_lookup(self, url, parameter):
        if not self.setup:
            self.setup = True
            self.n_init_2()
        # RUN IN EVIL MODE
        list_url = []
        page_f = {}
        for endpoint in self.endpoints:
            url = parameter.gen_page_count(
                endpoint, filter_ps=fliter_fliters)
            ok = False
            while not ok:
                response = requests.get(url)
                if response.ok:
                    page_f = response.text
                ok = response.ok
            page_f = json.loads(page_f)
            for pageNum in (range(page_f["pages"])):
                url = parameter.parameter_page_n(
                    endpoint, filter_ps=fliter_fliters)
                ok = False
                while not ok:
                    response = requests.get(url)
                    if response.ok:
                        links = (response.text).split("\n")
                        for link in links:
                            try:
                                x = json.loads(link)
                                yield common_crawl_index_url(x)
                            except:
                                pass
                    ok = response.ok


async def main_1():
    cc = common_crawl_index()

    a = await cc.async_search_url_subpath("www.pirateparty.org.uk/blog/")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    s = loop.run_until_complete(main_1())
