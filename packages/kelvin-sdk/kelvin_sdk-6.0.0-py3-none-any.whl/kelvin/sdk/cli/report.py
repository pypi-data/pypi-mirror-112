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

import click

from kelvin.sdk.lib.configs.internal.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.utils.click_utils import ClickExpandedPath, KSDKCommand


@click.command(cls=KSDKCommand)
@click.option(
    "--app-config", type=ClickExpandedPath(exists=True), required=False, help=KSDKHelpMessages.report_app_config_file
)
def report(app_config: str) -> bool:
    """
    Report the user's system information and log records for support purposes.

    """
    from kelvin.sdk.interface import kelvin_report

    return kelvin_report(app_config=app_config, generate_report_file=True).success
