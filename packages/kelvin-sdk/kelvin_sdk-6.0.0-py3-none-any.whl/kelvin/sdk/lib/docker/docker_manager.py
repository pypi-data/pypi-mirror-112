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

import tarfile
from pathlib import Path, PurePosixPath
from random import randint
from tempfile import TemporaryDirectory
from typing import Any, Dict, List, Optional, Union

from docker import APIClient  # type: ignore
from docker.errors import APIError, DockerException, NotFound
from docker.types import CancellableStream
from jinja2 import Template

from kelvin.sdk.lib.configs.internal.docker_configs import DockerConfigs
from kelvin.sdk.lib.configs.internal.emulation_configs import EmulationConfigs
from kelvin.sdk.lib.configs.internal.general_configs import GeneralConfigs, GeneralMessages
from kelvin.sdk.lib.docker.docker_utils import (
    assess_docker_connection_exception,
    display_docker_progress,
    ensure_docker_is_running,
    handle_error_stack_trace,
    process_dockerfile_build_entry,
)
from kelvin.sdk.lib.exceptions import DependencyNotRunning, InvalidApplicationConfiguration, KDockerException
from kelvin.sdk.lib.models.apps.kelvin_app import ApplicationInterface, ApplicationLanguage, Mqtt
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import Environment, ProjectType
from kelvin.sdk.lib.models.apps.ksdk_app_setup import (
    DockerAppBuildingObject,
    KelvinAppBuildingObject,
    ProjectBuildingObject,
    ProjectEmulationObject,
)
from kelvin.sdk.lib.models.generic import KPath, OSInfo
from kelvin.sdk.lib.models.ksdk_docker import (
    DockerBuildEntry,
    DockerContainer,
    DockerImage,
    DockerImageNameDetails,
    DockerNetwork,
    KSDKDockerAuthentication,
    KSDKNetworkConfig,
)
from kelvin.sdk.lib.models.types import EmbeddedFiles, VersionStatus
from kelvin.sdk.lib.session.session_manager import session_manager
from kelvin.sdk.lib.templates.templates_manager import get_embedded_file
from kelvin.sdk.lib.utils.display_utils import pretty_colored_content
from kelvin.sdk.lib.utils.general_utils import (
    check_if_requirement_is_present,
    get_iec_to_si_format_as_human_readable,
    get_random_hex_string,
)
from kelvin.sdk.lib.utils.logger_utils import logger
from kelvin.sdk.lib.utils.version_utils import assess_version_status, color_formats


