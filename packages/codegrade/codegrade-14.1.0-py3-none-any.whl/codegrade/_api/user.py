"""The endpoints for user objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar, Union

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from typing import Any, Dict, Mapping, Sequence, Union, cast

    from cg_maybe import Maybe, Nothing
    from cg_maybe.utils import maybe_from_nullable
    from typing_extensions import Literal

    from ..client import AuthenticatedClient, _BaseClient
    from ..models.base_error import BaseError
    from ..models.extended_user import ExtendedUser
    from ..models.login_user_data import LoginUserData
    from ..models.patch_user_data import PatchUserData
    from ..models.register_user_data import RegisterUserData
    from ..models.result_data_post_user_login import ResultDataPostUserLogin
    from ..models.result_data_post_user_register import (
        ResultDataPostUserRegister,
    )
    from ..models.user import User
    from ..parsers import JsonResponseParser, ParserFor, make_union

_ClientT = TypeVar("_ClientT", bound="_BaseClient")


class UserService(Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def patch(
        self: "UserService[AuthenticatedClient]",
        json_body: Union[dict, list, "PatchUserData"],
        *,
        user_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ExtendedUser":
        """Update the attributes of a user.

        :param json_body: The body of the request. See :model:`.PatchUserData`
            for information about the possible fields. You can provide this
            data as a :model:`.PatchUserData` or as a dictionary.
        :param user_id: The id of the user you want to change. Currently this
            can only be your own user id.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The updated user.
        """
        from ..models.base_error import BaseError
        from ..models.extended_user import ExtendedUser
        from ..models.patch_user_data import PatchUserData
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/users/{userId}".format(userId=user_id)
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.patch(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(ParserFor.make(ExtendedUser)).try_parse(
                response
            )
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )

    def get(
        self: "UserService[AuthenticatedClient]",
        *,
        type: "Literal['roles', 'extended', 'default']" = "default",
        extended: "bool" = False,
        with_permissions: "bool" = False,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Union[ExtendedUser, User, Mapping[str, str]]":
        """Get the info of the currently logged in user.

        :param type: If this is `roles` a mapping between course\_id and role
            name will be returned, if this is `extended` an `ExtendedUser`
            instead of a `User` will be returned.
        :param extended: If `true` this has the same effect as setting `type`
            to `extended`.
        :param with_permissions: Setting this to true will add the key
            `permissions` to the user. The value will be a mapping indicating
            which global permissions this user has.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized user
        """
        from typing import Dict, Mapping, Union

        from typing_extensions import Literal

        from ..models.base_error import BaseError
        from ..models.extended_user import ExtendedUser
        from ..models.user import User
        from ..parsers import JsonResponseParser, ParserFor, make_union

        url = "/api/v1/login"
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
            "type": to_dict(type),
            "extended": to_dict(extended),
            "with_permissions": to_dict(with_permissions),
        }

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                make_union(
                    ParserFor.make(ExtendedUser),
                    ParserFor.make(User),
                    rqa.LookupMapping(rqa.SimpleValue.str),
                )
            ).try_parse(response)
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )

    def login(
        self,
        json_body: Union[dict, list, "LoginUserData"],
        *,
        with_permissions: "bool" = False,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ResultDataPostUserLogin":
        """Login using your username and password.

        `permissions` to the user. The value will be a mapping indicating which
        global permissions this user has.

        :param json_body: The body of the request. See :model:`.LoginUserData`
            for information about the possible fields. You can provide this
            data as a :model:`.LoginUserData` or as a dictionary.
        :param with_permissions: Return the global permissions of the newly
            logged in user.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized user
        """
        from typing import Dict

        from ..models.base_error import BaseError
        from ..models.login_user_data import LoginUserData
        from ..models.result_data_post_user_login import (
            ResultDataPostUserLogin,
        )
        from ..parsers import JsonResponseParser, ParserFor, make_union

        url = "/api/v1/login"
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
            "with_permissions": to_dict(with_permissions),
        }

        with self.__client as client:
            response = client.http.post(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(ResultDataPostUserLogin)
            ).try_parse(response)
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )

    def register(
        self,
        json_body: Union[dict, list, "RegisterUserData"],
        *,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ResultDataPostUserRegister":
        """Create a new user.

        :param json_body: The body of the request. See
            :model:`.RegisterUserData` for information about the possible
            fields. You can provide this data as a :model:`.RegisterUserData`
            or as a dictionary.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The registered user and an `access_token` that can be used to
                  perform requests as this new user.
        """
        from ..models.base_error import BaseError
        from ..models.register_user_data import RegisterUserData
        from ..models.result_data_post_user_register import (
            ResultDataPostUserRegister,
        )
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/user"
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.post(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(ResultDataPostUserRegister)
            ).try_parse(response)
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )

    def search(
        self: "UserService[AuthenticatedClient]",
        *,
        q: "str",
        exclude_course: Maybe["int"] = Nothing,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[User]":
        """Search for a user by name and username.

        :param q: The string to search for, all SQL wildcard are escaped and
                  spaces are replaced by wildcards.
        :param exclude_course: Exclude all users that are in the given course
            from the search results. You need the permission
            `can_list_course_users` on this course to use this parameter.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The users that match the given query string.
        """
        from typing import Any, Dict, Sequence, cast

        from cg_maybe import Maybe, Nothing
        from cg_maybe.utils import maybe_from_nullable

        from ..models.base_error import BaseError
        from ..models.user import User
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/users/"
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
            "q": to_dict(q),
        }
        maybe_from_nullable(cast(Any, exclude_course)).if_just(
            lambda val: params.__setitem__("exclude_course", val)
        )

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(User))
            ).try_parse(response)
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )
