"""The module that defines the ``AutoTestResultWithExtraData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict
from .auto_test_result import AutoTestResult


@dataclass
class AutoTestResultWithExtraData(AutoTestResult):
    """An `AutoTestResults` with an assignment and course id."""

    #: The assignment id of this result.
    assignment_id: "int"
    #: The course id of this result.
    course_id: "int"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: AutoTestResult.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "assignment_id",
                    rqa.SimpleValue.int,
                    doc="The assignment id of this result.",
                ),
                rqa.RequiredArgument(
                    "course_id",
                    rqa.SimpleValue.int,
                    doc="The course id of this result.",
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        res["assignment_id"] = to_dict(self.assignment_id)
        res["course_id"] = to_dict(self.course_id)
        res["id"] = to_dict(self.id)
        res["created_at"] = to_dict(self.created_at)
        res["updated_at"] = to_dict(self.updated_at)
        res["started_at"] = to_dict(self.started_at)
        res["work_id"] = to_dict(self.work_id)
        res["state"] = to_dict(self.state)
        res["points_achieved"] = to_dict(self.points_achieved)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestResultWithExtraData"], d: Dict[str, Any]
    ) -> "AutoTestResultWithExtraData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            assignment_id=parsed.assignment_id,
            course_id=parsed.course_id,
            id=parsed.id,
            created_at=parsed.created_at,
            updated_at=parsed.updated_at,
            started_at=parsed.started_at,
            work_id=parsed.work_id,
            state=parsed.state,
            points_achieved=parsed.points_achieved,
        )
        res.raw_data = d
        return res
