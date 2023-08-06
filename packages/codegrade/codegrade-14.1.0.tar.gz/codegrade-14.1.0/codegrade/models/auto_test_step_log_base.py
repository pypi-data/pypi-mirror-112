"""The module that defines the ``AutoTestStepLogBase`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class AutoTestStepLogBase:
    """The base AutoTestStep log for every step type.

    This is also the type of the log when the test hasn't been started yet.
    """

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping().use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestStepLogBase"], d: Dict[str, Any]
    ) -> "AutoTestStepLogBase":
        parsed = cls.data_parser.try_parse(d)

        res = cls()
        res.raw_data = d
        return res
