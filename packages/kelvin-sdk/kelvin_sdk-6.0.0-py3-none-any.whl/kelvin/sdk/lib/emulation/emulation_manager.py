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

from collections import defaultdict
from tempfile import TemporaryDirectory
from typing import Any, DefaultDict, List, Mapping, Optional, Sequence, Set, Union

from docker.types import CancellableStream

from kelvin.sdk.lib.api.appregistry import appregistry_download
from kelvin.sdk.lib.apps.local_apps_manager import app_images_unpack, project_build
from kelvin.sdk.lib.configs.internal.docker_configs import DockerConfigs
from kelvin.sdk.lib.configs.internal.emulation_configs import EmulationConfigs, StudioConfigs
from kelvin.sdk.lib.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.docker.docker_manager import DockerManager
from kelvin.sdk.lib.exceptions import EmulationException
from kelvin.sdk.lib.models.apps.common import NameDNS
from kelvin.sdk.lib.models.apps.kelvin_app import (
    IO,
    ApplicationInterface,
    ApplicationLanguage,
    ClientInterfaceType,
    DataType,
    Images,
    Interface,
    Item,
    Language,
    Metric,
    PythonLanguageType,
)
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import (
    App,
    Environment,
    Info,
    KelvinAppConfiguration,
    KelvinAppType,
    ProjectType,
)
from kelvin.sdk.lib.models.apps.ksdk_app_setup import ProjectEmulationObject
from kelvin.sdk.lib.models.factories.app_setup_configuration_objects_factory import get_default_app_name
from kelvin.sdk.lib.models.factories.docker_manager_factory import get_docker_manager
from kelvin.sdk.lib.models.generic import GenericObject, KPath, OSInfo
from kelvin.sdk.lib.models.ksdk_docker import AppRunningContainers, DockerContainer, DockerImage, KSDKDockerVolume
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.schema.schema_manager import get_latest_app_schema_version, validate_app_schema_from_app_config_file
from kelvin.sdk.lib.session.session_manager import session_manager
from kelvin.sdk.lib.utils.display_utils import display_data_entries
from kelvin.sdk.lib.utils.general_utils import chdir, open_link_in_browser
from kelvin.sdk.lib.utils.logger_utils import logger


def studio_start(
    schema_file: Optional[str] = None,
    input_file: Optional[str] = None,
    port: int = StudioConfigs.default_port,
) -> OperationResponse:
    """
    Starts Kelvin Studio to modify the provided input.

    Parameters
    ----------
    schema_file: the schema file used to power the Kelvin Studio's interface.
    input_file: the input file to modify based on the schema file..
    port: the studio server port.

    Returns
    -------
    an OperationResponse object encapsulating the result of the kelvin studio start.

    """
    try:
        studio_configs = StudioConfigs(port=port)
        if studio_configs.is_port_open():
            raise EmulationException(f"Port {studio_configs.port} already in use")

        # 1 - Load all the input files
        schema_file_path: KPath
        if not schema_file:
            _, _, schema_file_path = get_latest_app_schema_version()
        else:
            schema_file_path = KPath(schema_file)

        schema_file_path = schema_file_path.expanduser().resolve().absolute()

        if not schema_file_path.exists():
            raise FileNotFoundError(f"File not found {schema_file_path.absolute()}")

        default_app_yaml: str = GeneralConfigs.default_app_config_file
        input_file_path = KPath(input_file if input_file else default_app_yaml).expanduser().resolve().absolute()

        if not input_file_path or (input_file_path and not input_file_path.exists()):
            raise FileNotFoundError("Please provide a valid input file")

        logger.info("Starting Kelvin Studio")

        # 2 - setup the binds, port mapping and arguments
        volumes: List = []
        arguments: List = []
        if schema_file_path:
            studio_schema_file_bind = StudioConfigs.studio_schema_file_bind.format(
                schema_file_path=str(schema_file_path), schema_file_name=schema_file_path.name
            )
            volumes.append(studio_schema_file_bind)
            arguments.append(schema_file_path.name)
        if input_file_path:
            studio_input_file_bind = StudioConfigs.studio_input_file_bind.format(
                input_file_path=str(input_file_path), input_file_name=input_file_path.name
            )
            volumes.append(studio_input_file_bind)
            arguments.append(input_file_path.name)

            if input_file:
                logger.info(f'Configuring "{str(input_file)}"')

        url_metadata = session_manager.get_current_session_metadata()
        studio_app_name = url_metadata.sdk.components.kelvin_studio
        environment_variables = {}
        environment_variables.update({"docker_exposed_port": studio_configs.port})

        # 1 - Jumpstart the application
        docker_manager = get_docker_manager()
        docker_manager.pull_docker_image_from_registry(docker_image_name=studio_app_name)

        project_emulation_object = ProjectEmulationObject(
            app_name=studio_app_name,
            volumes=volumes,
            port_mapping={studio_configs.port: studio_configs.port},
            ports=[(studio_configs.port, "tcp")],
            arguments=arguments,
            environment_variables=environment_variables,
            is_external_app=True,
        )
        successfully_started = emulation_start(project_emulation_object=project_emulation_object)

        if successfully_started.success:
            browser_url = studio_configs.get_url()
            studio_start_success: str = f"""

                    Kelvin Studio successfully started!
                    Use your browser of choice to access it on: \"{browser_url}\"

                    Opening Kelvin Studio...

                """
            logger.relevant(studio_start_success)
            import time

            time.sleep(3)
            open_link_in_browser(browser_url)

        return successfully_started
    except Exception as exc:
        error_message = f"Error starting Kelvin Studio: {str(exc)}"
        logger.error(error_message)
        return OperationResponse(success=False, log=error_message)


