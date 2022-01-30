import asyncio


class Error(Exception):
    pass


async def main():
    try:
        a = [raise_exception(), no_raise_exception()]
        done, pending = await asyncio.wait(a, return_when=asyncio.ALL_COMPLETED)
        future, = done  # unpack a set of length one
        print(future.result())  # raise an exception or use future.exception()
    except Error:
        print('got exception', flush=True)
    else:
        print('no exception', flush=True)


async def raise_exception():  # normally it is a generator (yield from)
    #  or it returns a Future
    raise Error("message")


async def no_raise_exception():  # normally it is a generator (yield from)
    #  or it returns a Future
    return 32

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
