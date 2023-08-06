"""The endpoints for user_setting objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar, Union

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from typing import Any, Dict, Optional, cast

    from cg_maybe import Maybe, Nothing
    from cg_maybe.utils import maybe_from_nullable

    from ..client import AuthenticatedClient, _BaseClient
    from ..models.base_error import BaseError
    from ..models.notification_setting import NotificationSetting
    from ..models.patch_notification_setting_user_setting_data import (
        PatchNotificationSettingUserSettingData,
    )
    from ..models.patch_ui_preference_user_setting_data import (
        PatchUiPreferenceUserSettingData,
    )
    from ..models.result_data_get_user_setting_get_all_ui_preferences import (
        ResultDataGetUserSettingGetAllUiPreferences,
    )
    from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

_ClientT = TypeVar("_ClientT", bound="_BaseClient")


class UserSettingService(Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def get_all_notification_settings(
        self,
        *,
        token: Maybe["str"] = Nothing,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "NotificationSetting":
        """Update preferences for notifications.

        :param token: The token with which you want to get the preferences, if
            not given the preferences are retrieved for the currently logged in
            user.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The preferences for the user as described by the `token`.
        """
        from typing import Any, Dict, cast

        from cg_maybe import Maybe, Nothing
        from cg_maybe.utils import maybe_from_nullable

        from ..models.base_error import BaseError
        from ..models.notification_setting import NotificationSetting
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/settings/notification_settings/"
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
        }
        maybe_from_nullable(cast(Any, token)).if_just(
            lambda val: params.__setitem__("token", val)
        )

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(NotificationSetting)
            ).try_parse(response)
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )

    def patch_notification_setting(
        self,
        json_body: Union[
            dict, list, "PatchNotificationSettingUserSettingData"
        ],
        *,
        token: Maybe["str"] = Nothing,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "None":
        """Update preferences for notifications.

        :param json_body: The body of the request. See
            :model:`.PatchNotificationSettingUserSettingData` for information
            about the possible fields. You can provide this data as a
            :model:`.PatchNotificationSettingUserSettingData` or as a
            dictionary.
        :param token: The token with which you want to update the preferences,
            if not given the preferences are updated for the currently logged
            in user.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing.
        """
        from typing import Any, Dict, cast

        from cg_maybe import Maybe, Nothing
        from cg_maybe.utils import maybe_from_nullable

        from ..models.base_error import BaseError
        from ..models.patch_notification_setting_user_setting_data import (
            PatchNotificationSettingUserSettingData,
        )
        from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

        url = "/api/v1/settings/notification_settings/"
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
        }
        maybe_from_nullable(cast(Any, token)).if_just(
            lambda val: params.__setitem__("token", val)
        )

        with self.__client as client:
            response = client.http.patch(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )

    def get_ui_preference(
        self,
        *,
        name: "str",
        token: Maybe["str"] = Nothing,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Optional[bool]":
        """Get a single UI preferences.

        :param name: The preference name you want to get.
        :param token: The token with which you want to get the preferences, if
            not given the preferences are retrieved for the currently logged in
            user.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The preferences for the user as described by the `token`.
        """
        from typing import Any, Dict, Optional, cast

        from cg_maybe import Maybe, Nothing
        from cg_maybe.utils import maybe_from_nullable

        from ..models.base_error import BaseError
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/settings/ui_preferences/{name}".format(name=name)
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
        }
        maybe_from_nullable(cast(Any, token)).if_just(
            lambda val: params.__setitem__("token", val)
        )

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.Nullable(rqa.SimpleValue.bool)
            ).try_parse(response)
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )

    def get_all_ui_preferences(
        self,
        *,
        token: Maybe["str"] = Nothing,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ResultDataGetUserSettingGetAllUiPreferences":
        """Get ui preferences.

        :param token: The token with which you want to get the preferences, if
            not given the preferences are retrieved for the currently logged in
            user.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The preferences for the user as described by the `token`.
        """
        from typing import Any, Dict, cast

        from cg_maybe import Maybe, Nothing
        from cg_maybe.utils import maybe_from_nullable

        from ..models.base_error import BaseError
        from ..models.result_data_get_user_setting_get_all_ui_preferences import (
            ResultDataGetUserSettingGetAllUiPreferences,
        )
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/settings/ui_preferences/"
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
        }
        maybe_from_nullable(cast(Any, token)).if_just(
            lambda val: params.__setitem__("token", val)
        )

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(ResultDataGetUserSettingGetAllUiPreferences)
            ).try_parse(response)
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )

    def patch_ui_preference(
        self,
        json_body: Union[dict, list, "PatchUiPreferenceUserSettingData"],
        *,
        token: Maybe["str"] = Nothing,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "None":
        """Update ui preferences.

        :param json_body: The body of the request. See
            :model:`.PatchUiPreferenceUserSettingData` for information about
            the possible fields. You can provide this data as a
            :model:`.PatchUiPreferenceUserSettingData` or as a dictionary.
        :param token: The token with which you want to update the preferences,
            if not given the preferences are updated for the currently logged
            in user.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing.
        """
        from typing import Any, Dict, cast

        from cg_maybe import Maybe, Nothing
        from cg_maybe.utils import maybe_from_nullable

        from ..models.base_error import BaseError
        from ..models.patch_ui_preference_user_setting_data import (
            PatchUiPreferenceUserSettingData,
        )
        from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

        url = "/api/v1/settings/ui_preferences/"
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
        }
        maybe_from_nullable(cast(Any, token)).if_just(
            lambda val: params.__setitem__("token", val)
        )

        with self.__client as client:
            response = client.http.patch(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )
