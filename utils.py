from dynamic import Dynamic

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'}


def process_config(configs, type):
    resp = dict()
    _id = 'user_id' if type == 'dynamic' else 'room_id'
    _ids = 'user_ids' if type == 'dynamic' else 'room_ids'
    resp[_ids] = list()
    for config in configs:
        resp.update({config[_id]: config})
        resp[_ids].append(config[_id])
    return resp


def filter_dynamic(items: list, timestamp: int):
    return [item for item in items if item.timestamp > timestamp]


def get_value(obj: dict, keys: list):
    for key in keys:
        obj = obj[key]
    return obj


def get_dynamic(card: dict):
    _dynamic = Dynamic(card)
    return _dynamic
