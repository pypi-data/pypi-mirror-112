"""The endpoints for submission objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar, Union

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from typing import Dict, Mapping, Sequence, Union

    from typing_extensions import Literal

    from ..client import AuthenticatedClient, _BaseClient
    from ..models.base_error import BaseError
    from ..models.extended_work import ExtendedWork
    from ..models.feedback_with_replies import FeedbackWithReplies
    from ..models.feedback_without_replies import FeedbackWithoutReplies
    from ..models.grade_history import GradeHistory
    from ..models.patch_grader_submission_data import PatchGraderSubmissionData
    from ..models.patch_rubric_result_submission_data import (
        PatchRubricResultSubmissionData,
    )
    from ..models.patch_submission_data import PatchSubmissionData
    from ..models.work_rubric_result_as_json import WorkRubricResultAsJSON
    from ..parsers import (
        ConstantlyParser,
        JsonResponseParser,
        ParserFor,
        make_union,
    )

_ClientT = TypeVar("_ClientT", bound="_BaseClient")


class SubmissionService(Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def delete_grader(
        self,
        *,
        submission_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "None":
        """Change the assigned grader of the given submission.

        :param submission_id: The id of the submission.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Empty response and a 204 status.
        """
        from ..models.base_error import BaseError
        from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

        url = "/api/v1/submissions/{submissionId}/grader".format(
            submissionId=submission_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.delete(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )

    def patch_grader(
        self,
        json_body: Union[dict, list, "PatchGraderSubmissionData"],
        *,
        submission_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "None":
        """Change the assigned grader of the given submission.

        :param json_body: The body of the request. See
            :model:`.PatchGraderSubmissionData` for information about the
            possible fields. You can provide this data as a
            :model:`.PatchGraderSubmissionData` or as a dictionary.
        :param submission_id: The id of the submission.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Empty response and a 204 status.
        """
        from ..models.base_error import BaseError
        from ..models.patch_grader_submission_data import (
            PatchGraderSubmissionData,
        )
        from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

        url = "/api/v1/submissions/{submissionId}/grader".format(
            submissionId=submission_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.patch(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )

    def get_feedback(
        self: "SubmissionService[AuthenticatedClient]",
        *,
        submission_id: "int",
        with_replies: "bool" = False,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Union[FeedbackWithoutReplies, FeedbackWithReplies]":
        """Get all feedback for a submission

        :param submission_id: The submission of which you want to get the
            feedback.
        :param with_replies: Do you want to include replies in with your
            comments? Starting with version "O.1" the default value will change
            to `True`.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The feedback of this submission.
        """
        from typing import Dict, Union

        from ..models.base_error import BaseError
        from ..models.feedback_with_replies import FeedbackWithReplies
        from ..models.feedback_without_replies import FeedbackWithoutReplies
        from ..parsers import JsonResponseParser, ParserFor, make_union

        url = "/api/v1/submissions/{submissionId}/feedbacks/".format(
            submissionId=submission_id
        )
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
            "with_replies": to_dict(with_replies),
        }

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                make_union(
                    ParserFor.make(FeedbackWithoutReplies),
                    ParserFor.make(FeedbackWithReplies),
                )
            ).try_parse(response)
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )

    def get_grade_history(
        self: "SubmissionService[AuthenticatedClient]",
        *,
        submission_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[GradeHistory]":
        """Get the grade history for the given submission.

        :param submission_id: The submission for which you want to get the
            grade history.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: All the `GradeHistory` objects, which describe the history of
                  this grade.
        """
        from typing import Sequence

        from ..models.base_error import BaseError
        from ..models.grade_history import GradeHistory
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/submissions/{submissionId}/grade_history/".format(
            submissionId=submission_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(GradeHistory))
            ).try_parse(response)
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )

    def get_rubric_result(
        self: "SubmissionService[AuthenticatedClient]",
        *,
        submission_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "WorkRubricResultAsJSON":
        """Get the full rubric result of the given submission (work).

        :param submission_id: The id of the submission
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The rubric result of the given submission, which also
                  contains the rubric.
        """
        from ..models.base_error import BaseError
        from ..models.work_rubric_result_as_json import WorkRubricResultAsJSON
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/submissions/{submissionId}/rubrics/".format(
            submissionId=submission_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(WorkRubricResultAsJSON)
            ).try_parse(response)
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )

    def get(
        self: "SubmissionService[AuthenticatedClient]",
        *,
        submission_id: "int",
        type: "Literal['zip', 'feedback', 'default']" = "default",
        owner: "Literal['student', 'teacher', 'auto']" = "auto",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Union[ExtendedWork, Mapping[str, str]]":
        """Get the given submission (also called work) by id.

        :param submission_id: The id of the submission
        :param type: If passed this cause you not to receive a submission
            object. What you will receive will depend on the value passed. If
            you pass `zip` If you pass `feedback` you will receive a text file
            with a textual representation of all the feedback given on this
            submission.
        :param owner: This query parameter is only used when `type=='zip'`. It
            will determine which revision is used to generate the zip file.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The requested submission, or one of the other types as
                  requested by the `type` query parameter.
        """
        from typing import Dict, Mapping, Union

        from typing_extensions import Literal

        from ..models.base_error import BaseError
        from ..models.extended_work import ExtendedWork
        from ..parsers import JsonResponseParser, ParserFor, make_union

        url = "/api/v1/submissions/{submissionId}".format(
            submissionId=submission_id
        )
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
            "type": to_dict(type),
            "owner": to_dict(owner),
        }

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                make_union(
                    ParserFor.make(ExtendedWork),
                    rqa.LookupMapping(rqa.SimpleValue.str),
                )
            ).try_parse(response)
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )

    def patch(
        self,
        json_body: Union[dict, list, "PatchSubmissionData"],
        *,
        submission_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ExtendedWork":
        """Update the given submission with new values.

        :param json_body: The body of the request. See
            :model:`.PatchSubmissionData` for information about the possible
            fields. You can provide this data as a
            :model:`.PatchSubmissionData` or as a dictionary.
        :param submission_id: The id of the submission.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The updated submission.
        """
        from ..models.base_error import BaseError
        from ..models.extended_work import ExtendedWork
        from ..models.patch_submission_data import PatchSubmissionData
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/submissions/{submissionId}".format(
            submissionId=submission_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.patch(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(ParserFor.make(ExtendedWork)).try_parse(
                response
            )
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )

    def patch_rubric_result(
        self,
        json_body: Union[dict, list, "PatchRubricResultSubmissionData"],
        *,
        submission_id: "int",
        copy_locked_items: "bool" = False,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "ExtendedWork":
        """Select the given rubric items for the given submission.

        :param json_body: The body of the request. See
            :model:`.PatchRubricResultSubmissionData` for information about the
            possible fields. You can provide this data as a
            :model:`.PatchRubricResultSubmissionData` or as a dictionary.
        :param submission_id: The submission to unselect the item for.
        :param copy_locked_items: Should we maintain the selected items in
            locked rubric rows.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing.
        """
        from typing import Dict

        from ..models.base_error import BaseError
        from ..models.extended_work import ExtendedWork
        from ..models.patch_rubric_result_submission_data import (
            PatchRubricResultSubmissionData,
        )
        from ..parsers import JsonResponseParser, ParserFor, make_union

        url = "/api/v1/submissions/{submissionId}/rubricitems/".format(
            submissionId=submission_id
        )
        params: "Dict[str, Any]" = {
            **(extra_parameters or {}),
            "copy_locked_items": to_dict(copy_locked_items),
        }

        with self.__client as client:
            response = client.http.patch(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(ParserFor.make(ExtendedWork)).try_parse(
                response
            )
        raise get_error(
            response, [((400, 409, 401, 403, 404, "5XX"), BaseError)]
        )
