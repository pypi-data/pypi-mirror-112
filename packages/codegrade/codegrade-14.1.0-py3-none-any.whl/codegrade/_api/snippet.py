"""The endpoints for snippet objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar, Union

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from typing import Sequence

    from ..client import AuthenticatedClient, _BaseClient
    from ..models.base_error import BaseError
    from ..models.snippet import Snippet
    from ..parsers import JsonResponseParser, ParserFor

_ClientT = TypeVar("_ClientT", bound="_BaseClient")


class SnippetService(Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def get_all(
        self: "SnippetService[AuthenticatedClient]",
        *,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[Snippet]":
        """Get all snippets of the current user.

        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: An array containing all snippets for the currently logged in
                  user.
        """
        from typing import Sequence

        from ..models.base_error import BaseError
        from ..models.snippet import Snippet
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/snippets/"
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(Snippet))
            ).try_parse(response)
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )
