"""
Copyright(C),2017-2022,宁静之盾

Summary: 工具类

Description:

Example:

2022/5/24, 邹辉,
"""
import time

from uuid import uuid4


def gen_uuid_str():
    """
    获取uuid
    :return: uuid
    """
    return uuid4().hex


def get_current_timestamp():
    """
    获取当前时间戳
    :return: 当前时间戳
    """
    return int(round(time.time() * 1000))