def studio_stop() -> OperationResponse:
    """
    Stops a Kelvin Studio.

    Returns
    -------
    an OperationResponse object encapsulating the result of the kelvin studio stop.

    """
    try:
        logger.info("Stopping Kelvin Studio")

        url_metadata = session_manager.get_current_session_metadata()
        studio_app_name = url_metadata.sdk.components.kelvin_studio

        docker_manager = get_docker_manager()
        docker_manager.stop_docker_containers_for_image(docker_image_name=studio_app_name)

        message = "Kelvin Studio successfully stopped"
        logger.relevant(message)
        return OperationResponse(success=True, log=message)

    except Exception as exc:
        error_message = f"Error stopping Kelvin Studio: {str(exc)}"
        logger.error(error_message)
        return OperationResponse(success=False, log=error_message)


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
    try:
        project_emulation_object = load_base_emulation_object(
            app_name_with_version=app_name_with_version, app_config=app_config
        )
        project_emulation_object.show_logs = show_logs
        return emulation_start(project_emulation_object=project_emulation_object)
    except Exception as exc:
        error_message = f"Error emulating application:\n{str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def emulation_start_server(
    app_name_with_version: Optional[str] = None,
    app_config: Optional[str] = None,
    tail: Optional[int] = None,
    stream: bool = False,
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
    try:
        project_emulation_object = load_base_emulation_object(
            app_config=app_config, app_name_with_version=app_name_with_version
        )
        project_emulation_object.tail = tail
        project_emulation_object.stream = stream
        project_emulation_object.should_print = False
        project_emulation_object.follow = True
        project_emulation_object.show_logs = True

        if stream:
            from kelvin.sdk.server.utils.stream import build_stream_response

            return build_stream_response(emulation_start, project_emulation_object=project_emulation_object)

        return emulation_start(project_emulation_object=project_emulation_object)
    except Exception as exc:
        error_message = f"Error emulating application:\n{str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def emulation_start(project_emulation_object: ProjectEmulationObject) -> OperationResponse:
    """
    Start an application on the emulation system.

    - Start off by retrieving the current Docker Manager.
    - Setup and start the emulation system
    - Start the application.

    Parameters
    ----------
    project_emulation_object: the application's emulation object.

    Returns
    ----------
    an OperationResponse object indicating whether the app was successfully started.

    """
    try:
        docker_manager = get_docker_manager()

        _start_ksdk_emulation_system(docker_manager=docker_manager)

        return _raw_emulation_start(project_emulation_object=project_emulation_object, docker_manager=docker_manager)

    except Exception as exc:
        error_message = f"Error emulating application:\n{str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def _raw_emulation_start(
    project_emulation_object: ProjectEmulationObject, docker_manager: DockerManager
) -> OperationResponse:
    """
    Internal function.
    Assumes both KSDK Network and Broker are already up and running.
    Simply starts the applications

    Parameters
    ----------
    project_emulation_object: the application's emulation object.
    docker_manager : the object that encapsulates the docker utility instance.

    Returns
    ----------
    an OperationResponse object indicating whether the app was successfully started.

    """
    app_name = project_emulation_object.emulation_app_name

    logger.info(f'Loading configuration and starting the application "{app_name}"')

    # 1 - Check if the app exists
    application_exists = docker_manager.check_if_docker_image_exists(
        docker_image_name=app_name, all_images=project_emulation_object.is_external_app
    )

    if not application_exists:
        raise EmulationException(f'\tProvided application "{app_name}" not found\n')

    # 2 - If an app configuration is provided, its schema mus be validated.
    if project_emulation_object.app_config_path:
        validate_app_schema_from_app_config_file(app_config_file_path=KPath(project_emulation_object.app_config_path))

    # 3 - Run the image with the host config
    image_was_ran = docker_manager.run_app_docker_image(project_emulation_object=project_emulation_object)

    if not image_was_ran:
        raise EmulationException(f'Error starting pre-built application "{app_name}"')

    message = f'Application successfully launched: "{app_name}"'
    logger.relevant(message)

    if project_emulation_object.show_logs:
        return emulation_logs(
            app_name_with_version=app_name,
            tail=project_emulation_object.tail,
            should_print=project_emulation_object.should_print,
            stream=project_emulation_object.stream,
            follow=project_emulation_object.follow,
        )

    return OperationResponse(success=True, log=message)


