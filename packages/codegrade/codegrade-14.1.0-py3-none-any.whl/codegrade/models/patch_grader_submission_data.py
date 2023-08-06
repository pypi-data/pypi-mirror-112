"""The module that defines the ``PatchGraderSubmissionData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class PatchGraderSubmissionData:
    """"""

    #: Id of the new grader.
    user_id: "int"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "user_id",
                rqa.SimpleValue.int,
                doc="Id of the new grader.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        res["user_id"] = to_dict(self.user_id)
        return res

    @classmethod
    def from_dict(
        cls: Type["PatchGraderSubmissionData"], d: Dict[str, Any]
    ) -> "PatchGraderSubmissionData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            user_id=parsed.user_id,
        )
        res.raw_data = d
        return res
