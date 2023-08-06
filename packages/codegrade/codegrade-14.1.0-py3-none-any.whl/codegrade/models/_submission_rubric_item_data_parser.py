"""The module that defines the ``_SubmissionRubricItemDataParser`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class _SubmissionRubricItemDataParser:
    """A single rubric item to select."""

    #: The id of the row the item is in.
    row_id: "int"
    #: The id of the item to select.
    item_id: "int"
    #: The multiplier you want to use for this rubric item. This value defaults
    #: to 1.0, and can only be something other than 1.0 for rubric rows with
    #: type 'continuous'.
    multiplier: "float" = 1.0

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "row_id",
                rqa.SimpleValue.int,
                doc="The id of the row the item is in.",
            ),
            rqa.RequiredArgument(
                "item_id",
                rqa.SimpleValue.int,
                doc="The id of the item to select.",
            ),
            rqa.DefaultArgument(
                "multiplier",
                rqa.SimpleValue.float,
                doc=(
                    "The multiplier you want to use for this rubric item. This"
                    " value defaults to 1.0, and can only be something other"
                    " than 1.0 for rubric rows with type 'continuous'."
                ),
                default=lambda: 1.0,
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        res["row_id"] = to_dict(self.row_id)
        res["item_id"] = to_dict(self.item_id)
        res["multiplier"] = to_dict(self.multiplier)
        return res

    @classmethod
    def from_dict(
        cls: Type["_SubmissionRubricItemDataParser"], d: Dict[str, Any]
    ) -> "_SubmissionRubricItemDataParser":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            row_id=parsed.row_id,
            item_id=parsed.item_id,
            multiplier=parsed.multiplier,
        )
        res.raw_data = d
        return res
