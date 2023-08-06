from PyPlcnextRsc.common.types import RscTpEnum

__all__ = ["RscStringEncoding"]


class RscStringEncoding(RscTpEnum):
    Null = 0,
    Ansi = 1,
    Utf8 = 2,
    Utf16 = 3
