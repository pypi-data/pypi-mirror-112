# -*- coding: utf-8 -*-
# @author: leesoar

"""base.py"""

import random
import socket
import struct
import time
from collections import Iterable


__all__ = ["extract", "random_ip", "sleep", ]


def extract(container, offset=0, *, default=None, max_extract=1):
    """安全的取值或切片

    Args:
        container: 容器对象。如list, tuple，同样支持str
        offset: 偏移量，支持int, list, tuple。默认为0
        default: 取失败默认返回None
        max_extract: 最大提取次数
    """
    try:
        if not isinstance(container, str) and isinstance(container, Iterable):
            container = list(container)

        if isinstance(offset, (tuple, list)):
            ret = container[offset[0]: offset[-1]]
        else:
            ret = container[offset]

        if max_extract > 1:
            max_extract -= 1
            return extract(ret, offset, default=default, max_extract=max_extract)
        return ret
    except (IndexError, TypeError):
        return default


def sleep(*rg, max_):
    """阻塞程序

    Args:
        rg: 阻塞时间范围(sec, sec)
        max_: 最大阻塞时间(sec)
    """
    if len(rg) == 1:
        time.sleep(*rg)
    else:
        time.sleep(min(random.uniform(*rg), max_))


def random_ip():
    """随机返回一个ip"""
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

