class CDX:
    def __init__(self) -> None:
        pass

    async def list_page(self, url, roles=[]):
        params = {}
        for i in await self.lookup(url, params):
            yield i

    async def list_subdoamin(self, url, roles=[]):
        params = {"matchType": "domain"}
        for i in await self.lookup(url, params):
            yield i

    async def search_url_host(self, url, roles=[]):
        params = {
            "matchType": "host"
        }
        for i in await self.lookup(url, params):
            yield i

    async def search_url_subpath(self, url, roles=[]):
        params = {"matchType": "prefix"}
        for i in await self.lookup(url, params):
            yield i

    async def lookup(url, params):
        pass


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