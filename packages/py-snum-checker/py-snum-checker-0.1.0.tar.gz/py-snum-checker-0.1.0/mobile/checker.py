"""手机号码检查包

1. 格式是否正确
"""

import re
from enum import Enum


class MobileError(Enum):
    """电话号码错误类型枚举"""
    INVALID = 1


def run(mobile:str):
    """检查号码是否符合正则规定"""
    if re.match(r"^1\d{10}$", mobile) is None:
        return MobileError.INVALID

    return True
