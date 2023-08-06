"""The module that defines the ``UpdatePeerFeedbackSettingsAssignmentData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type, Union

import cg_request_args as rqa

from ..parsers import make_union
from ..utils import to_dict


@dataclass
class UpdatePeerFeedbackSettingsAssignmentData:
    """"""

    #: The amount of subjects a single reviewer should give peer feedback on.
    amount: "int"
    #: The amount of time in seconds that a user has to give peer feedback
    #: after the deadline has expired.
    time: "Optional[Union[int, str]]"
    #: Should peer feedback comments by default be approved.
    auto_approved: "bool"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "amount",
                rqa.SimpleValue.int,
                doc=(
                    "The amount of subjects a single reviewer should give peer"
                    " feedback on."
                ),
            ),
            rqa.RequiredArgument(
                "time",
                rqa.Nullable(
                    make_union(rqa.SimpleValue.int, rqa.SimpleValue.str)
                ),
                doc=(
                    "The amount of time in seconds that a user has to give"
                    " peer feedback after the deadline has expired."
                ),
            ),
            rqa.RequiredArgument(
                "auto_approved",
                rqa.SimpleValue.bool,
                doc="Should peer feedback comments by default be approved.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        res["amount"] = to_dict(self.amount)
        res["time"] = to_dict(self.time)
        res["auto_approved"] = to_dict(self.auto_approved)
        return res

    @classmethod
    def from_dict(
        cls: Type["UpdatePeerFeedbackSettingsAssignmentData"],
        d: Dict[str, Any],
    ) -> "UpdatePeerFeedbackSettingsAssignmentData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            amount=parsed.amount,
            time=parsed.time,
            auto_approved=parsed.auto_approved,
        )
        res.raw_data = d
        return res
