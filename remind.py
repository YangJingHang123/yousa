import datetime, re
from typing import Callable

class Message(object):

    def __init__(self):
        pass

# 中文描述的日期
_date_ch = r"[今明后]天"
# 中文描述的时段
_front_time_ch = r"([上中下]午)|(晚上)"
# 中文描述的时间
_time_ch = r"(\d{1,2}点)+(\d{1,2}分)?"

# 时间戳格式的日期
_date_ts = r"\d{1,2},\d{1,2}"
# 时间戳格式的时间
_time_ts = r"\d{1,2}:\d{1,2}"

# 日期
_date = r"(%s)|(%s)" % (_date_ch, _date_ts)
# 时间
_time = r"(%s)|(%s)" % (_time_ch, _time_ts)
# 时间格式检查
_re_check = r"(%s)? ?(%s)? ?(%s)" % (_date, _front_time_ch, _time)

_re_check       = re.compile(_re_check)

def check_set_time(set_time: str) -> bool:
    '''
    检查提取出来的 set_time 是否符合规范
    '''
    res = _re_check.match(set_time)
    if res and set_time == res.group(0):
        return True
    return False

def set_time_datetime(match_res: Callable) -> Callable:
    '''
    从匹配结果里提取出 datetime()
    '''
    pass


def parse_date(_date: str) -> Callable:
    '''
    将 _date_ch / _date_ts 形式的字符串转换成 datetime.date()
    '''
    pass

def parse_time(_time: str) -> Callable:
    '''
    将 _time_ch / _time_ts 形式的字符串转换成 datetime.time()
    '''
    pass

def msg_to_command(message: str) -> tuple:
    '''
    必须包含关键词: 提醒

    将自然语句, 处理成命令格式 (set_time:datetime(), item:str), 并返回
    命令语句一般是: 时间 + 提醒 + 事件
    eg: 
        今天下午三点提醒我取快递 -> (datetime(year, month, day, 15), "取快递")

    时间有: 今/明/后 天 + 上/下/中 午 (晚上) + *点*分 /
           上中下午/ 晚 + *点*分 /
           *点*分
    也可以直接是一个时间戳 2019.06.01 19:35 / 06.01 18:00 / 18:00
    '''
    msg = message.split('提醒')
    set_time = msg[0]
    item = msg[-1]
    return (set_time, item)

def parse_item(item: str) -> str:
    '''
    对 item 内容的提取
    '''
    if item[0] == '我':
        return item[1:]


# date = datetime.date(2019, 4, 5)
# time = datetime.time(19, 0)
# dt = datetime.datetime.combine(date, time)
# print(dt)

if __name__ == "__main__":
    front = input()
    print(check_set_time(front))
