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
from typing import List, Optional

from kelvin.sdk.lib.apps.local_apps_manager import project_build, project_create
from kelvin.sdk.lib.configs.internal.emulation_configs import EmulationConfigs
from kelvin.sdk.lib.emulation.emulation_manager import emulation_start, emulation_stop, load_base_emulation_object
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import ProjectType
from kelvin.sdk.lib.models.apps.ksdk_app_setup import ProjectCreationParametersObject
from kelvin.sdk.lib.models.factories.docker_manager_factory import get_docker_manager
from kelvin.sdk.lib.models.ksdk_docker import DockerContainer
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.utils.logger_utils import logger


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
    try:
        project_creation_parameters = ProjectCreationParametersObject(
            app_dir=model_service_dir,
            app_name=model_service_name,
            app_description="",
            app_type=ProjectType.model_service,
        )
        return project_create(project_creation_parameters=project_creation_parameters)

    except Exception as exc:
        error_message = f"Error creating model service: {str(exc)}"
        logger.error(error_message)
        return OperationResponse(success=False, log=error_message)


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
    return project_build(app_dir=model_service_dir, fresh_build=fresh_build)


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
    try:
        app_emulation_object = load_base_emulation_object(
            app_name_with_version=model_service_name_with_version, app_config=model_service_config
        )
        app_emulation_object.show_logs = False

        successfully_started = emulation_start(project_emulation_object=app_emulation_object)

        if successfully_started.success:
            docker_manager = get_docker_manager()

            existing_ksdk_containers: List[DockerContainer] = docker_manager.get_docker_containers(
                image_name=f"{app_emulation_object.app_name}"
            )
            container: DockerContainer = existing_ksdk_containers[0]

            localhost_url: str = EmulationConfigs.model_service_docs_url.format(
                host="localhost", port=container.ports[0].public_port
            )

            container_url: str = EmulationConfigs.model_service_docs_url.format(
                host=container.id_address, port=container.ports[0].private_port
            )

            start_success: str = f"""

                    Model service successfully started!
                    Use your browser of choice to access the documentation:

                    \"{container_url}\"
                    or
                    \"{localhost_url}\"

                    Opening Model Service...

                """
            logger.relevant(start_success)

            message = f'Access Model Service by : "{app_emulation_object.app_name}"'
            logger.relevant(message)

        return successfully_started
    except Exception as exc:
        error_message = f"Error starting model service:\n{str(exc)}"
        logger.exception(error_message)

        return OperationResponse(success=False, log=error_message)


def model_service_stop(model_service_name_with_version: Optional[str]) -> OperationResponse:
    """
    Stop a running model service on the system.

    Parameters
    ----------
    model_service_name_with_version: the name of the app to stop.

    Returns
    -------
    an OperationResponse object encapsulating a message indicating whether the Model Service was successfully stopped.

    """
    return emulation_stop(app_name_with_version=model_service_name_with_version, project_type=ProjectType.model_service)
