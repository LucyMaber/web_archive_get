import aiohttp

from web_archive_get.services.services import services


class CDX(services):
    __can_filter = True

    def __init__(self) -> None:
        pass

    async def async_list_page(self, url, role=[]):
        async for i in self.async_lookup(url, role):
            yield i

    async def async_list_subdoamin(self, url, role=[]):
        role.append(("matchType", "domain"))
        async for i in self.async_lookup(url, role):
            yield i

    async def async_search_url_host(self, url, role=[]):
        role.append(("matchType", "host"))
        async for i in self.async_lookup(url, role):
            yield i

    async def async_search_url_subpath(self, url, role=[]):
        role.append(("matchType", "prefix"))
        async for i in await self.async_lookup(url, role):
            yield i
     # BLUK

    async def async_bulk_list_page(self, parameter, session):
        async for i in self.async_bulk_lookup(list(parameter), session):
            yield i

    async def async_bulk_list_subdoamin(self, parameters, session):
        async for i in self.async_bulk_lookup((parameters), session):
            yield i

    async def async_bulk_list_subdoamin(self, parameters, session):
        async for i in self.async_bulk_lookup((parameters), session):
            yield i

    async def async_bulk_search_url_host(self, parameters, session):
        for parameter in parameters:
            async for i in self.async_bulk_lookup(list(parameter), session):
                yield i

    async def async_bulk_search_url_subpath(self, parameters, session):
        for parameter in parameters:
            async for i in self.async_bulk_lookup(list(parameter), session):
                yield i
    # Blocking

    def blocking_list_page(self, url, role=[]):
        for i in self.blocking_lookup(url, role):
            yield i

    def blocking_list_subdoamin(self, url, role=[]):
        for i in self.blocking_lookup(url, role):
            yield i

    def blocking_search_url_host(self, url, role=[]):
        for i in self.blocking_lookup(url, role):
            yield i

    def blocking_search_url_subpath(self, url, role=[]):
        for i in self.blocking_lookup(url, role):
            yield i

    async def async_lookup(self, url, params):
        yield

    async def async_bulk_lookup(self, parameter, session):
        yield

    def blocking_lookup(self, url, params):
        yield


class PageRequest:
    def __init__(self, data) -> None:
        self.content = data["content"]
        self.raw = data["raw"]
        self.headers = data["headers"]
        self.status = data["status"]
        self.cookies = data["cookies"]
        self.history = data["history"]
        self.url = data["url"]
        self.status_code = data["status_code"]

    def request(self, data) -> None:
        pass
