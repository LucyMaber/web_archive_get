import asyncio
import web_archive_get


async def main():
    c = [
        [("url", "bbc.co.uk")]
    ]
    a = web_archive_get.list_bulk_subdoamin2(c)
    # print(a)
    async for i in a:
        if i is None:
            continue

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    s = loop.run_until_complete(main())
