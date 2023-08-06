"""The module that defines the ``IOTestLog`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .auto_test_step_log_base import AutoTestStepLogBase
from .io_test_step_log import IOTestStepLog


@dataclass
class IOTestLog(AutoTestStepLogBase):
    """The log type of an IO test."""

    #: The log for each step of the io test.
    steps: "Sequence[IOTestStepLog]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: AutoTestStepLogBase.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "steps",
                    rqa.List(ParserFor.make(IOTestStepLog)),
                    doc="The log for each step of the io test.",
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        res["steps"] = to_dict(self.steps)
        return res

    @classmethod
    def from_dict(cls: Type["IOTestLog"], d: Dict[str, Any]) -> "IOTestLog":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            steps=parsed.steps,
        )
        res.raw_data = d
        return res
