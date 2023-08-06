"""The module that defines the ``ResultDataGetUserSettingGetAllUiPreferences`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..utils import to_dict


@dataclass
class ResultDataGetUserSettingGetAllUiPreferences:
    """"""

    rubric_editor_v2: Maybe["Optional[bool]"] = Nothing
    no_msg_for_mosaic_1: Maybe["Optional[bool]"] = Nothing
    no_msg_for_mosaic_2: Maybe["Optional[bool]"] = Nothing
    no_msg_for_mosaic_3: Maybe["Optional[bool]"] = Nothing
    no_msg_for_nobel: Maybe["Optional[bool]"] = Nothing
    no_msg_for_nobel_1: Maybe["Optional[bool]"] = Nothing
    no_msg_for_nobel_2: Maybe["Optional[bool]"] = Nothing
    no_msg_for_orchid: Maybe["Optional[bool]"] = Nothing
    no_msg_for_orchid_1: Maybe["Optional[bool]"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.OptionalArgument(
                "rubric_editor_v2",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_mosaic_1",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_mosaic_2",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_mosaic_3",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_nobel",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_nobel_1",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_nobel_2",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_orchid",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_orchid_1",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        self.rubric_editor_v2 = maybe_from_nullable(self.rubric_editor_v2)
        self.no_msg_for_mosaic_1 = maybe_from_nullable(
            self.no_msg_for_mosaic_1
        )
        self.no_msg_for_mosaic_2 = maybe_from_nullable(
            self.no_msg_for_mosaic_2
        )
        self.no_msg_for_mosaic_3 = maybe_from_nullable(
            self.no_msg_for_mosaic_3
        )
        self.no_msg_for_nobel = maybe_from_nullable(self.no_msg_for_nobel)
        self.no_msg_for_nobel_1 = maybe_from_nullable(self.no_msg_for_nobel_1)
        self.no_msg_for_nobel_2 = maybe_from_nullable(self.no_msg_for_nobel_2)
        self.no_msg_for_orchid = maybe_from_nullable(self.no_msg_for_orchid)
        self.no_msg_for_orchid_1 = maybe_from_nullable(
            self.no_msg_for_orchid_1
        )

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        if self.rubric_editor_v2.is_just:
            res["rubric_editor_v2"] = to_dict(self.rubric_editor_v2.value)
        if self.no_msg_for_mosaic_1.is_just:
            res["no_msg_for_mosaic_1"] = to_dict(
                self.no_msg_for_mosaic_1.value
            )
        if self.no_msg_for_mosaic_2.is_just:
            res["no_msg_for_mosaic_2"] = to_dict(
                self.no_msg_for_mosaic_2.value
            )
        if self.no_msg_for_mosaic_3.is_just:
            res["no_msg_for_mosaic_3"] = to_dict(
                self.no_msg_for_mosaic_3.value
            )
        if self.no_msg_for_nobel.is_just:
            res["no_msg_for_nobel"] = to_dict(self.no_msg_for_nobel.value)
        if self.no_msg_for_nobel_1.is_just:
            res["no_msg_for_nobel_1"] = to_dict(self.no_msg_for_nobel_1.value)
        if self.no_msg_for_nobel_2.is_just:
            res["no_msg_for_nobel_2"] = to_dict(self.no_msg_for_nobel_2.value)
        if self.no_msg_for_orchid.is_just:
            res["no_msg_for_orchid"] = to_dict(self.no_msg_for_orchid.value)
        if self.no_msg_for_orchid_1.is_just:
            res["no_msg_for_orchid_1"] = to_dict(
                self.no_msg_for_orchid_1.value
            )
        return res

    @classmethod
    def from_dict(
        cls: Type["ResultDataGetUserSettingGetAllUiPreferences"],
        d: Dict[str, Any],
    ) -> "ResultDataGetUserSettingGetAllUiPreferences":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            rubric_editor_v2=parsed.rubric_editor_v2,
            no_msg_for_mosaic_1=parsed.no_msg_for_mosaic_1,
            no_msg_for_mosaic_2=parsed.no_msg_for_mosaic_2,
            no_msg_for_mosaic_3=parsed.no_msg_for_mosaic_3,
            no_msg_for_nobel=parsed.no_msg_for_nobel,
            no_msg_for_nobel_1=parsed.no_msg_for_nobel_1,
            no_msg_for_nobel_2=parsed.no_msg_for_nobel_2,
            no_msg_for_orchid=parsed.no_msg_for_orchid,
            no_msg_for_orchid_1=parsed.no_msg_for_orchid_1,
        )
        res.raw_data = d
        return res
