"""The module that defines the ``ImportIntoCourseData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class ImportIntoCourseData:
    """"""

    #: The id of the course from which you want to import.
    from_course_id: "int"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "from_course_id",
                rqa.SimpleValue.int,
                doc="The id of the course from which you want to import.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        res["from_course_id"] = to_dict(self.from_course_id)
        return res

    @classmethod
    def from_dict(
        cls: Type["ImportIntoCourseData"], d: Dict[str, Any]
    ) -> "ImportIntoCourseData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            from_course_id=parsed.from_course_id,
        )
        res.raw_data = d
        return res
