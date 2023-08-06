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
def model_service_create(model_service_name: str, model_service_dir: str) -> OperationResponse:
    """
    Create a model service.

    Parameters
    ----------
    model_service_name: the name of the model service to create.
    model_service_dir: the path to the model service's project.

    Returns
    -------
    an OperationResponse object encapsulating the result of the model service creation operation.

    """
    from kelvin.sdk.lib.model_services.model_services_manager import model_service_create as _model_service_create

    return _model_service_create(model_service_name=model_service_name, model_service_dir=model_service_dir)


@typechecked
def model_service_build(model_service_dir: str, fresh_build: bool = False) -> OperationResponse:
    """
    The entry point to build the Model Service.

    Build the Model Service on the provided directory.

    Parameters
    ----------
    model_service_dir: the path where the model service is hosted.
    fresh_build: If specified will remove any cache and rebuild the model service from scratch.

    Returns
    -------
    an OperationResponse object wrapping the result of the build process.

    """
    from kelvin.sdk.lib.model_services.model_services_manager import model_service_build as _model_service_build

    return _model_service_build(model_service_dir=model_service_dir, fresh_build=fresh_build)


@typechecked
def model_service_start(
    model_service_name_with_version: Optional[str] = None,
    model_service_config: Optional[str] = None,
) -> OperationResponse:
    """
    Start a model service on the system.

    Parameters
    ----------
    model_service_name_with_version: the model service's name.
    model_service_config: the model service configuration file to be used on the emulation.

    Returns
    -------
    an OperationResponse object indicating whether the service was successfully started.

    """
    from kelvin.sdk.lib.model_services.model_services_manager import model_service_start as _model_service_start

    return _model_service_start(
        model_service_name_with_version=model_service_name_with_version,
        model_service_config=model_service_config,
    )


@typechecked
def model_service_stop(model_service_name_with_version: Optional[str] = None) -> OperationResponse:
    """
    Stop a running model service on the system.

    Parameters
    ----------
    model_service_name_with_version: the name of the app to stop.

    Returns
    -------
    an OperationResponse object encapsulating a message indicating whether the Model Service was successfully stopped.

    """
    from kelvin.sdk.lib.model_services.model_services_manager import model_service_stop as _model_service_stop

    return _model_service_stop(model_service_name_with_version=model_service_name_with_version)
