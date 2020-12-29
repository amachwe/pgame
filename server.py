from aiohttp import web
import time 
import json
events = {}

async def get_events(request):
    return web.json_response(events)
    

async def register_event(request):
    txt = request.match_info.get("player").replace("\'","\"")
    print(txt)
    player = json.loads(txt)
    event = request.match_info.get("event")

    plr = events.get(player["id"])
    if plr:
        plr[time.time()] = {event:player}
    else:
        events[player["id"]] = {
            time.time():{event:player}
        }
    return web.Response()


app = web.Application()
app.add_routes([web.post('/event/{player}/{event}', register_event),
web.get('/event', get_events)])


if __name__ == '__main__':
    web.run_app(app)