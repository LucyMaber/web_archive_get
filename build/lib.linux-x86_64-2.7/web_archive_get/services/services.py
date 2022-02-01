import aiohttp


class services:
    __can_filter = True

    def __init__(self) -> None:
        pass

    async def async_list_page(self, url, role=[]):
        pass

    async def async_list_subdoamin(self, url, role=[]):
        pass

    async def async_search_url_host(self, url, role=[]):
        pass

    async def async_search_url_subpath(self, url, role=[]):
        pass
     # BLUK

    async def list_bulk(self, parameter, session):
        yield
    # Blocking

    def blocking_list_page(self, url, role=[]):
        pass

    def blocking_list_subdoamin(self, url, role=[]):
        pass

    def blocking_search_url_host(self, url, role=[]):
        pass

    def blocking_search_url_subpath(self, url, role=[]):
        pass

    async def async_lookup(self, url, params):
        yield

    async def async_bulk_lookup(self, parameter, session):
        yield

    def blocking_lookup(self, url, params):
        yield
