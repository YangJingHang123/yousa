import time
import datetime
import yaml

from aiocqhttp import CQHttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bilibili import monitor_dynamic
from bilibili import monitor_live
from utils import process_config

cq_url = 'http://127.0.0.1:5700/'

ONE_HOUR = 3600

bot = CQHttp(api_root=cq_url)

last_time = int(time.time())
sched = AsyncIOScheduler()
live_states = dict()


async def live_repost():
    global last_time
    status = await monitor_live(last_time)
    live_room_ids: list(int) = status['live']

    if live_room_ids != []:
        for room_id in live_room_ids:
            if live_states.get(room_id, None) is None or int(time.time()) > live_states.get(room_id, None)+ONE_HOUR:
                for group_id in room_monitor_config[room_id]['group_ids']:
                    print("OK_live")
                    await bot.send({'group_id': group_id}, '正在直播中: https://live.bilibili.com/{room_id}'.format(room_id=room_id))
                    live_states[room_id] = int(time.time())

    last_time = int(time.time())
    print("last_test_time:"+datetime.datetime.now().isoformat())


async def dynamic_repost():
    global last_time
    status = await monitor_dynamic(last_time)
    new_dynamics: list(int) = status['dynamic']

    if new_dynamics != []:
        for dynamic in new_dynamics:
            for group_id in dynamic_monitor_config[dynamic.user_id]['group_ids']:
                print("OK_dynamic")
                await bot.send({'group_id': group_id}, '新的动态' + '\n' + dynamic.content + '\n' + dynamic.url)

    last_time = int(time.time())
    print("last_test_time:"+datetime.datetime.now().isoformat())


if __name__ == "__main__":
    config = yaml.safe_load(open('./bilibili.yaml', 'rb'))

    dynamic_monitor_config = process_config(config['user_monitor'], 'dynamic')
    room_monitor_config = process_config(config['room_monitor'], 'room')

    sched.add_job(dynamic_repost, 'interval', seconds=30)
    sched.add_job(live_repost, 'interval', seconds=30)
    sched.start()

    bot.run(host='127.0.0.1', port=8080)
