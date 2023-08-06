"""The module that defines the ``AssignmentLoginLink`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .assignment import Assignment
from .user import User


@dataclass
class AssignmentLoginLink:
    """The way this class will be represented in JSON."""

    #: The id of this link.
    id: "str"
    #: The assignment connected to this login link.
    assignment: "Assignment"
    #: The user that is link will login.
    user: "User"
    #: The amount of seconds until the exam starts.
    time_to_start: "Optional[float]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.str,
                doc="The id of this link.",
            ),
            rqa.RequiredArgument(
                "assignment",
                ParserFor.make(Assignment),
                doc="The assignment connected to this login link.",
            ),
            rqa.RequiredArgument(
                "user",
                ParserFor.make(User),
                doc="The user that is link will login.",
            ),
            rqa.RequiredArgument(
                "time_to_start",
                rqa.Nullable(rqa.SimpleValue.float),
                doc="The amount of seconds until the exam starts.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        res["id"] = to_dict(self.id)
        res["assignment"] = to_dict(self.assignment)
        res["user"] = to_dict(self.user)
        res["time_to_start"] = to_dict(self.time_to_start)
        return res

    @classmethod
    def from_dict(
        cls: Type["AssignmentLoginLink"], d: Dict[str, Any]
    ) -> "AssignmentLoginLink":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            assignment=parsed.assignment,
            user=parsed.user,
            time_to_start=parsed.time_to_start,
        )
        res.raw_data = d
        return res
