import asyncio

events = []


async def event_generator():
    while True:
        if events:
            data = events.pop(0)
            yield f"data: {data}\n\n"
        await asyncio.sleep(1)


def add_event(message):
    events.append(message)
