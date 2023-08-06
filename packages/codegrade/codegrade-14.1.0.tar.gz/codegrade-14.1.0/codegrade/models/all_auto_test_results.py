"""The module that defines the ``AllAutoTestResults`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .auto_test_result_with_extra_data import AutoTestResultWithExtraData


@dataclass
class AllAutoTestResults:
    """The result when requesting all non started AutoTest results."""

    #: The total amount of not started AutoTest results
    total_amount: "int"
    #: The request results, these are limited by the given query parameters.
    results: "Sequence[AutoTestResultWithExtraData]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "total_amount",
                rqa.SimpleValue.int,
                doc="The total amount of not started AutoTest results",
            ),
            rqa.RequiredArgument(
                "results",
                rqa.List(ParserFor.make(AutoTestResultWithExtraData)),
                doc=(
                    "The request results, these are limited by the given query"
                    " parameters."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        res["total_amount"] = to_dict(self.total_amount)
        res["results"] = to_dict(self.results)
        return res

    @classmethod
    def from_dict(
        cls: Type["AllAutoTestResults"], d: Dict[str, Any]
    ) -> "AllAutoTestResults":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            total_amount=parsed.total_amount,
            results=parsed.results,
        )
        res.raw_data = d
        return res
