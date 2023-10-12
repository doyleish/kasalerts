from notifical.daemon import Daemon
from notifical.feed import Feed, EventStartTrigger
from alert import blink_location
import asyncio

async def _blink_office_blue():
    await blink_location("office", color="blue")

feed = Feed(
    'https://calendar.google.com/calendar/ical/ryan.doyle%40panther.io/public/basic.ics',
    triggers = [ EventStartTrigger(trigger=_blink_office_blue, offset = -30) ]
)

daemon = Daemon(feed)
daemon.run()
