
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
                print(url)
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
        parameter.append(("output", "json"))
        for endpoint in self.endpoints:
            while True:
                await asyncio.sleep(5)

                try:
                    pach = [
                        ("timestamp:",       "timestamp:"),
                        ("url:",             "original:"),
                        ("mime:",            "mimetype:"),
                        ("status:",          "statuscode:"),
                        ("=timestamp:",      "=timestamp:"),
                        ("=url:",            "=original:"),
                        ("=mime:",           "=mimetype:"),
                        ("=status:",         "=statuscode:"),
                        ("~timestamp:",      "~timestamp:"),
                        ("~url:",            "~original:"),
                        ("~mime:",           "~mimetype:"),
                        ("~status:",         "~statuscode:"),
                        ("!timestamp:",      "!timestamp:"),
                        ("!url:",            "!original:"),
                        ("!mime:",           "!mimetype:"),
                        ("!status:",         "!statuscode:"),
                        ("!=timestamp:",     "!=timestamp:"),
                        ("!=url:",           "!=original:"),
                        ("!=mime:",          "!=mimetype:"),
                        ("!=status:",        "!=statuscode:"),
                        ("!~timestamp:",     "!~timestamp:"),
                        ("!~url:",           "!~original:"),
                        ("!~mime:",          "!~mimetype:"),
                        ("!~status:",        "!~statuscode:"),
                    ]
                    req_page = prepare_url(endpoint, parameter, pach)
                    async with session.get(req_page, timeout=9999999) as response:
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
        parameter.append(("output", "json"))
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
        parameter.append(("output", "json"))
        parameter_page_Count = parameter
        parameter_page_Count.append(("showNumPages", "true"))
        for endpoint in self.endpoints:
            url_count = prepare_url(endpoint, parameter_page_Count)
            async with lock:
                async with session.get(url_count, timeout=9999999) as response:
                    try:
                        count_ = int(await response.text())
                    except:
                        count_ = 0
                for i in range(count_):
                    parameter_page_n = parameter[0:-1]
                    parameter_page_n.append(("page", str(i)))
                    url_ = prepare_url(endpoint, parameter_page_n)
                    parameter_page_n.append(("page", str(i)))
                    async with session.get(url_, timeout=9999999) as response:
                        ok = response.ok
                        if ok:
                            a = await response.text()
                            links = (a).split("\n")
                            for link in links:
                                try:
                                    x = json.loads(link)
                                    yield arquivo_url(x)
                                except:
                                    pass


if __name__ == '__main__':
    cc = arquivo()
    loop = asyncio.get_event_loop()
    a = cc.async_search_url_subpath("www.pirateparty.org.uk/blog/")
    s = loop.run_until_complete(a)
