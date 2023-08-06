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

from typing import Any, Optional

from fastapi import APIRouter

from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.server.models.parameter_models import EmulationStartRequest
from kelvin.sdk.server.utils.stream import build_stream_response

router = APIRouter(
    prefix="/emulation",
    tags=["emulation"],
    responses={404: {"description": "Not found"}},
)


@router.post("/start")
def emulation_start(emulation_request: EmulationStartRequest) -> Any:
    """
    Start an application on the emulation system.
    """
    from kelvin.sdk.interface import emulation_start_server as _emulation_start_server

    return _emulation_start_server(
        app_config=emulation_request.app_config_path,
        app_name_with_version=emulation_request.app_name_with_version,
        tail=emulation_request.tail,
        stream=emulation_request.stream,
    )


@router.post("/reset")
def emulation_reset() -> OperationResponse:
    """
    Reset the Emulation System.
    """
    from kelvin.sdk.interface import emulation_reset as _emulation_reset

    return _emulation_reset()


@router.post("/{app_name_with_version}/stop")
def emulation_stop(app_name_with_version: str) -> OperationResponse:
    """
    Stop a running application on the emulation system.
    """
    from kelvin.sdk.interface import emulation_stop as _emulation_stop

    return _emulation_stop(app_name_with_version=app_name_with_version)


@router.get("/{app_name_with_version}/logs")
def emulation_logs(
    app_name_with_version: str, tail: Optional[int] = None, stream: bool = False, follow: bool = False
) -> Any:
    """
    Display the logs of a running application.
    """
    from kelvin.sdk.interface import emulation_logs as _emulation_logs

    if stream:
        return build_stream_response(
            _emulation_logs,
            app_name_with_version=app_name_with_version,
            tail=tail,
            should_print=False,
            stream=stream,
            follow=follow,
        )

    return _emulation_logs(
        app_name_with_version=app_name_with_version,
        tail=tail,
        should_print=False,
        stream=stream,
        follow=follow,
    )
