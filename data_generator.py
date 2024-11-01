# -*- coding: utf-8 -*-
# @Time    : 2024/10/29 15:47
# @Author  : tangjie.zheng
# @File    : data_generator.py
# @Software: PyCharm2024
import random
import string
import datetime

# 随机字符串生成函数
def generate_random_string(min_len: int, max_len: int) -> str:
    length = random.randint(min_len, max_len)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# 随机日期生成函数
def generate_random_date(start_date: datetime.date, end_date: datetime.date) -> datetime.date:
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    return start_date + datetime.timedelta(days=random_days)

# 随机TIMESTAMP生成函数
def generate_random_timestamp(start_date: datetime.date, end_date: datetime.date) -> datetime.datetime:
    start_datetime = datetime.datetime.combine(start_date, datetime.time(0, 0, 0))
    end_datetime = datetime.datetime.combine(end_date, datetime.time(23, 59, 59))
    delta = end_datetime - start_datetime
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start_datetime + datetime.timedelta(seconds=random_seconds)

# 随机浮点数生成函数
def generate_random_float(min_value: float = 0.0, max_value: float = 100.0, decimal_places: int = 2) -> float:
    return round(random.uniform(min_value, max_value), decimal_places)

# 随机字节数据生成函数（用于BLOB）
def generate_random_blob(size: int = 8) -> bytes:
    return bytes(random.getrandbits(8) for _ in range(size))

def blob_to_hex_string(blob: bytes) -> str:
    return blob.hex()

# 随机CLOB内容生成函数（仅包含英文和数字）
def generate_random_clob(min_len: int, max_len: int) -> str:
    length = random.randint(min_len, max_len)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))