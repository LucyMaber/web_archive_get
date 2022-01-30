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
    # __arquivo,
    # __archive,
    __cc
]

setup = False


async def list_page(url, roles=[], archive_list=__archive_list):
    for i in archive_list:
        async for x in i.list_page(url, roles):
            yield x


async def list_subdoamin(url, roles=[], archive_list=__archive_list):
    for i in archive_list:
        async for x in i.list_subdoamin(url, roles):
            yield x


async def search_url_host(url, roles=[], archive_list=__archive_list):
    for i in archive_list:
        async for x in i.search_url_host(url, roles):
            yield x


async def search_url_subpath(url, roles=[], archive_list=__archive_list):
    for i in archive_list:
        async for x in i.search_url_subpath(url, roles):
            yield x

# bluk v1


async def list_bulk_page(configs):

    async with ClientSession() as client:
        for config in configs:
            for i in __archive_list:
                config.append()
                async for x in i.async_bulk_list_page(config, client):
                    yield x


async def list_bulk_subdoamin(configs):

    async with ClientSession() as client:
        for config in configs:
            for i in __archive_list:
                async for x in i.async_bulk_list_subdoamin(config, client):
                    yield x


async def list_bulk_subdoamin2(configs):
    # asyncio.as_completed
    data = []
    async with ClientSession() as client:
        for config in configs:
            for i in __archive_list:
                data.append(i.async_bulk_list_subdoamin(config, client))
        combine = stream.merge(*data)
        async with combine.stream() as streamer:
            async for item in streamer:
                yield item


async def search_bulk_url_host(configs):
    data = []
    async with ClientSession() as client:
        for config in configs:
            for i in __archive_list:
                data.append(i.async_bulk_search_url_host(config, client))
        combine = stream.merge(*data)
        async with combine.stream() as streamer:
            async for item in streamer:
                yield item


async def search_bulk_url_subpath(configs):
    data = []
    async with ClientSession() as client:
        for config in configs:
            for i in __archive_list:
                data.append(i.async_bulk_search_url_subpath(config, client))
        combine = stream.merge(*data)
        async with combine.stream() as streamer:
            async for item in streamer:
                yield item


async def search_bulk_url_raw(configs):
    # asyncio.as_completed
    data = []
    async with ClientSession() as client:
        for config in configs:
            for i in __archive_list:
                data.append(i.async_bulk_lookup(config, client))
    for res in asyncio.as_completed(data):
        pass
        async for x in i.async_bulk_lookup(config, client):
            yield x
# bluk v2


async def list_bulk_page_v2(configs, client):
    for config in configs:
        for i in __archive_list:
            config.append()
            async for x in i.async_bulk_list_page(config, client):
                yield x


async def list_bulk_subdoamin_v2(configs, client):
    for config in configs:
        config.append(("matchType", "domain"))
        for i in __archive_list:
            async for x in i.async_bulk_list_subdoamin(config, client):
                yield x


async def search_bulk_url_host_v2(configs, client):
    for config in configs:
        for i in __archive_list:
            async for x in i.async_bulk_lookup(config, client):
                yield x


async def search_bulk_url_subpath_v2(configs, client):
    for config in configs:
        for i in __archive_list:
            async for x in i.async_bulk_search_url_subpath(config, client):
                yield x


async def search_bulk_url_raw_v2(configs, client):
    for config in configs:
        for i in __archive_list:
            async for x in i.async_bulk_search_url_subpath(config, client):
                yield x
# blocking


def blocking_list_page(url, roles=[], archive_list=__archive_list):
    for i in archive_list:
        for x in i.blocking_list_page(url, roles):
            yield x


def blocking_list_subdoamin(url, roles=[], archive_list=__archive_list):
    for i in archive_list:
        for x in i.blocking_list_subdoamin(url, roles):
            yield x


def blocking_search_url_host(url, roles=[], archive_list=__archive_list):
    for i in archive_list:
        for x in i.blocking_search_url_host(url, roles):
            yield x


def blocking_search_url_subpath(url, roles=[], archive_list=__archive_list):
    for i in archive_list:
        for x in i.blocking_search_url_subpath(url, roles):
            yield x
