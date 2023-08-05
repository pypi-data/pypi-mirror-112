from typing import Optional

from .base_args import BaseArgs


class NineNineArgs(BaseArgs):
    """
    9.9元商品API：返回购买价格≤9.9元的商品列表，返回佣金≥15%，动态描述分≥4.6的商品列表。

    :doc https://www.zhetaoke.com/user/extend/extend_lingquan_jiu.aspx
    """

    @staticmethod
    def base_url():
        return "https://api.zhetaoke.com:10001/api/api_all.ashx"

    page: int = 1
    page_size: int = 20
    sort: str = "new"
    cid: Optional[int] = None

    #  券后价价格区间，
    #  值为空：全部商品，0.0-9.9：9.9元商品，0.0-19.9：19.9元商品
    price: str = "0.0-9.9"
