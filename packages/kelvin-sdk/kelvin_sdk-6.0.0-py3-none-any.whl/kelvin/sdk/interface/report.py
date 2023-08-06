"""
Copyright 2021 Kelvin Inc.

Licensed under the Kelvin Inc. Developer SDK License Agreement (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

http://www.kelvininc.com/developer-sdk-license

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
"""
from typing import Optional

from typeguard import typechecked

from kelvin.sdk.lib.models.operation import OperationResponse


@typechecked
def kelvin_report(app_config: Optional[str] = None, generate_report_file: bool = True) -> OperationResponse:
    """
    Report the user's system information and log records for support purposes.

    Parameters
    ----------
    app_config: the path to the application's configuration file.
    generate_report_file: if set to true, will generate the report file to the default location.

    Returns
    -------
    an OperationResponse object encapsulating the host machine's system report.

    """
    from kelvin.sdk.lib.utils.report_utils import report_current_status as _report_current_status

    return _report_current_status(app_config=app_config, generate_report_file=generate_report_file)
