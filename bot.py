import time
import datetime
import asyncio
import yaml

from aiocqhttp import CQHttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bilibili import monitor
from remind import TimeCommand

cq_url = 'http://127.0.0.1:5700/'

bot = CQHttp(api_root=cq_url)

last_time = int(time.time())
sched = AsyncIOScheduler()
str_to_command = TimeCommand()


async def dynamic_and_live_repost():
    global last_time
    status = await monitor(last_time)

    live_room_ids = status['live']
    new_dynamics = status['dynamic']

    if new_dynamics != []:
        for dynamic in new_dynamics:
            for group_id in dynamic_monitor_config[dynamic.user_id]:
                await bot.send({'group_id': group_id}, dynamic.content + '\n' + dynamic.url)

    if live_room_ids != []:
        for room_id in live_room_ids:
            for group_id in room_monitor_config[room_id]:
                await bot.send({'group_id': group_id}, 'https://live.bilibili.com/{room_id}'.format(room_id))

    last_time = int(time.time())
    print(datetime.datetime.now().isoformat())


def process_config(configs, type):
    resp = dict()
    _id = 'user_id' if type == 'dynamic' else 'room_id'
    _ids = 'user_ids' if type == 'dynamic' else 'room_ids'
    resp[_ids] = list()
    for config in configs:
        resp.update({config[_id]: config})
        resp[_ids].append(config[_id])
    return resp


if __name__ == "__main__":
    config = yaml.safe_load(open('./bilibili.yaml', 'rb'))

    dynamic_monitor_config = process_config(config['user_monitor'], 'dynamic')
    room_monitor_config = process_config(config['room_monitor'], 'room')

    sched.add_job(dynamic_and_live_repost, 'interval', seconds=30)
    sched.start()

    bot.run(host='127.0.0.1', port=8080, loop=asyncio.get_event_loop())
