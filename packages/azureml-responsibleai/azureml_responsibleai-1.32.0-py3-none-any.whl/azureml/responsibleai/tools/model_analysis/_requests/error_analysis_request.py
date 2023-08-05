# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from typing import Optional

from .base_request import BaseRequest


class ErrorAnalysisRequest(BaseRequest):
    def __init__(self,
                 comment: Optional[str]):
        """Initialize the ErrorAnalysisRequest.

        Must be pickleable. And ideally JSON-able
        """
        super(ErrorAnalysisRequest, self).__init__()
        self._comment = comment

    @property
    def comment(self) -> Optional[str]:
        return self._comment
