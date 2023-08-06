"""The module that defines the ``AutoTestRunner`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .auto_test_runner_state import AutoTestRunnerState


@dataclass
class AutoTestRunner:
    """A runner as JSON."""

    #: The current state of the runner
    state: "AutoTestRunnerState"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "state",
                rqa.EnumValue(AutoTestRunnerState),
                doc="The current state of the runner",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        res["state"] = to_dict(self.state)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestRunner"], d: Dict[str, Any]
    ) -> "AutoTestRunner":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            state=parsed.state,
        )
        res.raw_data = d
        return res
