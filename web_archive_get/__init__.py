"""
web_archive_get.

An example python library.
"""

from aiostream import stream
import aiostream
__version__ = "0.1.0.5"
__author__ = 'Willdor'
__credits__ = ''

import asyncio
from aiohttp import ClientSession
from web_archive_get.services.archive import archive
from web_archive_get.services.common_crawl_index import common_crawl_index
from web_archive_get.services.web_archive import web_archive
from web_archive_get.services.arquivo import arquivo

__archive = archive()
__web_archive = web_archive()
__arquivo = arquivo()
__cc = common_crawl_index()
__archive_list = [
    # __web_archive,
    __arquivo,
    # __archive,
    # __cc
]

setup = False


async def list_page(url, roles=[], archive_list=__archive_list):
    for i in archive_list:
        async for x in i.list_page(url, roles):
            yield x

# bluk v1


async def list_bulk(configs, archive_list=__archive_list):
    # asyncio.as_completed
    data = []
    async with ClientSession() as client:
        for config in configs:
            for i in archive_list:
                data.append(i.list_bulk(config, client))
        combine = stream.merge(*data)
        async with combine.stream() as streamer:
            async for item in streamer:
                print("!", type(item))
                if isinstance(item, str):
                    yield item
                else:
                    print("w", item)


# blocking
def blocking_search(url, roles=[], archive_list=__archive_list):
    for i in archive_list:
        for x in i.blocking_search_url_subpath(url, roles):
            yield x