def emulation_reset() -> OperationResponse:
    """
    Reset the emulation system.

    Returns
    ----------
    an OperationResponse object encapsulating the result of the emulation system reset.

    """
    try:
        logger.relevant("Resetting the Emulation System")
        images_and_containers = get_all_app_images_and_running_containers(should_display=False)
        container_data: AppRunningContainers = images_and_containers.data
        docker_manager = get_docker_manager()

        for container in container_data.existing_containers:
            emulation_stop(app_name_with_version=container.image_name)

        successfully_reset = _stop_ksdk_network(docker_manager=docker_manager)

        # Last but not least, purge the temporary directory for the emulation
        session_manager.get_global_ksdk_configuration().ksdk_temp_dir_path.delete_dir()
        success_message = "Emulation System successfully reset"
        logger.relevant(success_message)
        return OperationResponse(success=successfully_reset.success, log=success_message)

    except Exception as exc:
        error_message = f"Error resetting the Emulation System: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def emulation_stop(
    app_name_with_version: Optional[str], project_type: ProjectType = ProjectType.kelvin
) -> OperationResponse:
    """
    Stop a running application on the emulation system.

    Parameters
    ----------
    app_name_with_version: the name of the app to stop.
    project_type: the project type of the app to stop.

    Returns
    ----------
    an OperationResponse object encapsulating a message indicating whether the App was successfully stopped.

    """
    try:
        app_name = app_name_with_version or get_default_app_name()
        project_type_value = project_type.project_class_name().title()

        logger.info(f'Attempting to stop {project_type_value} "{app_name}"')

        docker_manager = get_docker_manager()

        if ".app" in app_name:
            container_stopped = docker_manager.stop_docker_container_by_name(container_name=app_name)
        else:
            container_stopped = docker_manager.stop_docker_containers_for_image(docker_image_name=app_name)

        result_message: str
        if container_stopped:
            result_message = f"{project_type_value} successfully stopped"
            logger.relevant(result_message)
        else:
            result_message = f"No running instances of the provided {project_type_value} were found"
            logger.warning(result_message)

        return OperationResponse(success=container_stopped, log=result_message)

    except Exception as exc:
        error_message = f"Error stopping {project_type.project_class_name()}: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def emulation_logs(
    app_name_with_version: Optional[str],
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
    should_print: indicates whether the logs should be printed.
    stream: indicates whether it should return the stream in the response.
    follow: indicates whether it should follow the logs stream.

    Returns
    -------
    an OperationResponse object indicating the logs were successfully obtained.

    """
    try:
        app_name_with_version = app_name_with_version or get_default_app_name()

        docker_manager = get_docker_manager()

        if ".app" in app_name_with_version:
            containers = docker_manager.get_docker_containers(container_name=app_name_with_version)
        else:
            containers = docker_manager.get_docker_containers(image_name=app_name_with_version)

        successful_logs = docker_manager.get_logs_for_docker_container(
            containers=containers, stream=stream, tail=tail, follow=follow
        )

        if not successful_logs:
            raise EmulationException(message=f'No logs found for the provided application "{app_name_with_version}"')

        if should_print:
            _print_log_stream(log_stream=successful_logs)
            return OperationResponse(success=True)

        if stream:
            return OperationResponse(success=True, stream=successful_logs)
        else:
            return OperationResponse(success=True, data=successful_logs)

    except Exception as exc:
        error_message = f"Error retrieving logs for the provided application: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def _print_log_stream(log_stream: Union[CancellableStream, str]) -> None:
    """
    Prints a log stream

    Parameters
    ----------
    log_stream : stream or a string containing the logs to print

    Returns
    -------
    Nothing

    """
    try:
        if isinstance(log_stream, str):
            logs = log_stream.split("\n")
            for item in logs:
                print(item)  # noqa
        elif isinstance(log_stream, bytes):
            logs = log_stream.decode("utf-8").split("\n")
            for item in logs:
                print(item)  # noqa
        else:
            for item in log_stream:
                print(item.decode("utf-8"), end="")  # type: ignore # noqa: T001
    except Exception as exc:
        logger.error(f'Error processing logs: "{str(exc)}"')


def get_all_app_images_and_running_containers(should_display: bool = False) -> OperationResponse:
    """
    Retrieve the list of all application images as well as its running.

    Will yield 2 tables: the first containing the existing Apps and the second containing all the running
    processes.

    Parameters
    ----------
    should_display: specifies whether or not output data should be displayed.

    Returns
    ----------
    an OperationResponse object wrapping the result of the existing app images and containers.

    """
    try:
        ksdk_labels = DockerConfigs.ksdk_base_identification_label

        docker_manager = get_docker_manager()
        existing_ksdk_images: List[DockerImage] = docker_manager.get_docker_images(labels=ksdk_labels)
        existing_ksdk_containers: List[DockerContainer] = docker_manager.get_docker_containers(labels=ksdk_labels)
        running_ksdk_containers = [container for container in existing_ksdk_containers if container.running]

        filtered_ksdk_images = [
            GenericObject(data={"tag": tag, "readable_created_date": image.readable_created_date})
            for image in existing_ksdk_images
            if any("<none>" not in tag for tag in image.tags)
            for tag in image.tags
        ]

        if should_display:
            display_data_entries(
                data=filtered_ksdk_images,
                header_names=["Applications", "Created"],
                attributes=["tag", "readable_created_date"],
                table_title=GeneralConfigs.table_title.format(title="Existing Apps"),
                no_data_message="No application available on the local registry",
            )
            display_data_entries(
                data=running_ksdk_containers,
                header_names=[
                    "Running applications",
                    "Containers",
                    "Up and running",
                    "Local IP Address",
                    "Ports (container->host)",
                ],
                attributes=["image_name", "container_names", "running", "id_address", "ports"],
                table_title=GeneralConfigs.table_title.format(title="Running Apps"),
                no_data_message="No applications running",
            )

        containers = AppRunningContainers(
            existing_images=existing_ksdk_images, existing_containers=existing_ksdk_containers
        )
        return OperationResponse(success=True, data=containers)

    except Exception as exc:
        error_message = f"Error retrieving application information: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, data=AppRunningContainers())


def emulation_inject(
    input_file: Sequence[str],
    app_name: Sequence[str],
    period: float,
    repeat: bool,
    ignore_timestamps: bool,
    acp_name: Optional[str] = None,
    workload_name: Optional[str] = None,
) -> OperationResponse:
    """
    Start the embedded Injector app that will inject data into the emulation system.

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
    -------
    an OperationResponse object indicating whether the injector was successfully started.

    """
    filenames = [KPath(x).resolve() for x in input_file]
    root = min(x.parent for x in filenames)

    return _build_data_app(
        app_name=EmulationConfigs.injector_app_name,
        entry_point=EmulationConfigs.injector_app_entry_point,
        image_names=app_name,
        routing=EmulationConfigs.injector_app_routing,
        period=period,
        data_files=filenames,
        configuration=[
            IO(
                name=EmulationConfigs.injector_app_name,
                data_type=EmulationConfigs.injector_app_config_data_type,
                values=[
                    Item(
                        name=EmulationConfigs.injector_param_filenames,
                        value=[f"data/{x.relative_to(root)}" for x in filenames],
                    ),
                    Item(name=EmulationConfigs.injector_param_repeat, value=repeat),
                    Item(
                        name=EmulationConfigs.injector_param_ignore_timestamps,
                        value=ignore_timestamps,
                    ),
                ],
            )
        ],
        environment=Environment(acp_name=acp_name, workload_name=workload_name),
    )


def emulation_extract(app_name: Sequence[str], shared_dir: str, batch: float) -> OperationResponse:
    """
    Start the embedded Extractor app that will extract data from the emulation system.

    Parameters
    ----------
    app_name: the sequence of apps to extract data from.
    shared_dir: the directory shared between the container and the host machine.
    batch: the extractor batch write frequency.

    Returns
    -------
    an OperationResponse object indicating whether the extractor was successfully started.

    """
    output_path = f"{DockerConfigs.container_app_shared_dir_path}/output"

    return _build_data_app(
        app_name=EmulationConfigs.extractor_app_name,
        entry_point=EmulationConfigs.extractor_app_entry_point,
        image_names=app_name,
        routing=EmulationConfigs.extractor_app_routing,
        configuration=[
            IO(
                name=EmulationConfigs.extractor_app_name,
                data_type=EmulationConfigs.extractor_app_config_data_type,
                values=[
                    Item(name=EmulationConfigs.extractor_param_batch, value=batch),
                    Item(name=EmulationConfigs.extractor_param_output_path, value=output_path),
                ],
            ),
        ],
        shared_dir=shared_dir,
    )


def _build_data_app(
    app_name: str,
    entry_point: str,
    image_names: Sequence[str],
    routing: Mapping[str, str],
    period: float = 1.0,
    data_files: Optional[Sequence[KPath]] = None,
    configuration: Optional[List[IO]] = None,
    shared_dir: Optional[str] = None,
    environment: Optional[Environment] = None,
) -> OperationResponse:
    """Build data app (e.g. injector/extractor)"""

    app_data_failure: str = "Error building data application: {image_name}: {reason}"

    app_dir = DockerConfigs.container_app_dir_path
    app_config_filename = GeneralConfigs.default_app_config_file

    image_app_config_filename = f"{app_dir}/{app_config_filename}"
    image_data_type_dir = f"{app_dir}/{GeneralConfigs.default_datatype_dir}"

    data_types: List[DataType] = []
    data_type_versions: DefaultDict[str, Set[str]] = defaultdict(set)
    io: DefaultDict[str, List[Metric]] = defaultdict(list)

    acp_names: Set[str] = {*[]}
    workload_names: Set[str] = {*[]}

    try:
        docker_manager = get_docker_manager()
        url_metadata = session_manager.get_current_session_metadata()

        with TemporaryDirectory(dir=OSInfo.temp_dir) as temp_dir:
            cache_dir = KPath(temp_dir)
            data_type_dir = cache_dir / GeneralConfigs.default_datatype_dir
            data_type_dir.mkdir()

            # extract inputs across target apps
            for image_name in image_names:
                image_exists = docker_manager.check_if_docker_image_exists(docker_image_name=image_name)
                if not image_exists:
                    if ":" not in image_name:
                        error_message = f'App name must include version: "{image_name}"'
                        logger.error(error_message)
                        return OperationResponse(success=False, log=error_message)
                    result: OperationResponse = appregistry_download(image_name, override_local_tag=True)
                    if not result.success:
                        return OperationResponse(success=False)

                # get app config
                result = app_images_unpack(image_name, str(cache_dir), image_dir=image_app_config_filename)
                if not result.success:
                    return OperationResponse(success=False)

                # get data types
                result = app_images_unpack(image_name, str(cache_dir), image_dir=image_data_type_dir, clean_dir=False)
                if not result.success:
                    return OperationResponse(success=False)

                app_config_file = cache_dir / app_config_filename
                try:
                    kelvin_app_config: KelvinAppConfiguration = KelvinAppConfiguration.parse_obj(
                        app_config_file.read_yaml()
                    )
                except Exception as e:
                    error_message = app_data_failure.format(image_name=image_name, reason=e)
                    logger.exception(error_message)
                    return OperationResponse(success=False, log=error_message)

                if kelvin_app_config.app.type != ProjectType.kelvin:
                    wrong_app_type: str = app_data_failure.format(
                        image_name=image_name, reason=f"app type: {kelvin_app_config.app.type.name}"
                    )
                    logger.error(wrong_app_type)
                    return OperationResponse(success=False, log=wrong_app_type)

                if kelvin_app_config.app.kelvin is None:
                    missing_kelvin_app_config: str = app_data_failure.format(
                        image_name=image_name, reason="missing kelvin app config"
                    )
                    logger.error(missing_kelvin_app_config)
                    return OperationResponse(success=False, log=missing_kelvin_app_config)

                app_config: KelvinAppType = kelvin_app_config.app.kelvin

                if app_config.data_types is not None:
                    data_type: DataType
                    for data_type in app_config.data_types:
                        versions = data_type_versions[str(data_type.name)]
                        n = len(versions)
                        versions |= {str(data_type.version)}
                        if len(versions) > n:
                            data_types += [data_type]

                for source, target in routing.items():
                    metrics = getattr(app_config, source, None)
                    if metrics is None:
                        continue

                    metric: Metric
                    for metric in metrics:
                        metric.sources, metric.targets = metric.targets, metric.sources
                        io[target] += [metric]
                        if metric.targets is not None:
                            for metric_info in metric.targets:
                                if metric_info.acp_names:
                                    acp_names |= {str(x) for x in metric_info.acp_names}
                                if metric_info.workload_names:
                                    workload_names |= {str(x) for x in metric_info.workload_names}

            acp_name = acp_names.pop() if len(acp_names) == 1 else None
            workload_name = workload_names.pop() if len(workload_names) == 1 else None

            if environment is not None:
                if not environment.acp_name and acp_name is not None:
                    environment.acp_name = NameDNS.parse_obj(acp_name)
                if not environment.workload_name and workload_name is not None:
                    environment.workload_name = NameDNS.parse_obj(workload_name)
            else:
                environment = Environment(acp_name=acp_name, workload_name=workload_name)

            data_type_dupes = "\n".join(
                f"  - {k}: {', '.join(sorted(v))}" for k, v in data_type_versions.items() if len(v) > 1
            )
            if data_type_dupes:
                error_message = f'Duplicated data types with differing versions:\n"{data_type_dupes}"'
                logger.error(error_message)
                return OperationResponse(success=False, log=error_message)

            kelvin_app_config = KelvinAppConfiguration(
                spec_version=url_metadata.kelvin_schema.latest_spec_version,
                info=Info(
                    name=app_name,
                    title=app_name,
                    description=app_name,
                    version="0.0.0",
                ),
                environment=environment,
                app=App(
                    type=ProjectType.kelvin,
                    kelvin=KelvinAppType(
                        images=Images(base="", builder=""),
                        system_packages=[],
                        data_types=data_types,
                        interface=Interface(
                            type=ApplicationInterface.client,
                            client=ClientInterfaceType(
                                period=period,
                                executable="run_app",
                                args=[],
                                spawn=True,
                            ),
                        ),
                        language=Language(
                            type=ApplicationLanguage.python,
                            python=PythonLanguageType(
                                entry_point=entry_point,
                                requirements=str(cache_dir / "requirements.txt"),
                            ),
                        ),
                        **io,
                    ),
                ),
            )

            if kelvin_app_config.app.kelvin is not None:
                kelvin_app_config.app.kelvin.configuration = configuration

            cache_dir_app_config_file: KPath = cache_dir / app_config_filename
            kelvin_app_config.to_file(path=cache_dir_app_config_file)

            cache_dir_requirements_file: KPath = cache_dir / GeneralConfigs.default_requirements_file
            cache_dir_requirements_file.write_text(GeneralConfigs.default_kelvin_app_dependency)

            if data_files is not None:
                cache_dir_data_dir: KPath = cache_dir / GeneralConfigs.default_data_dir
                cache_dir_data_dir.create_dir()
                root = min(x.parent for x in data_files)
                for x in data_files:
                    x.clone_into(cache_dir_data_dir / x.relative_to(root))

            with chdir(cache_dir):
                result = project_build(temp_dir)
                if not result.success:
                    return OperationResponse(success=False)

            volumes = []
            if shared_dir:
                shared_dir_path = KPath(shared_dir).absolute()
                shared_data_bind = DockerConfigs.container_app_shared_dir_bind
                shared_data_bind = shared_data_bind.format(shared_dir_path=shared_dir_path)
                volumes.append(shared_data_bind)

            project_emulation_object = ProjectEmulationObject(
                app_name=app_name,
                volumes=volumes,
                show_logs=True,
                is_external_app=True,
            )
            return emulation_start(project_emulation_object=project_emulation_object)

    except Exception as exc:
        str_image_names = ", ".join(image_names)
        error_message = f"Error building data application: {str_image_names}: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def load_base_emulation_object(
    app_name_with_version: Optional[str] = None, app_config: Optional[str] = None
) -> ProjectEmulationObject:
    """
    Loads the app emulation object from the config file.
    If none is provided, load it from the app name.

    Parameters
    ----------
    app_name_with_version : the application's name.
    app_config : the app configuration file to be used on the emulation.

    Returns
    -------
    An ProjectEmulationObject ready for consumption.

    """
    project_emulation_object: ProjectEmulationObject
    app_config_file_path: Optional[KPath] = KPath(app_config).expanduser().resolve() if app_config else None
    context_app_config_file = app_config or GeneralConfigs.default_app_config_file
    context_app_config_file_path: KPath = KPath(context_app_config_file).expanduser().resolve()

    if app_name_with_version:
        logger.relevant(f'Attempting to launch application "{app_name_with_version}" on the emulation system')
        if app_config_file_path and app_config_file_path.exists():
            logger.relevant(f'Emulation configuration loaded from: "{app_config_file_path.absolute()}"')
            project_emulation_object = ProjectEmulationObject.from_app_model(app_config_file_path=app_config_file_path)
            if app_name_with_version != project_emulation_object.app_name:
                different_versions = f"{app_name_with_version} <> {project_emulation_object.app_name}"
                raise ValueError(f"The provided configuration does not match application: {different_versions}")
        else:
            logger.warning(f'Starting "{app_name_with_version}" without configurations')
            project_emulation_object = ProjectEmulationObject(app_name=app_name_with_version)
    elif context_app_config_file_path.exists():
        logger.relevant(f'Emulation configuration loaded from: "{context_app_config_file_path.absolute()}"')
        project_emulation_object = ProjectEmulationObject.from_app_model(
            app_config_file_path=context_app_config_file_path
        )
    else:
        raise EmulationException("Please provide an application name or an application configuration file")

    return project_emulation_object


# Emulation System: Network & Broker
def _start_ksdk_emulation_system(docker_manager: DockerManager) -> OperationResponse:
    """
    Start the KSDK Emulation System.
    Jumpstart the KSDK network as well as the Kelvin Broker.

    Parameters
    ----------
    docker_manager : the object that encapsulates the docker utility instance.

    Returns
    -------
    an OperationResponse object encapsulating the result of the KSDK Emulation System setup and start.

    """
    try:
        network_started = _start_ksdk_network(docker_manager=docker_manager)

        broker_started = _start_ksdk_broker(docker_manager=docker_manager)

        result_message: str = "Kelvin Emulation System is online"
        logger.relevant(result_message)

        return OperationResponse(success=network_started.success and broker_started.success, log=result_message)
    except Exception as exc:
        raise EmulationException(f"Error starting Kelvin Emulation System: {exc}")


def _start_ksdk_network(docker_manager: DockerManager) -> OperationResponse:
    """
    Start the KSDK network of the provided DockerManager.

    Parameters
    ----------
    docker_manager : the object that encapsulates the docker utility instance.

    Returns
    -------
    a boolean indicating whether the ksdk network was successfully started.
    """
    network_id = docker_manager.get_docker_network_id()
    network_already_running = bool(network_id)

    if network_already_running:
        network_already_running_message: str = "Kelvin Network already running"
        logger.debug(network_already_running_message)
        return OperationResponse(success=True, log=network_already_running_message)
    else:
        logger.debug("Starting the Kelvin Network")
        network_successfully_started = docker_manager.create_docker_network()
        success_message = "Kelvin Network successfully started"
        logger.relevant(success_message)
        return OperationResponse(success=network_successfully_started, log=success_message)


def _stop_ksdk_network(docker_manager: DockerManager) -> OperationResponse:
    """
    Stop the KSDK network of the provided DockerManager.

    Parameters
    ----------
    docker_manager : the object that encapsulates the docker utility instance.

    Returns
    -------
    a boolean indicating whether the ksdk network was successfully stopped.
    """
    logger.debug("Stopping the Kelvin Network")

    # Remove the 'ksdk' docker network
    network_removed = docker_manager.remove_docker_network()
    # Remove "dangling" containers
    containers_pruned = docker_manager.prune_docker_containers()
    # Remove "dangling" images
    images_pruned = docker_manager.prune_docker_images()

    network_successfully_stopped = network_removed and containers_pruned and images_pruned
    if network_successfully_stopped:
        result_message: str = "Kelvin Network successfully stopped"
        logger.debug(result_message)
    else:
        result_message = "Error stopping the Kelvin Network"
        logger.error(result_message)

    return OperationResponse(success=True, log=result_message)


def _start_ksdk_broker(docker_manager: DockerManager) -> OperationResponse:
    """
    Start the dedicated Kelvin Broker for application communication.

    Parameters
    ----------
    docker_manager : the object that encapsulates the docker utility instance.

    Returns
    -------
    a boolean indicating whether the kelvin broker was successfully started.

    """
    # 1 - Retrieve the kelvin broker name
    url_metadata = session_manager.get_current_session_metadata()
    broker_app_name = url_metadata.sdk.components.kelvin_broker

    # 2 - Pull to ensure the broker is available
    all_broker_apps = docker_manager.get_docker_containers(image_name=broker_app_name, all_containers=True)
    running_broker_apps = [broker_app for broker_app in all_broker_apps if broker_app.running]

    if running_broker_apps:
        success_message = "Kelvin Broker already running"
        logger.debug(success_message)
        return OperationResponse(success=True, log=success_message)
    else:
        logger.debug("Initializing the Kelvin Broker")
        docker_manager.pull_docker_image_from_registry(docker_image_name=broker_app_name)
        project_emulation_object = ProjectEmulationObject(
            app_name=broker_app_name,
            is_external_app=True,
            file_volumes=[
                KSDKDockerVolume(
                    source_file_path=KPath(GeneralConfigs.default_mqtt_config_file),
                    container_file_path=GeneralConfigs.default_mqtt_config_file,
                    content="listener 1883\nallow_anonymous true",
                )
            ],
        )
        successfully_started = _raw_emulation_start(
            project_emulation_object=project_emulation_object, docker_manager=docker_manager
        )

        if successfully_started.success:
            result_message = "Kelvin Broker successfully initialized"
            logger.debug(result_message)
        else:
            result_message = "Error initializing the Kelvin Broker"
            logger.exception(result_message)

        return OperationResponse(success=successfully_started.success, log=result_message)
