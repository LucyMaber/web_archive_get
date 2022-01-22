import asyncio
import web_archive_get


async def main():
    async for i in web_archive_get.list_subdoamin("www.bbc.co.uk"):
        if i is None:
            continue
        print(i.get_url())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    s = loop.run_until_complete(main())
