import pytest

from .checker import *

@pytest.mark.parametrize("data, expected", [
        ("189", MobileError.INVALID),  # 过短
        ("130112356890", MobileError.INVALID),  # 过长
        ("57811235689", MobileError.INVALID),  # 不正确的格式
        ("187123456xy", MobileError.INVALID),  # 不正确的格式
        ("18980473365", True)
    ])
def test_length(data, expected):
    assert run(data) == expected

