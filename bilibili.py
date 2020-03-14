import yaml
import asyncio
import traceback
from aiohttp import request

from dynamic import Dynamic

dynamic_keys_from_type = {
    1: ['item', 'content'],
    2: ['item', 'description'],
    4: ['item', 'content'],
    8: ['dynamic']
}


def get_value(obj: dict, keys: list):
    for key in keys:
        obj = obj[key]
    return obj


def get_dynamic(card: dict):
    try:
        _dynamic = Dynamic(card)
    except Exception:
        traceback.print_exc()
    return _dynamic


async def user_dynamic(user_id: str) -> dict:
    api_url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history'
    async with request("GET", api_url, params={'host_uid': user_id, 'visitor_id': "0", 'offset_dynamic_id': "0"}) as response:
        cards = (await response.json())['data']['cards']

        return [get_dynamic(card) for card in cards]


def filter_dynamic(items: list, timestamp: int):
    return [item for item in items if item.timestamp > timestamp]


async def user_new_dynamic(user_ids: list, timestamp: int):
    new_dynamics = []
    for user_id in user_ids:
        dynamics = await user_dynamic(user_id)

        _new_dynamics = filter_dynamic(dynamics, timestamp)
        if _new_dynamics != []:
            new_dynamics.extend(_new_dynamics)

    return new_dynamics


async def room_status(room_id: str):
    room_info_url = 'https://api.live.bilibili.com/room/v1/Room/get_info'
    async with request('GET', room_info_url, params={'room_id': room_id}) as resp:
        response = (await resp.json())

        if response['msg'] == 'ok':
            return response['data']['live_status'] == 1
        else:
            raise ValueError(str(response))


async def monitor(timestamp: int):
    config = yaml.safe_load(open('./bilibili.yaml', 'rb'))

    user_monitor_config = config['user_monitor']
    room_monitor_config = config['room_monitor']

    new_dynamics = await user_new_dynamic(user_monitor_config['user_ids'], timestamp)

    live_room_ids = [room_id for room_id in room_monitor_config['room_ids'] if await room_status(room_id)]

    return {'dynamic': new_dynamics, 'live': live_room_ids}


if __name__ == "__main__":
    asyncio.run(monitor(1583232556))
