import asyncio
import web_archive_get


async def main():
    c = [
        [["url", "bbc.co.uk"], ["filter", "mimetype:text/html"]]
    ]
    a = web_archive_get.list_bulk_subdoamin2(c)
    async for i in a:
        # print(i.get_url())
        if i is None:
            continue

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    s = loop.run_until_complete(main())
