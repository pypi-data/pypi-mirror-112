"""The endpoints for file objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar, Union

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from typing import Any, Dict, cast

    from cg_maybe import Maybe, Nothing
    from cg_maybe.utils import maybe_from_nullable

    from ..client import AuthenticatedClient, _BaseClient
    from ..models.base_error import BaseError
    from ..parsers import JsonResponseParser, ParserFor, ResponsePropertyParser

_ClientT = TypeVar("_ClientT", bound="_BaseClient")


class FileService(Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def download(
        self,
        *,
        filename: "str",
        mime: Maybe["str"] = Nothing,
        as_attachment: "bool" = False,
        name: Maybe["str"] = Nothing,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "bytes":
        """Serve some specific file in the uploads folder.

        Warning: The file will be deleted after you download it!

        :param filename: The filename of the file to get.
        :param mime: The mime type header to set on the response.
        :param as_attachment: If truthy the response will have a
            `Content-Disposition: attachment` header set.
        :param name: The filename for the attachment, defaults to the second
            part of the url.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The requested file.
        """
        from typing import Any, Dict, cast

        from cg_maybe import Maybe, Nothing
        from cg_maybe.utils import maybe_from_nullable

        from ..models.base_error import BaseError
        from ..parsers import (
            JsonResponseParser,
            ParserFor,
            ResponsePropertyParser,
        )

        url = "/api/v1/files/{filename}".format(filename=filename)
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
            "as_attachment": to_dict(as_attachment),
        }
        maybe_from_nullable(cast(Any, mime)).if_just(
            lambda val: params.__setitem__("mime", val)
        )
        maybe_from_nullable(cast(Any, name)).if_just(
            lambda val: params.__setitem__("name", val)
        )

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return ResponsePropertyParser("content", bytes).try_parse(response)
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )
