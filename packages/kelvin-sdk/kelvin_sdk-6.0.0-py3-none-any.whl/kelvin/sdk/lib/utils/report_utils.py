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

from kelvin.sdk.lib.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.models.generic import KPath
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.utils.general_utils import ansi_escape_string
from kelvin.sdk.lib.utils.logger_utils import logger


def report_current_status(app_config: Optional[str], generate_report_file: bool = True) -> OperationResponse:
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
    try:
        from kelvin.sdk.lib.session.session_manager import session_manager

        logger.info("Generating Kelvin report. Please wait...")
        system_information = session_manager.display_current_system_info() or "System information not available."
        system_information = ansi_escape_string(value=system_information)

        app_config_file_path: Optional[KPath] = KPath(app_config) if app_config else None
        app_config_content: str = "Application configuration not specified/available."
        if app_config_file_path and app_config_file_path.exists():
            app_config_content = str(app_config_file_path.read_content())

        ksdk_hist_file_path: KPath = session_manager.get_global_ksdk_configuration().ksdk_history_file_path
        ksdk_hist_file_content: str = "Kelvin Logs file not available."
        if ksdk_hist_file_path and ksdk_hist_file_path.exists():
            ksdk_hist_file_content = ansi_escape_string(value=ksdk_hist_file_path.read_content())

        kelvin_report_content = f"----- System Information -----\n{system_information}\n\n"
        kelvin_report_content += f"----- App Configuration file -----\n{app_config_content}\n\n"
        kelvin_report_content += f"----- Kelvin Logs -----\n{ksdk_hist_file_content}\n\n"

        success_message: str = ""
        if generate_report_file:
            kelvin_report_file: KPath = KPath(GeneralConfigs.default_report_file)
            kelvin_report_file.write_content(content=kelvin_report_content)
            success_message = f'Kelvin report successfully generated under "{kelvin_report_file.absolute()}"'
            logger.relevant(f'Kelvin report successfully generated under "{kelvin_report_file.absolute()}"')
        return OperationResponse(success=True, log=success_message, data=kelvin_report_content)
    except Exception as exc:
        error_message = f"Error generating Kelvin Report. Please contact Kelvin's support team: {exc}"
        logger.error(error_message)
        return OperationResponse(success=False, log=error_message)
