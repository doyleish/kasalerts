import requests
import sys
import asyncio
import time

from icalendar import Calendar
from datetime import datetime, timezone

from alert import blink_location

EVENT_LOOP_SPEED = 300
PRE_WARNING = 30

async def sleep_and_fire(seconds, location):
    print(f"Waiting {seconds} seconds")
    await asyncio.sleep(seconds)
    print("Blink!")
    await blink_location(location)

async def get_cal(url):
    print(f"Fetching calendar")
    resp = requests.get(url)
    return Calendar.from_ical(resp.content)

async def schedule_near_events(reftime, cal, location):
    print(f"Walking events")
    for event in cal.walk("VEVENT"):
        delta = event['DTSTART'].dt - reftime
        s = delta.total_seconds()
        print(s)
        if PRE_WARNING < s < EVENT_LOOP_SPEED+PRE_WARNING:
            print(f"Firing for upcoming event")
            asyncio.ensure_future(sleep_and_fire(s-PRE_WARNING, location))

async def poll_loop(url, location):
    while True:
        now = datetime.now(timezone.utc)
        cal = await get_cal(url)
        await asyncio.gather(
          schedule_near_events(now, cal, location),
          asyncio.sleep(EVENT_LOOP_SPEED)
        )


if __name__ == "__main__":
    asyncio.run(poll_loop(sys.argv[1], sys.argv[2]))
