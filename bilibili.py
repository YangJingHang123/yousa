import yaml
from aiohttp import request

from utils import process_config, filter_dynamic, get_dynamic, headers

dynamic_keys_from_type = {
    1: ['item', 'content'],
    2: ['item', 'description'],
    4: ['item', 'content'],
    8: ['dynamic']
}


async def user_dynamic(user_id: str) -> dict:
    api_url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history'
    async with request("GET", api_url, headers=headers, params={'host_uid': user_id, 'visitor_id': "0", 'offset_dynamic_id': "0", "need_top": "1"}) as response:
        cards = (await response.json())['data']['cards']

        return [get_dynamic(card) for card in cards]


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
    async with request('GET', room_info_url, headers=headers, params={'room_id': room_id}) as resp:
        response = (await resp.json())
        if response['msg'] == 'ok':
            return response['data']['live_status'] == 1
        else:
            raise ValueError(str(response))


async def monitor_live(timestamp: int):
    config = yaml.safe_load(open('./bilibili.yaml', 'rb'))
    room_monitor_config = process_config(config['room_monitor'], 'room')
    live_room_ids = [room_id for room_id in room_monitor_config['room_ids'] if await room_status(room_id)]
    return {'live': live_room_ids}


async def monitor_dynamic(timestamp: int):
    config = yaml.safe_load(open('./bilibili.yaml', 'rb'))
    dynamic_monitor_config = process_config(config['user_monitor'], 'dynamic')
    new_dynamics = await user_new_dynamic(dynamic_monitor_config['user_ids'], timestamp)
    return {'dynamic': new_dynamics}
