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

from typing import Any, Optional, Sequence

from typeguard import typechecked

from kelvin.sdk.lib.models.apps.ksdk_app_setup import ProjectEmulationObject
from kelvin.sdk.lib.models.operation import OperationResponse


@typechecked
def emulation_start_simple(
    app_name_with_version: Optional[str] = None,
    app_config: Optional[str] = None,
    show_logs: bool = False,
) -> OperationResponse:
    """
    Start an application on the emulation system.

    Parameters
    ----------
    app_name_with_version: the application's name.
    app_config: the app configuration file to be used on the emulation.
    show_logs: if provided, will start displaying logs once the app is emulated.

    Returns
    ----------
    an OperationResponse object indicating whether the app was successfully started.

    """
    from kelvin.sdk.lib.emulation.emulation_manager import emulation_start_simple as _emulation_start_simple

    return _emulation_start_simple(
        app_name_with_version=app_name_with_version, app_config=app_config, show_logs=show_logs
    )


def emulation_start(project_emulation_object: ProjectEmulationObject) -> OperationResponse:
    """
    Start an application on the emulation system.

    Parameters
    ----------
    project_emulation_object: the application's emulation object.

    Returns
    ----------
    an OperationResponse object indicating whether the app was successfully started.

    """
    from kelvin.sdk.lib.emulation.emulation_manager import emulation_start as _emulation_start

    return _emulation_start(project_emulation_object=project_emulation_object)


def emulation_start_server(
    app_name_with_version: Optional[str] = None,
    app_config: Optional[str] = None,
    tail: Optional[int] = None,
    stream: bool = True,
) -> Any:
    """
    Start an application on the emulation system.

    Parameters
    ----------
    app_name_with_version: the application's name.
    app_config: the app configuration file to be used on the emulation.
    tail: the application's emulation object.
    stream: the application's emulation object.

    Returns
    ----------
    an OperationResponse object indicating whether the app was successfully started.

    """
    from kelvin.sdk.lib.emulation.emulation_manager import emulation_start_server as _emulation_start_server

    return _emulation_start_server(
        app_name_with_version=app_name_with_version, app_config=app_config, tail=tail, stream=stream
    )


@typechecked
def emulation_reset() -> OperationResponse:
    """
    Reset the Emulation System.

    Returns
    ----------
    an OperationResponse object encapsulating the result of the Emulation System reset.

    """
    from kelvin.sdk.lib.emulation.emulation_manager import emulation_reset as _emulation_reset

    return _emulation_reset()


@typechecked
def emulation_stop(app_name_with_version: Optional[str] = None) -> OperationResponse:
    """
    Stop a running application on the emulation system.

    Parameters
    ----------
    app_name_with_version: the name of the app to stop.

    Returns
    ----------
    an OperationResponse object encapsulating a message indicating whether the App was successfully stopped.

    """
    from kelvin.sdk.lib.emulation.emulation_manager import emulation_stop as _emulation_stop

    return _emulation_stop(app_name_with_version=app_name_with_version)


@typechecked
def emulation_logs(
    app_name_with_version: Optional[str] = None,
    tail: Optional[int] = None,
    should_print: bool = True,
    stream: bool = True,
    follow: bool = False,
) -> OperationResponse:
    """
    Display the logs of a running application.

    Parameters
    ----------
    app_name_with_version: the name of the application to retrieve the logs from.
    tail: indicates whether it should tail the logs and return.
    should_print: indicates whether the logs should be printed
    stream: indicates whether it should tail the logs and return.
    follow: indicates whether it should follow the logs stream.

    Returns
    ----------
    an OperationResponse object containing the status whether the App was successfully started.

    """
    from kelvin.sdk.lib.emulation.emulation_manager import emulation_logs as _emulation_logs

    return _emulation_logs(
        app_name_with_version=app_name_with_version, tail=tail, should_print=should_print, stream=stream, follow=follow
    )


@typechecked
def data_inject(
    input_file: Sequence[str],
    app_name: Sequence[str],
    period: float,
    repeat: bool,
    ignore_timestamps: bool,
    acp_name: Optional[str] = None,
    workload_name: Optional[str] = None,
) -> OperationResponse:
    """
    Start the embedded Injector app that will inject data into the emulation system..

    Parameters
    ----------
    input_file: the sequence of files that will be injected into the system.
    app_name: the app into which the data will be injected.
    period: the rate at which data will be polled from the application.
    repeat: indicates whether the injection should repeat forever.
    ignore_timestamps: ignore timestamps in data.
    acp_name: ACP name.
    workload_name: Workload name.

    Returns
    ----------
    an OperationResponse object encapsulating the result of the data injection operation.

    """

    from kelvin.sdk.lib.emulation.emulation_manager import emulation_inject as _emulation_inject

    return _emulation_inject(
        input_file=input_file,
        app_name=app_name,
        period=period,
        repeat=repeat,
        ignore_timestamps=ignore_timestamps,
        acp_name=acp_name,
        workload_name=workload_name,
    )


@typechecked
def data_extract(app_name: Sequence[str], shared_dir: str, batch: float) -> OperationResponse:
    """
    Start the embedded Extractor app that will extract data from the emulation system..

    Parameters
    ----------
    app_name: the sequence of apps to extract data from.
    shared_dir: the directory shared between the container and the host machine.
    batch: the extractor batch write frequency.

    Returns
    ----------
    an OperationResponse object encapsulating the result of the data extraction operation.

    """
    from kelvin.sdk.lib.emulation.emulation_manager import emulation_extract as _emulation_extract

    return _emulation_extract(app_name=app_name, shared_dir=shared_dir, batch=batch)
