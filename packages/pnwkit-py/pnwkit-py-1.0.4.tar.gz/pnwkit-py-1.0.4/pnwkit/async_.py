from __future__ import annotations

from typing import Any, Dict, Mapping, Optional, Sequence, Tuple, Union

import aiohttp

from .abc import KitBase
from .data import (
    Alliance,
    Color,
    Data,
    Nation,
    PaginatorInfo,
    Trade,
    Tradeprice,
    Treasure,
    War,
)
from .errors import GraphQLError
from .paginator import AlliancePaginator, NationPaginator, Paginator


class AsyncKit(KitBase):
    async def _query(
        self: AsyncKit,
        endpoint: str,
        params: Union[str, Mapping[str, Any]],
        args: Union[str, Sequence[str]],
        *,
        is_paginator: bool = False,
    ) -> Dict[str, Any]:
        query = query = self._format_query(endpoint, params, args, is_paginator)
        async with aiohttp.request(
            "GET", self.graphql_url(), json={"query": query}
        ) as response:
            response = await response.json()
            try:
                if "errors" in response[0]:
                    error = (
                        "\n".join(i["message"] for i in response[0]["errors"])
                        if len(response[0]["errors"]) > 1
                        else response[0]["errors"][0]["message"]
                    )
                    raise GraphQLError(error)
            except KeyError:
                pass
            try:
                if "errors" in response:
                    error = (
                        "\n".join(i["message"] for i in response["errors"])
                        if len(response["errors"]) > 1
                        else response["errors"][0]["message"]
                    )
                    raise GraphQLError(error)
            except KeyError:
                pass
            return response

    async def _data_query(
        self: AsyncKit,
        endpoint: str,
        params: Union[str, Mapping[str, Any]],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        is_paginator: bool = False,
        type_: Data,
        paginator_type: Optional[Paginator] = None,
        **kwargs: Any,
    ) -> Union[Tuple[Data], Paginator]:
        args = (arg, *args)
        params = params or kwargs
        if "first" not in params and endpoint in {"alliance", "nations"}:
            params["first"] = 5
        response = await self._query(
            endpoint, params, args, is_paginator=is_paginator
        )
        if is_paginator and paginator_type:
            data: Tuple[type_] = tuple(
                type_(i) for i in response["data"][endpoint]["data"]
            )
            if paginator:
                return paginator_type(
                    data, PaginatorInfo(response["data"][endpoint]["paginatorInfo"])
                )
            return data
        data: Tuple[type_] = tuple(type_(i) for i in response["data"][endpoint])
        return data

    async def alliance_query(
        self: AsyncKit,
        params: Union[str, Mapping[str, Any]],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **kwargs: Any,
    ) -> Union[Tuple[Alliance], AlliancePaginator]:
        return await self._data_query(
            "alliances",
            params,
            arg,
            *args,
            **kwargs,
            type_=Alliance,
            paginator=paginator,
            is_paginator=True,
            paginator_type=AlliancePaginator,
        )

    async def color_query(
        self: AsyncKit,
        params: Union[str, Mapping[str, Any]],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        **kwargs: Any,
    ) -> Tuple[Color]:
        return await self._data_query(
            "colors",
            params,
            arg,
            *args,
            **kwargs,
            type_=Color,
        )

    async def nation_query(
        self: KitBase,
        params: Union[str, Mapping[str, Any]],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **kwargs: Any,
    ) -> Union[Tuple[Nation], NationPaginator]:
        return await self._data_query(
            "nations",
            params,
            arg,
            *args,
            **kwargs,
            type_=Nation,
            paginator=paginator,
            is_paginator=True,
            paginator_type=NationPaginator,
        )

    async def trade_query(
        self: AsyncKit,
        params: Union[str, Mapping[str, Any]],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        **kwargs: Any,
    ) -> Tuple[Trade]:
        return await self._data_query(
            "trades",
            params,
            arg,
            *args,
            **kwargs,
            type_=Trade,
        )

    async def trade_price_query(
        self: AsyncKit,
        params: Union[str, Mapping[str, Any]],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        **kwargs: Any,
    ) -> Tuple[Tradeprice]:
        return await self._data_query(
            "tradeprices",
            params,
            arg,
            *args,
            **kwargs,
            type_=Tradeprice,
        )

    async def treasure_query(
        self: AsyncKit,
        params: Union[str, Mapping[str, Any]],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        **kwargs: Any,
    ) -> Tuple[Treasure]:
        return await self._data_query(
            "treasures",
            params,
            arg,
            *args,
            **kwargs,
            type_=Treasure,
        )

    async def war_query(
        self: AsyncKit,
        params: Union[str, Mapping[str, Any]],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        **kwargs: Any,
    ) -> Tuple[War]:
        return await self._data_query(
            "wars",
            params,
            arg,
            *args,
            **kwargs,
            type_=War,
        )
