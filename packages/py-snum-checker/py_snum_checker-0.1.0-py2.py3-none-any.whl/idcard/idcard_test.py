import pytest

from .checker import *

@pytest.mark.parametrize("data, expected", [
        ("5101081972", IDCardError.INVALID_LENGTH),  # 过短
        ("5101081972050521370", IDCardError.INVALID_LENGTH),  # 过长
        ("510108197205052137", True)
    ])
def test_length(data, expected):
    assert run(data) == expected


APP_KEY = "203748911"
APP_SECRET = "mbi6o6nlq4fnjqhbosamgzfvsiajjco1"
APP_CODE = "65827782610e49f8b9c9ec984b67f955"

@pytest.mark.parametrize("data, expected", [
        # (("苏渝", "510108197205052137"), True),
        (("苏渝", "510108197205052135"), IDCardError.DF_AUTH_FAIL),  # 身份证号不正确
        (("苏瑜", "510108197205052137"), IDCardError.DF_AUTH_FAIL)   # 姓名不正确
    ])
def test_format(data, expected):
    name, idcard = data
    assert double_factor(idcard, name, APP_CODE) == expected



#@pytest.mark.parametrize("data, expected", [
#        ("510108197205052137", True),
#        ("51010819720505ab37", IDCardError.INVALID_FORMAT),
#        ("51010819720505213x", IDCardError.INVALID_FORMAT),
#        ("51010819720505213X", IDCardError.INVALID_CHECKCODE),
#        ("510108197205052135", IDCardError.INVALID_CHECKCODE)
#    ])
