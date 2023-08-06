"""身份证号码检查包

1. 身份证号检查。
2. 身份证与姓名双因子验证。
3. Todo 身份证、姓名、人脸三因子验证。
"""

from enum import Enum
import httpx


IDCARD_LENGTH = 18


class IDCardError(Enum):
    """身份证号检查错误枚举"""
    INVALID_LENGTH = 1
    INVALID_FORMAT = 2
    INVALID_CHECKCODE = 3
    DF_AUTH_FAIL = 4


def run(idcard:str):
    """合法性检查

    1. 长度不匹配。
    2. Todo 校验码不合格。
    """
    if len(idcard) != IDCARD_LENGTH:
        return IDCardError.INVALID_LENGTH
    return True


def double_factor(idcard:str, name:str, appcode:str):
    """公安部双因子认证

    1. 身份证号。
    2. 姓名。
    """
    url = "https://idenauthen.market.alicloudapi.com/idenAuthentication"
    headers = {"Authorization": "APPCODE " + appcode}
    response = httpx.post(url, headers=headers, data={"idNo": idcard, "name": name})
    val = response.json()

    if val["respCode"] != "0000":
        return IDCardError.DF_AUTH_FAIL
    return True
