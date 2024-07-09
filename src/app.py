import asyncio

from server import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Keyboard interrupted")
    except AttributeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
