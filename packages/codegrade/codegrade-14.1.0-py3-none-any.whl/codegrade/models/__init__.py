"""Contains all the data models used in inputs/outputs.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

from ._submission_rubric_item_data_parser import (
    _SubmissionRubricItemDataParser,
)
from .about import About
from .abstract_role import AbstractRole
from .all_auto_test_results import AllAutoTestResults
from .all_site_settings import AllSiteSettings
from .api_codes import APICodes
from .assignment import Assignment
from .assignment_anonymization_algo import AssignmentAnonymizationAlgo
from .assignment_done_type import AssignmentDoneType
from .assignment_feedback import AssignmentFeedback
from .assignment_grader import AssignmentGrader
from .assignment_kind import AssignmentKind
from .assignment_login_link import AssignmentLoginLink
from .assignment_peer_feedback_connection import (
    AssignmentPeerFeedbackConnection,
)
from .assignment_peer_feedback_settings import AssignmentPeerFeedbackSettings
from .assignment_state_enum import AssignmentStateEnum
from .auto_test import AutoTest
from .auto_test_fixture import AutoTestFixture
from .auto_test_quality_comment import AutoTestQualityComment
from .auto_test_result import AutoTestResult
from .auto_test_result_state import AutoTestResultState
from .auto_test_result_with_extra_data import AutoTestResultWithExtraData
from .auto_test_run import AutoTestRun
from .auto_test_runner import AutoTestRunner
from .auto_test_runner_state import AutoTestRunnerState
from .auto_test_set import AutoTestSet
from .auto_test_step_base import AutoTestStepBase
from .auto_test_step_base_input_as_json import AutoTestStepBaseInputAsJSON
from .auto_test_step_log_base import AutoTestStepLogBase
from .auto_test_step_result import AutoTestStepResult
from .auto_test_step_result_state import AutoTestStepResultState
from .auto_test_suite import AutoTestSuite
from .base_about import BaseAbout
from .base_auto_test_quality_comment import BaseAutoTestQualityComment
from .base_auto_test_step_base import BaseAutoTestStepBase
from .base_error import BaseError
from .base_file import BaseFile
from .base_lti1p1_provider import BaseLTI1p1Provider
from .base_lti1p3_provider import BaseLTI1p3Provider
from .base_lti_provider import BaseLTIProvider
from .base_release_info import BaseReleaseInfo
from .base_rubric_item import BaseRubricItem
from .change_user_role_course_data import ChangeUserRoleCourseData
from .column_range import ColumnRange
from .comment_base import CommentBase
from .comment_reply import CommentReply
from .comment_reply_edit import CommentReplyEdit
from .comment_reply_type import CommentReplyType
from .comment_type import CommentType
from .copy_auto_test_data import CopyAutoTestData
from .copy_rubric_assignment_data import CopyRubricAssignmentData
from .course import Course
from .course_registration_link import CourseRegistrationLink
from .course_role import CourseRole
from .course_snippet import CourseSnippet
from .course_state import CourseState
from .create_auto_test_data import CreateAutoTestData
from .create_course_data import CreateCourseData
from .create_group_set_course_data import CreateGroupSetCourseData
from .create_lti_data import CreateLTIData
from .create_snippet_course_data import CreateSnippetCourseData
from .create_tenant_data import CreateTenantData
from .custom_output_log import CustomOutputLog
from .custom_output_log_base import CustomOutputLogBase
from .email_notification_types import EmailNotificationTypes
from .email_users_course_data import EmailUsersCourseData
from .extended_auto_test_result import ExtendedAutoTestResult
from .extended_auto_test_run import ExtendedAutoTestRun
from .extended_course import ExtendedCourse
from .extended_group import ExtendedGroup
from .extended_job import ExtendedJob
from .extended_tenant import ExtendedTenant
from .extended_user import ExtendedUser
from .extended_work import ExtendedWork
from .feedback_base import FeedbackBase
from .feedback_with_replies import FeedbackWithReplies
from .feedback_without_replies import FeedbackWithoutReplies
from .file_mixin import FileMixin
from .file_rule_input_data import FileRuleInputData
from .file_tree import FileTree
from .finalized_lti1p1_provider import FinalizedLTI1p1Provider
from .finalized_lti1p3_provider import FinalizedLTI1p3Provider
from .fixture_like import FixtureLike
from .frontend_site_settings import FrontendSiteSettings
from .global_perm_map import GlobalPermMap
from .grade_history import GradeHistory
from .grade_origin import GradeOrigin
from .group import Group
from .group_set import GroupSet
from .health_information import HealthInformation
from .import_into_assignment_data import ImportIntoAssignmentData
from .import_into_course_data import ImportIntoCourseData
from .io_test_log import IOTestLog
from .io_test_step_log import IOTestStepLog
from .io_test_step_log_base import IOTestStepLogBase
from .job import Job
from .json_create_auto_test import JsonCreateAutoTest
from .json_create_tenant import JsonCreateTenant
from .json_patch_auto_test import JsonPatchAutoTest
from .junit_test_log import JunitTestLog
from .junit_test_log_base import JunitTestLogBase
from .legacy_features import LegacyFeatures
from .line_range import LineRange
from .linter_comment import LinterComment
from .lms_capabilities import LMSCapabilities
from .login_user_data import LoginUserData
from .non_finalized_lti1p1_provider import NonFinalizedLTI1p1Provider
from .non_finalized_lti1p3_provider import NonFinalizedLTI1p3Provider
from .notification_reasons import NotificationReasons
from .notification_setting import NotificationSetting
from .notification_setting_option import NotificationSettingOption
from .options_input_data import OptionsInputData
from .patch_assignment_data import PatchAssignmentData
from .patch_auto_test_data import PatchAutoTestData
from .patch_course_data import PatchCourseData
from .patch_grader_submission_data import PatchGraderSubmissionData
from .patch_notification_setting_user_setting_data import (
    PatchNotificationSettingUserSettingData,
)
from .patch_rubric_result_submission_data import (
    PatchRubricResultSubmissionData,
)
from .patch_site_settings_data import PatchSiteSettingsData
from .patch_snippet_course_data import PatchSnippetCourseData
from .patch_submission_data import PatchSubmissionData
from .patch_tenant_data import PatchTenantData
from .patch_ui_preference_user_setting_data import (
    PatchUiPreferenceUserSettingData,
)
from .patch_user_data import PatchUserData
from .plagiarism_run import PlagiarismRun
from .plagiarism_run_plagiarism_assignment_as_json import (
    PlagiarismRunPlagiarismAssignmentAsJSON,
)
from .plagiarism_run_plagiarism_course_as_json import (
    PlagiarismRunPlagiarismCourseAsJSON,
)
from .plagiarism_state import PlagiarismState
from .put_enroll_link_course_data import PutEnrollLinkCourseData
from .put_rubric_assignment_data import PutRubricAssignmentData
from .quality_comment_severity import QualityCommentSeverity
from .quality_test_log import QualityTestLog
from .quality_test_log_base import QualityTestLogBase
from .register_user_data import RegisterUserData
from .release_info import ReleaseInfo
from .result_data_get_auto_test_get import ResultDataGetAutoTestGet
from .result_data_get_task_result_get_all import ResultDataGetTaskResultGetAll
from .result_data_get_user_setting_get_all_ui_preferences import (
    ResultDataGetUserSettingGetAllUiPreferences,
)
from .result_data_post_login_link_login import ResultDataPostLoginLinkLogin
from .result_data_post_user_login import ResultDataPostUserLogin
from .result_data_post_user_register import ResultDataPostUserRegister
from .rubric_description_type import RubricDescriptionType
from .rubric_item import RubricItem
from .rubric_item_input_as_json import RubricItemInputAsJSON
from .rubric_lock_reason import RubricLockReason
from .rubric_row_base import RubricRowBase
from .rubric_row_base_input_as_json import RubricRowBaseInputAsJSON
from .rubric_row_base_input_base_as_json import RubricRowBaseInputBaseAsJSON
from .run_program_log import RunProgramLog
from .site_setting_input import SiteSettingInput
from .snippet import Snippet
from .submission_validator_input_data import SubmissionValidatorInputData
from .task_result_state import TaskResultState
from .tenant import Tenant
from .tenant_course_statistics import TenantCourseStatistics
from .tenant_statistics import TenantStatistics
from .types import *
from .ui_preference_name import UIPreferenceName
from .update_peer_feedback_settings_assignment_data import (
    UpdatePeerFeedbackSettingsAssignmentData,
)
from .update_set_auto_test_data import UpdateSetAutoTestData
from .update_suite_auto_test_data import UpdateSuiteAutoTestData
from .user import User
from .user_course import UserCourse
from .user_input import UserInput
from .user_without_group import UserWithoutGroup
from .webhook_base import WebhookBase
from .work import Work
from .work_origin import WorkOrigin
from .work_rubric_item import WorkRubricItem
from .work_rubric_result_as_json import WorkRubricResultAsJSON
from .work_rubric_result_points_as_json import WorkRubricResultPointsAsJSON