class DockerManager:
    _docker_client: APIClient
    _minimum_docker_version: Optional[str]

    def __init__(
        self,
        credentials: KSDKDockerAuthentication,
        network_configuration: KSDKNetworkConfig,
        minimum_docker_version: Optional[str] = None,
    ):
        """
        Initializes a DockerManager object based on the provided configurations.

        :param network_configuration: the object containing all the variables required to manage a docker network.
        :param credentials: the object containing all necessary credentials for docker registry interaction.
        :param minimum_docker_version: the minimum accepted docker version to run KSDK.

        """
        self._reset_docker_client()
        self._minimum_docker_version = minimum_docker_version
        self._validate_docker_version(minimum_docker_version=self._minimum_docker_version)
        # Credentials
        self._credentials = credentials
        # Setup the network configuration
        self._network_configuration = network_configuration

    def _reset_docker_client(self) -> APIClient:
        """
        Resets the client to its original state.

        :return: the internal Docker API Client in its new state.

        """
        try:
            self._docker_client = APIClient(timeout=DockerConfigs.docker_client_timeout)
        except Exception as exc:
            raise assess_docker_connection_exception(exc=exc)
        return self._docker_client

    @ensure_docker_is_running
    def _validate_docker_version(self, minimum_docker_version: Optional[str]) -> bool:
        """
        Sets up the minimum accepted docker version and matches it against the current docker version of the system.

        :param minimum_docker_version: the minimum accepted docker version, externally injected.

        :return: a boolean indicating whether or not the current docker version is supported and able to to run ksdk.
        """
        version_status = VersionStatus.UP_TO_DATE
        if minimum_docker_version:
            system_docker_version = ""
            try:
                docker_version_object = self._docker_client.version() if self._docker_client else None
            except (DockerException, Exception):
                docker_version_object = None

            if docker_version_object:
                system_docker_version = docker_version_object.get("Version", "").rsplit("-", 1)[0]

            if not system_docker_version:
                raise DependencyNotRunning(message=DockerConfigs.docker_dependency)

            version_status = assess_version_status(
                minimum_version=minimum_docker_version,
                current_version=system_docker_version,
                latest_version=system_docker_version,
            )

            if version_status == VersionStatus.UNSUPPORTED:
                docker_version_unsupported: str = """\n
                        {red}Docker version is no longer supported!{reset} \n
                        {red}Current: {current_version}{reset} → {yellow}Minimum: {minimum_version}{reset} \n
                        {green}For more information{reset}: https://docs.docker.com/engine/install/ \n
                        Please update Docker in order to proceed.
                """.format_map(
                    {
                        **color_formats,
                        "current_version": system_docker_version,
                        "minimum_version": minimum_docker_version,
                    }
                )
                raise KDockerException(message=docker_version_unsupported)

        return version_status == VersionStatus.UP_TO_DATE

    # 1 - AUTH
    @ensure_docker_is_running
    def login_on_docker_registry(self) -> Optional[APIClient]:
        """
        Logs in to the docker registry specified in the credentials object.

        :return:(s) the successfully logged instance Docker APIClient.

        """
        try:
            self._docker_client.login(
                username=self._credentials.username,
                password=self._credentials.password,
                registry=self._credentials.full_registry_url,
                reauth=True,
            )
            registry = self._credentials.full_registry_url
            logger.relevant(f'Successfully logged on registry "{registry}"')
            return self._docker_client
        except APIError as exc:
            if exc.status_code == 500:
                login_docker_registry_failure: str = f"""
                    "Error accessing the registry: {exc.explanation}. \n
                    The build process will continue regardless."
                """
                logger.warning(login_docker_registry_failure)
                return None
            raise

    # 2 - NETWORKS
    @ensure_docker_is_running
    def get_docker_network_id(self) -> str:
        """
        Get the id of the docker network specified in the instance network configuration.

        :return: the running id of the matching the network configuration.

        """
        matching_networks = self._docker_client.networks(names=[self._network_configuration.network_name])
        target_network = matching_networks[0] if matching_networks else {}
        return DockerNetwork(**target_network).id

    @ensure_docker_is_running
    def create_docker_network(self) -> bool:
        """
        Creates and launches a docker network with the specified instance configuration.

        :return: a boolean indicating whether the network was initiated.

        """
        docker_network_successfully_created = True

        network_name = self._network_configuration.network_name
        docker_network_id = self.get_docker_network_id()

        if not docker_network_id:
            result = self._docker_client.create_network(
                name=network_name, driver=self._network_configuration.network_driver, internal=False
            )
            docker_network_successfully_created = bool(result)

        if docker_network_successfully_created:
            logger.debug(f'Docker network "{network_name}" successfully started')
            return True

        raise KDockerException(message=f'Error starting docker network "{network_name}"')

    @ensure_docker_is_running
    def remove_docker_network(self) -> bool:
        """
        Removes all docker networks that correspond to the instance's network configuration.

        :return: a boolean indicating whether the specified docker networks were removed.

        """
        docker_network_name = self._network_configuration.network_name
        docker_network_id = self.get_docker_network_id()

        if docker_network_id:
            docker_containers_to_be_stopped = self.get_network_docker_containers()
            for container in docker_containers_to_be_stopped:
                self._docker_client.disconnect_container_from_network(container=container.id, net_id=docker_network_id)
                self._docker_client.stop(container.id)
            self._docker_client.remove_network(net_id=docker_network_id)
            self._docker_client.prune_networks()

        logger.debug(f'Docker network "{docker_network_name}" successfully removed')
        return True

    @ensure_docker_is_running
    def get_network_docker_containers(self) -> List[DockerContainer]:
        """
        Retrieve the ids of all docker containers running on the instance's network.

        :return: a list containing the ids of the docker containers running under the instance's network.

        """
        network_docker_containers: List[DockerContainer] = []

        matching_networks = [
            DockerNetwork(**network_obj)
            for network_obj in self._docker_client.networks(names=[self._network_configuration.network_name])
        ]

        for network in matching_networks:
            detailed_network_info = self._docker_client.inspect_network(net_id=network.id)
            container_keys = detailed_network_info.get("Containers", {}) if detailed_network_info else {}
            for key, value in container_keys.items():
                container_name = value.get("Name", "")
                container_state = value.get("State", "")
                container_is_running = container_state == "running"
                network_docker_containers.append(
                    DockerContainer(id=key, image_name=container_name, running=container_is_running)
                )

        return network_docker_containers

    # 3 - DOCKERFILES
    @staticmethod
    def build_kelvin_app_dockerfile(kelvin_app_building_object: KelvinAppBuildingObject) -> bool:
        """
        Build the docker file used in the creation of the docker image.

        :param kelvin_app_building_object: the KelvinAppBuildingObject with all the required variables to build an app.

        :return: a boolean indicating whether the dockerfile was successfully built.

        """
        # 1 - Make sure the kelvin app configuration is available
        kelvin_app = kelvin_app_building_object.app_config_model.app.app_type_configuration
        if kelvin_app is None:
            raise InvalidApplicationConfiguration(message=str(kelvin_app_building_object.app_config_file_path))

        if kelvin_app.language is None:
            raise InvalidApplicationConfiguration(
                message=GeneralMessages.invalid_name.format(reason="Language is missing")
            )

        # 2 - if there is an image configuration that provides a valid system packages list, collect it.
        system_packages: str = ""
        if kelvin_app.system_packages:
            system_packages = " ".join(kelvin_app.system_packages)

        # 3 - Verify compatibility between for both python and cpp apps.
        requirements_file = None
        app_language = kelvin_app.language.type
        app_interface: Optional[ApplicationInterface] = kelvin_app.interface.type if kelvin_app.interface else None

        adhoc_python_dependencies: List[str] = []
        app_file_system_name: str = ""

        if app_language == ApplicationLanguage.python:
            python_app_config = kelvin_app.language.python
            if python_app_config:
                # extract file path from entrypoint point
                if python_app_config.entry_point:
                    entrypoint_file = python_app_config.entry_point.root_value.split(":")[0]
                    # get parent folder from entrypoint
                    app_file_system_name = KPath(entrypoint_file).parent

                aux_req_file: KPath = kelvin_app_building_object.app_dir_path / python_app_config.requirements
                if aux_req_file and aux_req_file.exists():
                    requirements_file = KPath(aux_req_file).relative_to(kelvin_app_building_object.app_dir_path)
                    # Make sure kelvin-app is injected
                    kelvin_app_dep = GeneralConfigs.default_kelvin_app_dependency_simple
                    if not check_if_requirement_is_present(file_path=requirements_file, requirement=kelvin_app_dep):
                        adhoc_python_dependencies.append(GeneralConfigs.default_kelvin_app_dependency)
                else:
                    adhoc_python_dependencies = [GeneralConfigs.default_kelvin_app_dependency]
            if app_interface and app_interface is not ApplicationInterface.client:
                invalid_interface = "Invalid interface. Please provide a client type interface"
                error_message = GeneralMessages.invalid_name.format(reason=invalid_interface)
                raise InvalidApplicationConfiguration(message=error_message)
        if app_language == ApplicationLanguage.cpp:
            if kelvin_app.language.cpp and kelvin_app.language.cpp.dso:
                app_file_system_name = KPath(kelvin_app.language.cpp.dso).parent
            if app_interface and app_interface is not ApplicationInterface.data:
                invalid_interface = "Invalid interface. Please provide a data type interface"
                error_message = GeneralMessages.invalid_name.format(reason=invalid_interface)
                raise InvalidApplicationConfiguration(message=error_message)

        # 4 - Retrieve the appropriate docker template for the language the app is building for.
        template = (
            EmbeddedFiles.CPP_APP_DOCKERFILE
            if app_language == ApplicationLanguage.cpp
            else EmbeddedFiles.PYTHON_APP_DOCKERFILE
        )

        # check if there are any wheels
        wheels = (kelvin_app_building_object.app_dir_path / GeneralConfigs.default_wheels_dir).glob("*.whl")
        wheels_dir = GeneralConfigs.default_wheels_dir if any(wheels) else None

        dockerfile_template: Template = get_embedded_file(embedded_file=template)
        if not dockerfile_template:
            raise KDockerException(f"No template available for {app_language.value_as_str} kelvin_app_lang")

        # 5 - Prepare the dockerfile parameters and finally render the template with them as arguments.
        dockerfile_parameters: Dict[str, Any] = {
            "build_for_datatype_compilation": kelvin_app_building_object.build_for_datatype_compilation,
            "base_data_model_builder_image": kelvin_app_building_object.base_data_model_builder_image,
            "base_image": kelvin_app_building_object.base_image,
            "app_configuration_file": kelvin_app_building_object.app_config_file_path.name,
            "build_for_upload": kelvin_app_building_object.build_for_upload,
            "app_file_system_name": app_file_system_name,
            "requirements_file": requirements_file,
            "system_packages": system_packages,
            "app_language": app_language.name,
            "adhoc_python_dependencies": " ".join(adhoc_python_dependencies),
            "wheels_dir": wheels_dir,
        }
        if app_language.name == "python":
            if kelvin_app.language.python:
                dockerfile_parameters.update({"entry_point": kelvin_app.language.python.entry_point})
            executable: str = GeneralConfigs.default_executable
            if kelvin_app.interface and kelvin_app.interface.client and kelvin_app.interface.client.executable:
                executable = kelvin_app.interface.client.executable
            dockerfile_parameters.update({"executable": executable})

        dockerfile_content = dockerfile_template.render(dockerfile_parameters)
        kelvin_app_building_object.dockerfile_path.write_text(dockerfile_content)
        logger.debug(f"Build Dockerfile:\n\n{dockerfile_content}")

        return True

    # 4 - IMAGES
    @ensure_docker_is_running
    def build_kelvin_app_docker_image(self, kelvin_app_building_object: KelvinAppBuildingObject) -> bool:
        """
        Build the docker image from the provided KelvinAppBuildingObject.

        An exception is expected should any step of the process fail.

        :param kelvin_app_building_object: an object that contains the necessary variables to build a kelvin-type app.

        :return: a boolean indicating whether the image was successfully built.

        """
        # 1 - Login on the registry
        self.login_on_docker_registry()

        # 2 - Both the base builder image and datamodel builder images are required so we assure them
        self.ensure_base_docker_images_exist(
            base_docker_image=kelvin_app_building_object.base_image,
            base_data_model_builder=kelvin_app_building_object.base_data_model_builder_image,
        )

        return self._build_engine_step(
            base_build_object=kelvin_app_building_object,
            dockerfile_path=kelvin_app_building_object.dockerfile_path,
            docker_build_context_path=kelvin_app_building_object.docker_build_context_path,
            build_args=kelvin_app_building_object.build_args,
        )

    @ensure_docker_is_running
    def build_docker_app_image(self, docker_build_object: DockerAppBuildingObject) -> bool:
        """
        Build the docker image from the provided DockerAppBuildingObject.

        An exception is expected should any step of the process fail.

        :param docker_build_object: an object that contains the necessary variables to build a docker-type app.

        :return: a boolean indicating whether the image was successfully built.

        """
        dockerfile_path: Optional[KPath]
        docker_build_context_path: Optional[KPath]
        build_args = {}

        # 1 - Make sure the kelvin app configuration is available
        docker_app = docker_build_object.app_config_model.app.docker
        if not docker_app:
            raise InvalidApplicationConfiguration(message=str(docker_build_object.app_config_file_path))

        dockerfile_path = KPath(docker_app.dockerfile)
        docker_build_context_path = KPath(docker_app.context)
        if docker_app.args:
            split_args = (arg.split("=") for arg in docker_app.args)
            build_args = {key: value for key, value in split_args}

        return self._build_engine_step(
            base_build_object=docker_build_object,
            dockerfile_path=dockerfile_path,
            docker_build_context_path=docker_build_context_path,
            build_args=build_args,
        )

    def _build_engine_step(
        self,
        base_build_object: ProjectBuildingObject,
        dockerfile_path: KPath,
        docker_build_context_path: KPath,
        build_args: Optional[Dict[str, str]],
    ) -> bool:
        """
        Internal method shared by both kelvin and docker apps in order to build.

        :param base_build_object: the base building object with the necessary inputs.
        :param dockerfile_path: the path to the dockerfile
        :param docker_build_context_path: the path to where the docker build should be executed (context).
        :param build_args: additional build arguments to be passed to the build operation.

        :return: a boolean indicating the build step was successfully executed.

        """
        docker_image_name = base_build_object.full_docker_image_name  # name of the docker image
        docker_image_labels = base_build_object.docker_image_labels  # ksdk identification labels
        dockerfile_path_relative_to_context = PurePosixPath(dockerfile_path.relative_to(docker_build_context_path))
        build_log_file = GeneralConfigs.default_build_logs_file
        docker_build_complete_stack: List[DockerBuildEntry] = []
        docker_stack_trace_has_errors: bool = False

        # 3 - Fresh applications attempt to purge all the existing cache
        if base_build_object.fresh_build:
            self.prune_docker_containers()
            self.prune_docker_images()

        # 4 - If its a 'rebuild', stop all existing containers of this same app
        if self.check_if_docker_image_exists(docker_image_name=docker_image_name):
            # 5 - If its an 'appregistry upload', purge any previous instance and start from scratch
            if base_build_object.fresh_build or base_build_object.build_for_upload:
                self.remove_docker_image(docker_image_name=docker_image_name)
            else:
                self.stop_docker_containers_for_image(docker_image_name=docker_image_name)

        # 6 - Build the image and store the logs
        logger.info(f'Building new image for "{docker_image_name}". Please wait..')
        for entry in self._docker_client.build(
            path=str(docker_build_context_path),
            dockerfile=str(dockerfile_path_relative_to_context),
            tag=docker_image_name,
            labels=docker_image_labels,
            buildargs=build_args,
            rm=True,
            decode=True,
        ):
            # 6.1 - Store all log output entries
            dockerfile_build_entry = DockerBuildEntry(**entry)
            docker_build_complete_stack.append(dockerfile_build_entry)
            # 6.2 - If there are any errors, collect them as well
            docker_stack_trace_has_errors |= dockerfile_build_entry.entry_has_errors
            # 6.3 output the verbose entries to the debug level
            verbose_entry = process_dockerfile_build_entry(entry=entry)
            if verbose_entry:
                logger.debug(verbose_entry)

        # 7 - Once built, tag the image to have a 'latest' version
        if self.check_if_docker_image_exists(docker_image_name=docker_image_name):
            self._docker_client.tag(
                image=docker_image_name,
                repository=base_build_object.docker_image_name,
                tag=DockerConfigs.latest_docker_image_version,
            )

        # 8 - Output the complete Dockerfile and respective logs to the build/build.log file
        build_logs_file: KPath = dockerfile_path.parent / build_log_file
        if not build_logs_file.parent.exists():
            build_logs_file.parent.mkdir()

        log_file_content = KPath(dockerfile_path).read_text() + "\n"
        log_file_content += "\n".join([entry.log_content for entry in docker_build_complete_stack])
        build_logs_file.write_content(content=log_file_content)

        logger.debug(f'Build logs successfully registered on "{build_logs_file}"')

        # 9 - Raise an exception if there is any error in the stack
        if docker_stack_trace_has_errors:
            handle_error_stack_trace(complete_stack=docker_build_complete_stack)
        return True

    @ensure_docker_is_running
    def run_app_docker_image(self, project_emulation_object: ProjectEmulationObject) -> bool:
        """
        Run the specified App docker image with the provided command as argument.

        :param project_emulation_object: the application's emulation object.

        :return: a boolean indicating whether the image exists was successfully started.

        """
        # 0 - Setup a temporary directory path for interactions
        ksdk_temp_dir_prefix = session_manager.get_global_ksdk_configuration().ksdk_temp_dir_path.create_dir()
        temporary_directory_name: str = get_random_hex_string()
        temporary_directory_path: KPath = KPath(ksdk_temp_dir_prefix / temporary_directory_name)

        # 1 - Getting both container's name in the network and the network id to run the container on
        docker_image_name_details = DockerImageNameDetails(
            registry_url=project_emulation_object.emulation_app_name,
            docker_image_name=project_emulation_object.emulation_app_name,
        )
        container_name_in_the_network = docker_image_name_details.container_name

        # 2 - Assess if its a normal app or if it has a custom entrypoint
        if not project_emulation_object.entrypoint:
            # 2.1 - In case its a normal app, stop its running instances and remove them before advancing
            self.stop_docker_containers_for_image(docker_image_name=project_emulation_object.emulation_app_name)
            self.remove_container(container=container_name_in_the_network)
        else:
            container_name_in_the_network += f"-{randint(0, 1 << 16)}"  # nosec
            logger.info(f'Running container: "{container_name_in_the_network}"')

        # 3 - get all the container configurations for the application's host config
        reporter: dict = {}

        # 3.1 - Environment variables
        environment_variables = (
            {**project_emulation_object.environment_variables}
            if project_emulation_object.environment_variables is not None
            else {}
        )
        env_vars_collector = []
        for variable_name, _ in environment_variables.items():
            env_vars_collector.append(f'Loading "{variable_name}" from the configuration file')

        # 3.1.2 - add credential environment vars for client access during emulation
        client = session_manager.login_client_on_current_url()
        environment_variables.update(
            (key, str(value))
            for key, value in [
                ("KELVIN_URL", client.config.url),
                ("KELVIN_USERNAME", client.config.username),
                ("KELVIN_PASSWORD", client.password),
            ]
            if key not in environment_variables and value is not None
        )

        # 3.2 - Port bindings
        port_mapping_bindings = project_emulation_object.port_mapping or {}
        ports_collector = []
        for container_port, host_port in port_mapping_bindings.items():
            ports_collector.append(f'Container port "{container_port}" connected to host port "{host_port}"')

        # 3.3 - Text file volumes
        file_volumes = project_emulation_object.file_volumes or []
        file_volumes_to_add_to_container: Dict[KPath, str] = {}
        for file_volume in file_volumes:
            source_volume_file: KPath = temporary_directory_path / file_volume.source_file_path.name
            source_volume_file.write_content(content=file_volume.content)
            file_volumes_to_add_to_container[source_volume_file] = file_volume.container_file_path
            logger.relevant(f'Creating file volume under "{file_volume.container_file_path}"')
            file_volume_str_bind = f"{source_volume_file.absolute()}:{file_volume.container_file_path}:Z"
            if not project_emulation_object.volumes:
                project_emulation_object.volumes = []
            project_emulation_object.volumes.append(file_volume_str_bind)

        # 3.4 - Generic volumes
        volume_bindings = project_emulation_object.volumes or []
        volume_collector: list = []
        for volume in volume_bindings:
            host_volume, container_volume = volume.split(":", 2)[0:2]
            volume_collector.append(f'"{container_volume}" connected to "{host_volume}" (container -> host)')

        # 3.5 - Memory configuration
        memory_limit = None
        memory_collector: list = []
        if project_emulation_object.memory:
            memory_limit = get_iec_to_si_format_as_human_readable(project_emulation_object.memory)
            memory_collector.append(f'Container memory restricted to a maximum of "{memory_limit}"')

        if project_emulation_object.privileged:
            reporter["Privileges"] = ['Running the container in "privileged" mode.']
        if env_vars_collector:
            reporter["Environment variables"] = env_vars_collector
        if ports_collector:
            reporter["Ports"] = ports_collector
        if volume_collector:
            reporter["Volumes"] = volume_collector
        if memory_collector:
            reporter["Memory"] = memory_collector

        if reporter:
            final_reporter = {"Emulation configurations applied to container": reporter}
            colored_content = pretty_colored_content(content=final_reporter, initial_indent=2, indent=2, show_arm=True)
            logger.relevant(colored_content)

        # 4 - Create the host config
        host_config = self._docker_client.create_host_config(
            privileged=project_emulation_object.privileged,
            binds=project_emulation_object.volumes,
            port_bindings=project_emulation_object.port_mapping,
            auto_remove=project_emulation_object.auto_remove,
            publish_all_ports=project_emulation_object.publish_all_ports,
            mem_limit=memory_limit,
        )

        # 5 - Connect the newly created container to the docker network
        aliases = [project_emulation_object.net_alias] if project_emulation_object.net_alias is not None else None

        # 6 - Create the container with the provided configurations
        container_result = self._docker_client.create_container(
            image=project_emulation_object.emulation_app_name,
            detach=False,
            host_config=host_config,
            ports=project_emulation_object.ports,
            name=container_name_in_the_network,
            entrypoint=project_emulation_object.entrypoint,
            stdin_open=project_emulation_object.attach,
            environment=environment_variables,
            command=project_emulation_object.arguments or [],
            tty=project_emulation_object.attach,
            volumes=[str(x) for x in file_volumes_to_add_to_container.values()],
            networking_config=self._docker_client.create_networking_config(
                {self._network_configuration.network_name: self._docker_client.create_endpoint_config(aliases=aliases)}
            ),
        )
        container = DockerContainer(
            id=container_result.get("Id", ""), image_name=project_emulation_object.emulation_app_name
        )

        # 6 - If there is a specific app configuration file, insert it into the container and override
        if container_result:
            self._override_emulation_configuration_file(
                container_id=container.id,
                temporary_directory_path=temporary_directory_path,
                project_emulation_object=project_emulation_object,
            )

        # 7 - Variables for logging purposes
        network_identification_name: str = self._network_configuration.network_name
        container_identification = f'"{container.id}" ("{project_emulation_object.emulation_app_name}")'
        logger.debug(f'Container {container_identification} connected to the "{network_identification_name}" network')

        # 8 - Jumpstart the app
        self._docker_client.start(container=container.id)
        message = f"Container {container_identification} successfully started"
        logger.debug(message)

        return True

    def _override_emulation_configuration_file(
        self, temporary_directory_path: KPath, container_id: str, project_emulation_object: ProjectEmulationObject
    ) -> bool:
        """
        Override the emulation configuration file and pass it into the container

        Parameters
        ----------
        temporary_directory_path : The temporary directory into which the configuration file output.
        container_id : the container id to override the app configuration file.
        project_emulation_object : the project emulation object used to assess generic information.

        Returns
        -------
        a boolean indicating whether or not the emulation configuration was successfully overwritten to the container.

        """
        config_model = project_emulation_object.app_config_model
        is_a_valid_kelvin_project = config_model is not None and config_model.app.app_type_configuration is not None

        if config_model and is_a_valid_kelvin_project and project_emulation_object.app_config_path:
            provided_app_yaml_path: KPath = KPath(project_emulation_object.app_config_path)
            target_file_path = self.setup_kelvin_broker_configuration(
                app_name=config_model.info.name.root_value,
                target_output_directory=temporary_directory_path,
                app_config_file_path=provided_app_yaml_path,
                project_type=config_model.app.type,
            )
            app_config_override = self.add_file_to_container(
                container_id=container_id,
                file_path=target_file_path,
                container_file_path=DockerConfigs.container_app_dir_path,
            )
            if app_config_override:
                logger.relevant(f'Overriding existing configuration with "{project_emulation_object.app_config_path}"')

        return True

    @staticmethod
    def setup_kelvin_broker_configuration(
        app_name: str,
        target_output_directory: KPath,
        app_config_file_path: KPath,
        project_type: ProjectType,
    ) -> KPath:
        """
        Setup the Kelvin Broker configuration.

        Parameters
        ----------
        app_name : the name of the application.
        target_output_directory : the directory into which the configuration file will be overridden.
        app_config_file_path : the app configuration file to override into the target output directory.
        project_type : the project type of the application to setup.

        Returns
        -------
        A KPath to the new app configuration file in the target output directory.

        """
        provided_app_yaml_configuration = app_config_file_path.read_yaml()
        override_app_config_file_path: KPath = target_output_directory / GeneralConfigs.default_app_config_file

        if not provided_app_yaml_configuration.get("app", {}).get(project_type.value_as_str, {}).get("mqtt", {}):
            url_metadata = session_manager.get_current_session_metadata()
            broker_app_name = url_metadata.sdk.components.kelvin_broker
            if not broker_app_name:
                session_manager.reset_session(ignore_destructive_warning=True)
                raise ValueError("Kelvin Broker is not available. Please authenticate.")
            broker_app_container_name = DockerImageNameDetails(
                registry_url=broker_app_name, docker_image_name=broker_app_name
            ).container_name

            kelvin_broker_configuration = Mqtt.default_mqtt_configuration(ip_address=broker_app_container_name)
            provided_app_yaml_configuration["app"][project_type.value_as_str]["mqtt"] = kelvin_broker_configuration

        if not provided_app_yaml_configuration.get("environment", {}):
            environment_config = Environment.default_environment_configuration(
                app_name=app_name, acp_name=EmulationConfigs.emulation_system_acp
            )
            provided_app_yaml_configuration["environment"] = environment_config

        override_app_config_file_path.write_yaml(yaml_data=provided_app_yaml_configuration)
        return override_app_config_file_path

    @ensure_docker_is_running
    def ensure_base_docker_images_exist(self, base_docker_image: str, base_data_model_builder: str) -> bool:
        """
        Using the base logged client, ensure that the provided images are valid in the currently logged registry.

        :param base_docker_image: the docker image used to build the application.
        :param base_data_model_builder: the docker image used to compile datatypes.

        :return: a boolean indicating whether the images are valid in the currently logged registry.
        """
        for image_name in [base_docker_image, base_data_model_builder]:
            try:
                self.pull_docker_image_from_registry(docker_image_name=image_name)
            except NotFound as exc:
                # 1 - if does not exist in the registry, look for it locally.
                if not self.check_if_docker_image_exists(docker_image_name=image_name, all_images=True):
                    raise exc
        return True

    @ensure_docker_is_running
    def push_docker_image_to_registry(self, docker_image_name: str) -> bool:
        """
        Push the specified docker image to the currently logged registry.

        :param docker_image_name: the name of the docker image to building.

        :return: a boolean indicating whether the image was successfully pushed to the currently logged registry.

        """
        image_name_details = DockerImageNameDetails(
            docker_image_name=docker_image_name, registry_url=self._credentials.full_registry_url
        )
        docker_image_name_for_registry = image_name_details.repository_docker_image_name

        if not self._docker_client.tag(docker_image_name, docker_image_name_for_registry, force=True):
            raise KDockerException(f"Error tagging {docker_image_name} to {docker_image_name_for_registry}")

        # Pushing operation
        auth_config: dict = {"username": self._credentials.username, "password": self._credentials.password}

        stream = self._docker_client.push(docker_image_name_for_registry, auth_config=auth_config, stream=True)

        # Display all the information from the stream
        display_docker_progress(stream=stream)

        # Once pushed, remove the docker image and proceed.
        # return self.remove_docker_image(docker_image_name=docker_image_name_for_registry)
        return True

    @ensure_docker_is_running
    def pull_docker_image_from_registry(self, docker_image_name: str, override_local_tag: bool = False) -> bool:
        """
        Pull the specified docker image from the currently logged registry.

        :param docker_image_name: the name of the docker image to be pulled.
        :param override_local_tag: if set, will indicate whether the pulled image should override the local tag.

        :return: a boolean indicating whether the image was successfully pulled to the currently logged registry.

        """
        auth_config = {"username": self._credentials.username, "password": self._credentials.password}

        # will yield a string with the format "<client>.kelvininc.com:5000/<image-name>:<image-version>"
        image_name_details = DockerImageNameDetails(
            docker_image_name=docker_image_name, registry_url=self._credentials.full_registry_url
        )
        docker_image_name_for_registry = image_name_details.repository_docker_image_name

        logger.info(f'Pulling "{docker_image_name}" from "{self._credentials.registry_url}"')

        try:
            stream = self._docker_client.pull(
                repository=docker_image_name_for_registry, auth_config=auth_config, stream=True
            )
            # Get both image names and version
            image_name, image_version = image_name_details.image_name_and_version
            # Display the stream progress
            display_docker_progress(stream=stream)
            logger.relevant(f'Successfully pulled "{docker_image_name}" from "{self._credentials.registry_url}"')
            if override_local_tag:
                self._docker_client.tag(
                    image=docker_image_name_for_registry, repository=image_name, tag=image_version, force=True
                )
            return True
        except NotFound:
            raise NotFound(
                f"""\n
                The provided app is not available in the platform's registry: \"{docker_image_name_for_registry}\". \n
                Please provide a valid combination of image and version. E.g \"hello-world:0.0.1\" \n
            """
            )
        except Exception as exc:
            raise KDockerException(message=f'Error pulling "{docker_image_name}": {str(exc)}')

    @ensure_docker_is_running
    def remove_docker_image(self, docker_image_name: str, silent: bool = False) -> bool:
        """
        Remove the specified docker image from the local system.

        Raise an exception if the docker image was not successfully removed.

        :param docker_image_name: the name of the docker image to be removed.
        :param silent: indicates whether logs should be displayed.

        :return: a boolean indicating whether the image was successfully removed.

        """
        # 1 - Check if the image exists. If not, raise the proper exception
        matching_images = self.get_docker_images(docker_image_name=docker_image_name)

        if not matching_images:
            raise KDockerException(f'Image "{docker_image_name}" does not exist')

        for image in matching_images:
            for tag in image.tags:
                # 2 - Stop the containers for the provided image
                self.stop_docker_containers_for_image(docker_image_name=tag)

                # 3 - attempt to remove the image
                docker_image_was_removed = self._docker_client.remove_image(tag, force=True)

                # 4 - transform the docker image result to a string
                removed_result_str = str(docker_image_was_removed) if docker_image_was_removed else None

                # 5 - verify if the success string is part of the result
                docker_image_was_removed = removed_result_str is not None and tag in removed_result_str

                if not docker_image_was_removed:
                    raise KDockerException(f'Error removing "{tag}"')

                if not silent:
                    logger.info(f'Image "{tag}" successfully removed')

        return True

    @ensure_docker_is_running
    def prune_docker_images(self, filters: dict = None) -> bool:
        """
        A simple wrapper around the client to prune dangling docker images.

        :param filters: the keywords used to filter out the prune operation.

        :return: a bool indicating the images were successfully pruned.
        """
        try:
            self._docker_client.prune_images(filters=filters)
            logger.debug("Images successfully pruned")
            return True
        except Exception:
            raise KDockerException("Error pruning images")

    @ensure_docker_is_running
    def check_if_docker_image_exists(
        self, docker_image_name: str, silent: bool = False, labels: Optional[dict] = None, all_images: bool = False
    ) -> bool:
        """
        Check whether the specified docker image exists on the local system.

        :param docker_image_name: the name of the docker image to be checked.
        :param silent: indicates whether logs should be displayed.
        :param labels: the labels to apply on the filter operation.
        :param all_images: if set to True, will bypass the labels and retrieve all images.

        :return: a boolean indicating whether the image exists on the local docker list.

        """
        docker_images = self.get_docker_images(
            docker_image_name=docker_image_name, labels=labels, all_images=all_images
        )
        if not silent:
            if docker_images:
                message = f'Image "{docker_image_name}" already exists'
            else:
                message = f'Image "{docker_image_name}" does not exist'
            logger.debug(message)

        return bool(docker_images)

    @ensure_docker_is_running
    def get_docker_images(
        self, docker_image_name: Optional[str] = None, labels: Optional[dict] = None, all_images: bool = False
    ) -> List[DockerImage]:
        """
        Return the list of all docker images in the local system.

        This image list can be narrowed down by using labels or an image name.
        By default, includes the standard: {'source': 'ksdk'} labels.

        Parameters
        ----------
        docker_image_name: the name of the docker image to be matched.
        labels: the labels used to get images. If not specified, will provide all the ksdk defaults.
        all_images: if set to 'True', will bypass the labels and retrieve all images.

        Returns
        -------
        a list of DockerImage items.

        """
        filters: Dict[str, Any] = {}
        if not all_images:
            identification_labels: dict = DockerConfigs.ksdk_base_identification_label

            if labels:
                if "name" in labels:
                    labels.pop("name", "")
                identification_labels = labels

            filters["label"] = [f"{key}={label}" for key, label in identification_labels.items()]
            if docker_image_name is not None:
                filters["reference"] = docker_image_name

        docker_images = self._docker_client.images(filters=filters, all=all_images)

        all_docker_images: List[DockerImage] = []

        for image in docker_images:
            image_id = image.get("Id", "")
            image_parent_id = image.get("ParentId", "")
            image_tags = image.get("RepoTags", []) or []
            image_created = image.get("Created", "")
            image_labels: dict = image.get("Labels", {}) or {}
            image_entry = DockerImage(
                id=image_id,
                parent_id=image_parent_id,
                tags=image_tags,
                created=image_created,
                labels=image_labels,
            )
            all_docker_images.append(image_entry)

        return all_docker_images

    @ensure_docker_is_running
    def unpack_app_from_docker_image(
        self,
        app_name: str,
        output_dir: str,
        image_dir: str = DockerConfigs.container_app_dir_path,
        clean_dir: bool = True,
    ) -> bool:
        """
        Extract the content of the specified built application to the provided output directory.

        :param app_name: the name of the application to unpack.
        :param output_dir: the directory into which the application will be unpacked.
        :param image_dir: the directory from which to extract the application content.
        :param clean_dir: clean the directory before extracting into it.

        :return: a boolean flag indicating the image was successfully unpacked.

        """
        default_unpack_app_name = "unpack"

        output_dir_path = KPath(output_dir)
        if clean_dir:
            output_dir_path.delete_dir().create_dir()
        else:
            output_dir_path.create_dir()

        self.remove_container(container=default_unpack_app_name)

        container = self._docker_client.create_container(
            image=app_name,
            stdin_open=True,
            name=default_unpack_app_name,
            entrypoint="tail",
            command=["-f", "/dev/null"],
        )
        container_object = DockerContainer(id=container.get("Id", ""), image_name=default_unpack_app_name)

        # try to extract application type app
        app_folder_extracted: bool = self.extract_folder_from_container(
            container_id=container_object.id, folder=image_dir, output_dir=output_dir
        )

        if not app_folder_extracted:
            logger.warning("The application unpack feature is not compatible with this application type")

        self._docker_client.remove_container(container=default_unpack_app_name)

        return app_folder_extracted

    def extract_folder_from_container(self, container_id: str, folder: str, output_dir: str) -> bool:
        unpack_temp_file = "app.tar"
        app_container_app_dir = DockerConfigs.app_container_app_dir

        try:
            stream, stat = self._docker_client.get_archive(container=container_id, path=folder)
            with TemporaryDirectory(dir=OSInfo.temp_dir) as temp_dir:
                app_tar_file = KPath(temp_dir) / unpack_temp_file

                with open(app_tar_file, "wb") as f:
                    for item in stream:
                        f.write(item)

                with tarfile.TarFile(app_tar_file) as tf:
                    for member in tf.getmembers():
                        if member.name.startswith(f"{app_container_app_dir}/"):
                            member.name = str(Path(member.name).relative_to(app_container_app_dir))
                    tf.extractall(path=output_dir)
        except DockerException:
            return False

        return True

    # 5 - CONTAINERS
    @ensure_docker_is_running
    def get_docker_containers(
        self,
        image_name: Optional[str] = None,
        container_name: Optional[str] = None,
        labels: Optional[dict] = None,
        all_containers: bool = False,
    ) -> List[DockerContainer]:
        """
        Obtain a list of all docker containers available in the system.

        This image list can be narrowed down by using labels or an image name.
        By default, includes the standard: {'source': 'ksdk'} labels.

        Parameters
        ----------
        image_name : the name of the docker image to filters the containers.
        container_name : the name of the docker container to filter.
        labels : the labels used to selectively get containers.
        all_containers : if set to 'True', will target all containers.

        Returns
        -------
        a list of DockerContainer items.

        """
        filters: Dict[str, Any] = {}
        if not all_containers:
            identification_labels: dict = DockerConfigs.ksdk_base_identification_label

            if labels:
                if "name" in labels:
                    labels.pop("name", "")
                identification_labels = labels

            filters = {"label": [f"{key}={label}" for key, label in identification_labels.items()]}

        if image_name:
            filters.update({"ancestor": image_name})
        if container_name:
            filters.update({"name": container_name})

        docker_containers = self._docker_client.containers(filters=filters, all=all_containers)

        all_docker_containers: List[DockerContainer] = []
        for container in docker_containers:
            container_id = container.get("Id", "")
            container_names: List[str] = [name.replace("/", "") for name in container.get("Names", []) or []]
            container_image = container.get("Image", "")
            container_is_running = container.get("State", "") == "running"
            container_labels: dict = container.get("Labels", {}) or {}
            container_ports: List = container.get("Ports", [])

            container_network_settings: dict = container.get("NetworkSettings", {})
            container_networks: dict = container_network_settings.get("Networks", {})
            container_network_ksdk: dict = container_networks.get(DockerConfigs.default_ksdk_network, {})
            container_network_ip: str = container_network_ksdk.get("IPAddress", "")

            container_entry = DockerContainer(
                id=container_id,
                container_names=[name.replace("/", "") for name in container_names],
                image_name=container_image,
                id_address=container_network_ip,
                running=container_is_running,
                ports=container_ports,
                labels=container_labels,
            )
            all_docker_containers.append(container_entry)

        return all_docker_containers

    @ensure_docker_is_running
    def add_file_to_container(self, container_id: str, file_path: KPath, container_file_path: str) -> bool:
        """
        Copy the provided file into a container.

        :para container: the id of the container to add the file into.
        :para file_path: the path of the file to be added.
        :para container_file_path: the path of the file inside the container.

        :return: a boolean indicating whether the file was successfully added to the container.
        """
        import time
        from io import BytesIO

        file_tar_stream = BytesIO()

        file_tar = tarfile.TarFile(fileobj=file_tar_stream, mode="w")
        with open(file_path.absolute(), "rb") as file:
            file_data = file.read()

        tarinfo = tarfile.TarInfo(name=file_path.name)
        tarinfo.size = len(file_data)
        tarinfo.mtime = int(time.time())

        file_tar.addfile(tarinfo, BytesIO(file_data))
        file_tar.close()
        file_tar_stream.seek(0)

        try:
            self._docker_client.get_archive(container=container_id, path=container_file_path)
        except NotFound:
            raise KDockerException(f"Application type is not compatible with configuration")

        return self._docker_client.put_archive(
            container=container_id, path=container_file_path, data=file_tar_stream.read()
        )

    @ensure_docker_is_running
    def stop_docker_containers_for_image(self, docker_image_name: str) -> bool:
        """
        Stop all the containers of the specified image.

        Parameters
        ----------
        docker_image_name : the name of docker image whose containers should be stopped.

        Returns
        -------
        a symbolic return boolean.

        """
        return self._stop_containers(image_name=docker_image_name)

    @ensure_docker_is_running
    def stop_docker_container_by_name(self, container_name: str) -> bool:
        """
        Stop the container using it's name.

        Parameters
        ----------
        container_name : the name of docker container to be stopped.

        Returns
        -------
        a symbolic return boolean.

        """
        return self._stop_containers(container_name=container_name)

    def _stop_containers(self, container_name: Optional[str] = None, image_name: Optional[str] = None) -> bool:
        """
        Internal method for stopping containers.

        Parameters
        ----------
        container_name : the container name, optional
        image_name : the image name, optional

        Returns
        -------
        a bool indicating whether the container(s) was successfully stopped

        """
        containers = self.get_docker_containers(
            container_name=container_name, image_name=image_name, all_containers=True
        )  # Target all containers
        if containers:
            running_containers = [container for container in containers if container.running]
            for container in running_containers:
                logger.info(f'Stopping container "{container.image_name}"')
                self._docker_client.stop(container=container.id)
            return True
        else:
            return False

    @ensure_docker_is_running
    def remove_container(self, container: str) -> bool:
        """
        Remove the provided container from the system.

        Parameters
        ----------
        container : the id of the container to be removed.

        Returns
        -------
        a default boolean indicating the container removal operation was successful.

        """
        all_containers = self.get_docker_containers(all_containers=True)  # include the stopped ones as well

        matching_container = [entry for entry in all_containers if container in entry.container_names]

        if matching_container:
            self._docker_client.remove_container(container=container, force=True)
            logger.debug("Container successfully removed")

        return True

    @ensure_docker_is_running
    def prune_docker_containers(self, filters: dict = None) -> bool:
        """
        A simple wrapper around the client to prune dangling docker containers.

        :param filters: the keywords used to filter out the prune operation.

        :return: a symbolic return flag.

        """
        try:
            self._docker_client.prune_containers(filters=filters)
            logger.debug("Containers successfully pruned")
            return True
        except (DockerException, Exception):
            raise KDockerException("Error pruning docker containers. Proceeding.")

    @ensure_docker_is_running
    def get_logs_for_docker_container(
        self, containers: List[DockerContainer], stream: bool = True, tail: Optional[int] = None, follow: bool = True
    ) -> Optional[Union[CancellableStream, str]]:
        """
        Prints out the logs of the containers of the specified docker image.

        :param containers: a list of containers to get the logs from.
        :param stream: if set to 'True', will return a stream response.
        :param tail: if set, will tail the logs and return.
        :param follow: if set to 'True', will follow the logs stream.

        :return: a symbolic return flag.

        """
        for docker_container in containers:
            logs = self._docker_client.logs(
                container=docker_container.id,
                stdout=True,
                stderr=True,
                stream=stream,
                tail=tail if tail else "all",
                timestamps=False,
                follow=follow,
            )

            return logs
        return None
