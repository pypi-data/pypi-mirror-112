"""The module that defines the ``ExtendedUser`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..parsers import ParserFor
from ..utils import to_dict
from .global_perm_map import GlobalPermMap
from .user import User


@dataclass
class ExtendedUser(User):
    """The extended JSON representation of a user."""

    #: The email of the user. This will only be provided for the currently
    #: logged in user.
    email: "str"
    #: Can this user see hidden assignments at least in one course.
    hidden: "bool"
    #: The permissions of the user. This will only be present if requested.
    permissions: Maybe["GlobalPermMap"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: User.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "email",
                    rqa.SimpleValue.str,
                    doc=(
                        "The email of the user. This will only be provided for"
                        " the currently logged in user."
                    ),
                ),
                rqa.RequiredArgument(
                    "hidden",
                    rqa.SimpleValue.bool,
                    doc=(
                        "Can this user see hidden assignments at least in one"
                        " course."
                    ),
                ),
                rqa.OptionalArgument(
                    "permissions",
                    ParserFor.make(GlobalPermMap),
                    doc=(
                        "The permissions of the user. This will only be"
                        " present if requested."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        getattr(super(), "__post_init__", lambda: None)()
        self.permissions = maybe_from_nullable(self.permissions)

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        res["email"] = to_dict(self.email)
        res["hidden"] = to_dict(self.hidden)
        res["group"] = to_dict(self.group)
        res["id"] = to_dict(self.id)
        res["name"] = to_dict(self.name)
        res["username"] = to_dict(self.username)
        res["is_test_student"] = to_dict(self.is_test_student)
        res["tenant_id"] = to_dict(self.tenant_id)
        if self.permissions.is_just:
            res["permissions"] = to_dict(self.permissions.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["ExtendedUser"], d: Dict[str, Any]
    ) -> "ExtendedUser":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            email=parsed.email,
            hidden=parsed.hidden,
            group=parsed.group,
            id=parsed.id,
            name=parsed.name,
            username=parsed.username,
            is_test_student=parsed.is_test_student,
            tenant_id=parsed.tenant_id,
            permissions=parsed.permissions,
        )
        res.raw_data = d
        return res
