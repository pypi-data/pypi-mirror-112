# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from typing import List

from .error_analysis_request import ErrorAnalysisRequest
from .explain_request import ExplainRequest


class RequestDTO:
    """Pickleable object for transmitting the requests to remote compute.

    Ideally we ought to be able to convert this to JSON as well."""

    def __init__(self,
                 *,
                 error_analysis_requests: List[ErrorAnalysisRequest] = None,
                 explanation_requests: List[ExplainRequest] = None):
        self._explain_requests = explanation_requests if explanation_requests is not None else []
        self._error_analysis_requests = error_analysis_requests if error_analysis_requests is not None else []

    @property
    def error_analysis_requests(self) -> List[ErrorAnalysisRequest]:
        return self._error_analysis_requests

    @property
    def explanation_requests(self) -> List[ExplainRequest]:
        return self._explain_requests
