"""The module that defines the ``PatchSnippetCourseData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class PatchSnippetCourseData:
    """"""

    #: The new key of the snippet
    key: "str"
    #: The new value of the snippet
    value: "str"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "key",
                rqa.SimpleValue.str,
                doc="The new key of the snippet",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.SimpleValue.str,
                doc="The new value of the snippet",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        res["key"] = to_dict(self.key)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["PatchSnippetCourseData"], d: Dict[str, Any]
    ) -> "PatchSnippetCourseData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            key=parsed.key,
            value=parsed.value,
        )
        res.raw_data = d
        return res
