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
from typing import Optional, Sequence

import click

from kelvin.sdk.lib.configs.internal.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.utils.click_utils import ClickExpandedPath, KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def emulation() -> bool:
    """
    Emulate and test applications locally.
    """


@emulation.command(cls=KSDKCommand)
@click.argument("app_name_with_version", nargs=1, type=click.STRING, required=False)
@click.option(
    "--app-config", type=ClickExpandedPath(exists=True), required=False, help=KSDKHelpMessages.emulation_app_config
)
@click.option("--show-logs", is_flag=True, default=False, show_default=True, help=KSDKHelpMessages.show_logs)
def start(
    app_name_with_version: str,
    app_config: str,
    show_logs: bool,
) -> bool:
    """
    Start an application in the emulation system.

    """
    from kelvin.sdk.interface import emulation_start_simple

    return emulation_start_simple(
        app_name_with_version=app_name_with_version,
        app_config=app_config,
        show_logs=show_logs,
    ).success


@emulation.command(cls=KSDKCommand)
@click.argument("app_name_with_version", type=click.STRING, nargs=1, required=False)
def stop(app_name_with_version: str) -> bool:
    """
    Stop an application running in the application system.

    """
    from kelvin.sdk.interface import emulation_stop

    return emulation_stop(app_name_with_version=app_name_with_version).success


@emulation.command(cls=KSDKCommand)
def reset() -> bool:
    """
    Reset the emulation system.

    """
    from kelvin.sdk.interface import emulation_reset

    return emulation_reset().success


@emulation.command(cls=KSDKCommand)
@click.argument("app_name_with_version", type=click.STRING, nargs=1, required=False)
@click.option(
    "--follow", is_flag=True, default=False, show_default=True, help=KSDKHelpMessages.emulation_logs_follow_lines
)
@click.option("--tail", type=click.INT, required=False, help=KSDKHelpMessages.emulation_logs_tail_lines)
def logs(app_name_with_version: str, follow: bool, tail: Optional[int] = None) -> bool:
    """
    Show the logs of an application running in the emulation system.

    """
    from kelvin.sdk.interface import emulation_logs

    return emulation_logs(
        app_name_with_version=app_name_with_version, tail=tail, should_print=True, follow=follow
    ).success


@emulation.command(cls=KSDKCommand)
@click.argument("input_file", type=ClickExpandedPath(exists=True), nargs=-1, required=True)
@click.option("--app-name", multiple=True, required=True, help=KSDKHelpMessages.data_injector_app_name)
@click.option(
    "--period", type=click.FLOAT, default=1.0, show_default=True, help=KSDKHelpMessages.data_injector_poller_period
)
@click.option("--repeat", is_flag=True, default=False, show_default=True, help=KSDKHelpMessages.data_injector_repeat)
@click.option(
    "--ignore-timestamps",
    is_flag=True,
    default=False,
    show_default=True,
    help=KSDKHelpMessages.data_injector_ignore_timestamps,
)
@click.option("--acp-name", required=False, help=KSDKHelpMessages.emulation_acp_name)
@click.option("--workload-name", required=False, help=KSDKHelpMessages.emulation_workload_name)
def inject(
    input_file: Sequence[str],
    app_name: Sequence[str],
    period: float,
    repeat: bool,
    ignore_timestamps: bool,
    acp_name: Optional[str] = None,
    workload_name: Optional[str] = None,
) -> bool:
    """
    Initializes the default injector application.
    This application will take the input file provided and inject it into the bus.

    Supported file types: ".csv", ".parquet".

    A compressed zip file with the valid types is supported.

    """

    from kelvin.sdk.interface import data_inject

    return data_inject(
        input_file=input_file,
        app_name=app_name,
        period=period,
        repeat=repeat,
        ignore_timestamps=ignore_timestamps,
        acp_name=acp_name,
        workload_name=workload_name,
    ).success


@emulation.command(cls=KSDKCommand)
@click.argument("app_name", nargs=-1, required=True)
@click.option(
    "--output-dir",
    type=click.STRING,
    required=True,
    help=KSDKHelpMessages.data_extractor_output_dir,
    show_default=True,
)
@click.option("--batch", type=click.FLOAT, default=15.0, show_default=True, help=KSDKHelpMessages.data_extractor_batch)
def extract(app_name: Sequence[str], output_dir: str, batch: float) -> bool:
    """
    Initializes the default extractor application.

    """
    from kelvin.sdk.interface import data_extract

    return data_extract(app_name=app_name, shared_dir=output_dir, batch=batch).success
