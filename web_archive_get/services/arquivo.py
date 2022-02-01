
import asyncio
import json
from tkinter import N
from tkinter.messagebox import NO
from urllib import request
from urllib.parse import urljoin
from aiohttp import ClientSession, RequestInfo
from requests.models import PreparedRequest
from web_archive_get.services.cdx import CDX
from web_archive_get.utils import prepare_url

import requests
lock = asyncio.Lock()

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
        "replace_operator": ""
    })
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


sem = asyncio.Semaphore(1)


class arquivo_url:
    def __init__(self, data):
        self.data = data

    def get_length(self):
        try:
            return self.data["length"]
        except:
            return None

    def get_statuscode(self):
        try:
            return None
        except:
            return None

    def get_mimetype(self):
        try:
            return self.data["mimetype"]
        except:
            return None

    def get_url(self):
        return self.data["url"]

    async def request(self):
        url_dir = "https://arquivo.pt/wayback/" + \
            self.data["timestamp"] + "/"+self.data["url"]
        async with ClientSession() as client:
            async with client.get(url_dir, timeout=9999999) as response:
                try:
                    return await response.text()
                except:
                    return await response.content.read()


class arquivo(CDX):

    def __init__(self) -> None:
        self.endpoints = ["https://arquivo.pt/wayback/cdx"]

    async def async_lookup(self, url, params):
        list_url = []
        async with ClientSession() as client:
            params.append(("output", "json"))
            params.append(("url", url))
            for endpoint in self.endpoints:
                params.append(("showNumPages", "false"))
                url = prepare_url(endpoint, params)
                ok = False
                while not ok:
                    async with client.get(url, timeout=9999999) as response:
                        ok = response.ok
                        if response.ok:
                            text = await response.text()
                            links = text.split("\n")
                            for link in links:
                                try:
                                    x = json.loads(link)
                                    yield arquivo_url(x)
                                except:
                                    pass

    def blocking_lookup(self, url, params):
        list_url = []
        params.append(("output", "json"))
        params.append(("url", url))
        for endpoint in self.endpoints:
            params.append(("showNumPages", "false"))
            url = prepare_url(endpoint, params)
            ok = False
            while not ok:
                response = requests.get(url)
                ok = response.ok
                if response.ok:
                    links = (response.text).split("\n")
                    for link in links:
                        try:
                            x = json.loads(link)
                            yield arquivo_url(x)
                        except:
                            pass
        return list_url

    async def async_bulk_lookup(self, parameter, session):
        for endpoint in self.endpoints:
            while True:
                await asyncio.sleep(5)

                try:
                    url = parameter.parameter_page_n(endpoint)
                    async with session.get(url, timeout=9999999) as response:
                        data = await response.json()
                    for i in data[1:]:
                        l = {}
                        for count, item in enumerate(data[0], start=0):
                            l[item] = i[count]
                        yield arquivo_url(l)
                    break
                except:
                    continue

    async def bulk_lookup(self, parameter, session):
        for endpoint in self.endpoints:
            parameter.append(("showNumPages", "false"))
            req_page = PreparedRequest()
            req_page.prepare_url(endpoint, parameter)
            ok = False
            while not ok:
                async with lock:
                    async with session.get(req_page.url, timeout=9999999) as response:
                        ok = response.ok
                        if response.ok:
                            links = (response.text).split("\n")
                            for link in links:
                                try:
                                    x = json.loads(link)
                                    yield arquivo_url(x)
                                except:
                                    pass

    async def async_bulk_lookup(self, parameter, session):
        for endpoint in self.endpoints:
            url_count = parameter.gen_page_count(endpoint)
            async with lock:
                while True:
                    async with sem:
                        async with session.get(url_count, timeout=9999999) as response:
                            try:
                                if response.ok:
                                    count_ = int(await response.text())
                                    break
                                else:
                                    print("arquivo Error:", await response.text())
                                    await asyncio.sleep(30)
                            except:
                                count_ = 1
                async with sem:
                    for i in range(count_):
                        parameter_page_n = parameter[0:-1]
                        url_ = parameter.parameter_page_n(endpoint, count=i)
                        async with lock:
                            while True:
                                async with session.get(url_, timeout=9999999) as response:
                                    ok = response.ok
                                    if ok:
                                        a = await response.text()
                                        links = (a).split("\n")
                                        if len(links) == 0:
                                            break
                                        for link in links:
                                            try:
                                                x = json.loads(link)
                                                yield arquivo_url(x)
                                            except:
                                                pass
                                        break
                                    else:
                                        print("arquivo Error:", await response.text())
                                        await asyncio.sleep(30)


if __name__ == '__main__':
    cc = arquivo()
    loop = asyncio.get_event_loop()
    a = cc.async_search_url_subpath("www.pirateparty.org.uk/blog/")
    s = loop.run_until_complete(a)
