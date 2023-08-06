"""The module that defines the ``PatchSubmissionData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..utils import to_dict


@dataclass
class PatchSubmissionData:
    """"""

    #: General feedback on the submission.
    feedback: Maybe["Optional[str]"] = Nothing
    #: The grade of the submission.
    grade: Maybe["Optional[float]"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.OptionalArgument(
                "feedback",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="General feedback on the submission.",
            ),
            rqa.OptionalArgument(
                "grade",
                rqa.Nullable(rqa.SimpleValue.float),
                doc="The grade of the submission.",
            ),
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        self.feedback = maybe_from_nullable(self.feedback)
        self.grade = maybe_from_nullable(self.grade)

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        if self.feedback.is_just:
            res["feedback"] = to_dict(self.feedback.value)
        if self.grade.is_just:
            res["grade"] = to_dict(self.grade.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["PatchSubmissionData"], d: Dict[str, Any]
    ) -> "PatchSubmissionData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            feedback=parsed.feedback,
            grade=parsed.grade,
        )
        res.raw_data = d
        return res
