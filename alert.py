from kasa import SmartBulb
import asyncio
import time
from bottle import post, run, request 

bulbs = {
    "office": ["10.0.1.15"]
}

speeds = {
    "slow": 1.8,
    "medium": 1.3,
    "fast": 0.8
}

max_blink = 30

hsvs = {
    "red": [0, 100, 100],
    "green": [120, 100, 100],
    "blue": [240, 100, 100]
}

bulb_params = ["blink_count","blink_speed","color"]

async def blink_bulb(bulb: SmartBulb, blink_count=5, blink_speed="medium", color="red"):
    cycles = min(blink_count, max_blink)
    cycle_time = speeds.get(blink_speed, speeds["medium"])
    hsv = hsvs.get(color, hsvs["red"])
    for i in range(0,cycles):
        await bulb.set_hsv(*hsv)
        time.sleep((cycle_time/2)-0.015)
        await bulb.turn_off()
        time.sleep((cycle_time/2)-0.015)


async def blink_location(location, **kwargs):
    alert_bulbs = [SmartBulb(b) for b in bulbs[location]]
    await asyncio.gather(*[b.update() for b in alert_bulbs])
    await asyncio.gather(*[blink_bulb(b, **kwargs) for b in alert_bulbs])
    

@post('/bulbs/<location>')
def alert(location=None):
    if location and location in bulbs.keys():
        params = {}
        for p, v in request.params.items():
            if p in bulb_params:
                params[p] = v
                if p == "blink_count":
                    params[p] = int(v)

            
        asyncio.run(blink_location(location, **params))
        return f"All bulbs in {location} alerted" 
    else:
        return "Please provide a valid location in /bulbs/<location>"


run(host='0.0.0.0', port=5908)
