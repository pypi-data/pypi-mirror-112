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

import pathlib
from typing import Dict, List, Optional, cast

from kelvin.sdk.lib.configs.internal.docker_configs import DockerConfigs
from kelvin.sdk.lib.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.exceptions import InvalidApplicationConfiguration
from kelvin.sdk.lib.models.apps.kelvin_app import ApplicationLanguage, KelvinAppType
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import KelvinAppConfiguration, ProjectType
from kelvin.sdk.lib.models.apps.ksdk_app_setup import (
    BridgeAppBuildingObject,
    DockerAppCreationObject,
    File,
    KelvinAppBuildingObject,
    KelvinAppCreationObject,
    ModelServiceCreationObject,
    ProjectBuildingObject,
    ProjectCreationObject,
    ProjectCreationParametersObject,
    TemplateFile,
)
from kelvin.sdk.lib.models.generic import KPath, NameWithVersion
from kelvin.sdk.lib.models.ksdk_global_configuration import SDKMetadataEntry
from kelvin.sdk.lib.models.types import FileType
from kelvin.sdk.lib.schema.schema_manager import generate_base_schema_template
from kelvin.sdk.lib.session.session_manager import session_manager
from kelvin.sdk.lib.templates.templates_manager import get_project_templates
from kelvin.sdk.lib.utils.general_utils import check_if_image_is_allowed_on_platform, dict_to_yaml, standardize_string
from kelvin.sdk.lib.utils.pypi_utils import get_pypi_credentials


# Creation - Apps
def get_kelvin_app_creation_object(
    project_creation_parameters: ProjectCreationParametersObject,
) -> ProjectCreationObject:
    """
    Creates a KelvinAppCreationObject from the specified parameters.
    This object will encapsulate all the necessary variables for the creation of an application, thus resulting in
    reduced and more testable code.

    :param project_creation_parameters: the object containing all the required variables for App creation.

    :return: a KelvinAppCreationObject containing all the necessary variables for the creation of the application.

    """

    app_name = project_creation_parameters.app_name
    dir_path = project_creation_parameters.app_dir
    app_type = project_creation_parameters.app_type
    kelvin_app_lang = project_creation_parameters.kelvin_app_lang
    kelvin_app_interface = project_creation_parameters.kelvin_app_interface

    app_config_file = GeneralConfigs.default_app_config_file
    app_file_system_name = standardize_string(value=app_name)

    app_root_dir_path: KPath = KPath(dir_path) / app_name
    app_source_dir_path: KPath = app_root_dir_path / app_file_system_name
    app_file_path: KPath = app_source_dir_path / f"{app_file_system_name}{kelvin_app_lang.get_extension()}"

    relative_source_app_file_path: KPath = app_file_path.relative_to(app_root_dir_path)
    app_entry_point = str(pathlib.PurePosixPath(relative_source_app_file_path)).replace(".cpp", ".so")

    # 1 - Configuration files, app dir and files
    parameters: dict = {
        "app_name": app_name,
        "app_title": app_name,
        "app_lang": kelvin_app_lang.value,
        "app_description": GeneralConfigs.default_app_description,
        "app_version": GeneralConfigs.default_app_version,
        "app_file_system_name": app_file_system_name,
        "app_lang_extension": kelvin_app_lang.get_extension(),
        "app_type": app_type.value,
        "kelvin_app_interface": kelvin_app_interface.value if kelvin_app_interface else None,
        "kelvin_app_lang": kelvin_app_lang.value,
        "cpp_app_header_extension": ".h",
        "app_entry_point": app_entry_point,
        "app_config_file": app_config_file,
    }

    # 2 - Setup the base paths for each app sub folder in the app
    build_dir_path = app_root_dir_path / GeneralConfigs.default_build_dir
    data_dir_path: KPath = app_root_dir_path / GeneralConfigs.default_data_dir
    datatype_dir_path: KPath = app_root_dir_path / GeneralConfigs.default_datatype_dir
    docs_dir_path = app_root_dir_path / GeneralConfigs.default_docs_dir
    tests_dir_path = app_root_dir_path / GeneralConfigs.default_tests_dir
    wheels_dir_path = app_root_dir_path / GeneralConfigs.default_wheels_dir

    # 2 - Retrieve the templates for the files of each folder
    configuration_files_templates: List[TemplateFile] = get_project_templates(
        project_type=app_type,
        kelvin_app_lang=kelvin_app_lang,
        kelvin_app_interface=kelvin_app_interface,
        file_type=FileType.CONFIGURATION,
    )

    application_files_templates: List[TemplateFile] = get_project_templates(
        project_type=app_type,
        kelvin_app_lang=kelvin_app_lang,
        kelvin_app_interface=kelvin_app_interface,
        file_type=FileType.APP,
    )

    data_files_templates: List[TemplateFile] = get_project_templates(
        project_type=app_type,
        kelvin_app_lang=kelvin_app_lang,
        kelvin_app_interface=kelvin_app_interface,
        file_type=FileType.DATA,
    )

    datatype_files_templates: List[TemplateFile] = get_project_templates(
        project_type=app_type,
        kelvin_app_lang=kelvin_app_lang,
        kelvin_app_interface=kelvin_app_interface,
        file_type=FileType.DATATYPE,
    )

    docs_files_templates: List[TemplateFile] = get_project_templates(
        project_type=app_type,
        kelvin_app_lang=kelvin_app_lang,
        kelvin_app_interface=kelvin_app_interface,
        file_type=FileType.DOCS,
    )

    test_files_templates: List[TemplateFile] = get_project_templates(
        project_type=app_type,
        kelvin_app_lang=kelvin_app_lang,
        kelvin_app_interface=kelvin_app_interface,
        file_type=FileType.TESTS,
    )

    wheels_files_templates: List[TemplateFile] = get_project_templates(
        project_type=app_type,
        kelvin_app_lang=kelvin_app_lang,
        kelvin_app_interface=kelvin_app_interface,
        file_type=FileType.WHEELS,
    )

    # 3 - Render the templates and produce File objects for each template
    configuration_files: List[File] = _get_files_from_templates(
        directory=app_root_dir_path, templates=configuration_files_templates, render_params=parameters
    )

    app_config_file_path: KPath = app_root_dir_path / app_config_file
    app_configuration = generate_base_schema_template(project_creation_parameters_object=project_creation_parameters)
    app_configuration_yaml: str = dict_to_yaml(content=app_configuration)
    configuration_files.append(File(file=app_config_file_path, content=app_configuration_yaml))

    application_files: List[File] = _get_files_from_templates(
        directory=app_source_dir_path, templates=application_files_templates, render_params=parameters
    )

    data_dir_path_files: List[File] = _get_files_from_templates(
        directory=data_dir_path, templates=data_files_templates, render_params={}
    )

    docs_dir_path_files: List[File] = _get_files_from_templates(
        directory=docs_dir_path, templates=docs_files_templates, render_params={}
    )

    datatype_dir_path_files: List[File] = _get_files_from_templates(
        directory=datatype_dir_path, templates=datatype_files_templates, render_params={}
    )

    test_dir_path_files: List[File] = _get_files_from_templates(
        directory=tests_dir_path, templates=test_files_templates, render_params=parameters
    )

    wheels_dir_path_files: List[File] = _get_files_from_templates(
        directory=wheels_dir_path, templates=wheels_files_templates, render_params=parameters
    )

    # 4 - Include all the file templates into their respective folders
    app_root_dir_object: dict = {"directory": app_root_dir_path, "files": configuration_files}
    app_dir_object: dict = {"directory": app_source_dir_path, "files": application_files}
    build_dir_object: dict = {"directory": build_dir_path}
    data_dir_object: dict = {"directory": data_dir_path, "files": data_dir_path_files}
    datatype_dir_object: dict = {"directory": datatype_dir_path, "files": datatype_dir_path_files}
    docs_dir_object: dict = {"directory": docs_dir_path, "files": docs_dir_path_files}
    tests_dir_object: dict = {"directory": tests_dir_path, "files": test_dir_path_files}
    wheels_dir_object: dict = {"directory": wheels_dir_path, "files": wheels_dir_path_files}

    # 5 - build the final KelvinAppCreationObject
    return KelvinAppCreationObject(
        **{
            "app_root_dir": app_root_dir_object,
            "app_dir": app_dir_object,
            "build_dir": build_dir_object,
            "data_dir": data_dir_object,
            "datatype_dir": datatype_dir_object,
            "docs_dir": docs_dir_object,
            "tests_dir": tests_dir_object,
            "wheels_dir": wheels_dir_object,
        }
    )


def get_docker_app_creation_object(
    project_creation_parameters: ProjectCreationParametersObject,
) -> ProjectCreationObject:
    """
    Creates a KelvinAppCreationObject from the specified parameters.
    This object will encapsulate all the necessary variables for the creation of an application, thus resulting in
    reduced and more testable code.

    :param project_creation_parameters: the object containing all the required variables for App creation.

    :return: a KelvinAppCreationObject containing all the necessary variables for the creation of the application.

    """
    # Setup variables
    app_name = project_creation_parameters.app_name
    app_description = project_creation_parameters.app_description
    dir_path = project_creation_parameters.app_dir

    app_config_file = GeneralConfigs.default_app_config_file
    app_root_dir_path: KPath = KPath(dir_path) / app_name

    # 1 - Configuration files, app dir and files
    parameters: dict = {
        "app_name": app_name,
        "app_description": app_description,
        "app_version": GeneralConfigs.default_app_version,
        "app_config_file": app_config_file,
    }

    # 2 - Retrieve the templates for the files of each folder
    configuration_files_templates: List[TemplateFile] = get_project_templates(
        project_type=project_creation_parameters.app_type,
        kelvin_app_lang=project_creation_parameters.kelvin_app_lang,
        kelvin_app_interface=project_creation_parameters.kelvin_app_interface,
        file_type=FileType.CONFIGURATION,
    )

    # 3 - Render the templates and produce File objects for each template
    configuration_files: List[File] = _get_files_from_templates(
        directory=app_root_dir_path, templates=configuration_files_templates, render_params=parameters
    )

    app_config_file_path: KPath = app_root_dir_path / app_config_file
    app_configuration = generate_base_schema_template(project_creation_parameters_object=project_creation_parameters)
    app_configuration_yaml: str = dict_to_yaml(content=app_configuration)
    configuration_files.append(File(file=app_config_file_path, content=app_configuration_yaml))

    # 4 - Include all the file templates into their respective folders
    app_root_dir_object: dict = {"directory": app_root_dir_path, "files": configuration_files}

    # 5 - build the final KelvinAppCreationObject
    return DockerAppCreationObject(
        **{
            "app_root_dir": app_root_dir_object,
        }
    )


def get_model_service_creation_object(
    project_creation_parameters: ProjectCreationParametersObject,
) -> ProjectCreationObject:
    """
    Creates a ProjectCreationObject (ModelServiceCreationObject) from the specified parameters.
    This object will encapsulate all the necessary variables for the creation of ModelService application,
    thus resulting in reduced and more testable code.

    :param project_creation_parameters: the object containing all the required variables for App creation.

    :return: a ModelServiceCreationObject containing all the necessary variables for the creation of the application.

    """
    # Setup variables
    app_name = project_creation_parameters.app_name
    app_description = project_creation_parameters.app_description
    dir_path = project_creation_parameters.app_dir

    app_root_dir_path: KPath = KPath(dir_path) / app_name
    app_config_file = GeneralConfigs.default_app_config_file
    app_config_file_path: KPath = app_root_dir_path / app_config_file

    app_dir_path = app_root_dir_path / GeneralConfigs.default_app_dir
    app_server_dir_path = app_dir_path / GeneralConfigs.default_server_dir
    tests_dir_path: KPath = app_root_dir_path / GeneralConfigs.default_tests_dir
    artifacts_dir_path: KPath = app_root_dir_path / GeneralConfigs.default_artifacts_dir

    # 1 - Configuration files, app dir and files
    parameters: dict = {
        "app_name": app_name,
        "app_description": app_description,
        "app_version": GeneralConfigs.default_app_version,
        "app_config_file": app_config_file,
        "python_dependencies": " ".join(GeneralConfigs.default_model_service_dependencies),
        "model_service_module": GeneralConfigs.default_model_service_module,
        "model_service_yaml_file": GeneralConfigs.default_model_service_yaml_file,
        "requirements_file": GeneralConfigs.default_requirements_file,
        "title": app_name.title(),
    }

    # 2 - Retrieve the templates for the files of each folder
    configuration_files_templates: List[TemplateFile] = get_project_templates(
        project_type=project_creation_parameters.app_type,
        kelvin_app_lang=project_creation_parameters.kelvin_app_lang,
        kelvin_app_interface=project_creation_parameters.kelvin_app_interface,
        file_type=FileType.CONFIGURATION,
    )

    application_files_templates: List[TemplateFile] = get_project_templates(
        project_type=project_creation_parameters.app_type,
        kelvin_app_lang=project_creation_parameters.kelvin_app_lang,
        kelvin_app_interface=project_creation_parameters.kelvin_app_interface,
        file_type=FileType.APP,
    )

    application_server_files_templates: List[TemplateFile] = get_project_templates(
        project_type=project_creation_parameters.app_type,
        kelvin_app_lang=project_creation_parameters.kelvin_app_lang,
        kelvin_app_interface=project_creation_parameters.kelvin_app_interface,
        file_type=FileType.APP_MODULE,
    )

    test_files_templates: List[TemplateFile] = get_project_templates(
        project_type=project_creation_parameters.app_type,
        kelvin_app_lang=project_creation_parameters.kelvin_app_lang,
        kelvin_app_interface=project_creation_parameters.kelvin_app_interface,
        file_type=FileType.TESTS,
    )

    # 3 - Render the templates and produce File objects for each template
    configuration_files: List[File] = _get_files_from_templates(
        directory=app_root_dir_path, templates=configuration_files_templates, render_params=parameters
    )

    application_files: List[File] = _get_files_from_templates(
        directory=app_dir_path, templates=application_files_templates, render_params=parameters
    )

    server_files: List[File] = _get_files_from_templates(
        directory=app_server_dir_path, templates=application_server_files_templates, render_params=parameters
    )

    test_files: List[File] = _get_files_from_templates(
        directory=tests_dir_path, templates=test_files_templates, render_params=parameters
    )

    project_creation_parameters.app_type = ProjectType.docker
    app_configuration = generate_base_schema_template(project_creation_parameters_object=project_creation_parameters)
    app_configuration_yaml: str = dict_to_yaml(content=app_configuration)
    configuration_files.append(File(file=app_config_file_path, content=app_configuration_yaml))

    # 4 - Include all the file templates into their respective folders
    app_root_dir_object: dict = {"directory": app_root_dir_path, "files": configuration_files}
    app_server_dir_object: dict = {"directory": app_server_dir_path, "files": server_files}
    app_dir_object: dict = {"directory": app_dir_path, "files": application_files}
    artifacts_dir_object: dict = {"directory": artifacts_dir_path, "files": []}
    tests_dir_object: dict = {"directory": tests_dir_path, "files": test_files}

    # 5 - build the final ModelServiceCreationObject
    return ModelServiceCreationObject(
        **{
            "app_root_dir": app_root_dir_object,
            "app_server_dir": app_server_dir_object,
            "app_dir": app_dir_object,
            "artifacts_dir": artifacts_dir_object,
            "tests_dir": tests_dir_object,
        }
    )


def _get_files_from_templates(directory: KPath, templates: List[TemplateFile], render_params: Dict) -> List[File]:
    """
    When provided with a directory, a list of templates and additional parameters, render the templates with the render
    parameters and create File objects with the associated directory.

    :param directory: the directory to associate to each new File object.
    :param templates: the templates to render.
    :param render_params: the parameters to render the templates with.

    :return: a list of File objects
    """
    files_return_result = []

    for template in templates:
        render_params = render_params or {}
        file_name = template.name.format_map(render_params) if render_params else template.name
        file_content = template.content.render(render_params)
        file_path = directory / file_name
        files_return_result.append(File(file=file_path, content=file_content, **template.options))

    return files_return_result


def get_project_building_object(app_dir: str, fresh_build: bool = False) -> ProjectBuildingObject:
    """
    Create a ProjectBuildingObject from the provided app directory.

    This object will encapsulate all the necessary variables for the building of a base application, thus resulting
    in reduced, cleaner and more testable code.

    :param app_dir: the path to the application's dir.
    :param fresh_build: If specified will remove any cache and rebuild the application from scratch.

    :return: a ProjectBuildingObject containing all the necessary variables for the building of a base app.

    """
    app_dir_path: KPath = KPath(app_dir).expanduser().resolve()
    app_config_file_path: KPath = app_dir_path / GeneralConfigs.default_app_config_file
    app_build_dir_path: KPath = app_dir_path / GeneralConfigs.default_build_dir
    app_config_raw = app_config_file_path.read_yaml()
    app_config_model = KelvinAppConfiguration(**app_config_raw)
    docker_image_labels = DockerConfigs.ksdk_app_identification_label
    app_name = str(app_config_model.info.name)
    app_version = str(app_config_model.info.version)
    docker_image_name = app_name
    docker_image_labels["name"] = NameWithVersion(name=app_name, version=app_version).full_name
    docker_image_labels["type"] = app_config_model.app.type.value_as_str
    base_app_build_object = ProjectBuildingObject(
        # base building object
        fresh_build=fresh_build,
        app_config_file_path=app_config_file_path,
        app_config_raw=app_config_raw,
        app_config_model=app_config_model,
        app_dir_path=app_dir_path,
        app_build_dir_path=app_build_dir_path,
        docker_image_labels=docker_image_labels,
        docker_image_name=docker_image_name,
    )
    return base_app_build_object


def get_kelvin_app_building_object(
    app_dir: str,
    app_config_raw: Optional[Dict] = None,
    fresh_build: bool = False,
    build_for_upload: bool = False,
    upload_datatypes: bool = False,
) -> KelvinAppBuildingObject:
    """
    Creates a KelvinAppBuildingObject from the specified parameters.

    This object will encapsulate all the necessary variables for the building of a kelvin application, thus resulting
    in reduced, cleaner and more testable code.

    :param app_dir: the path to the application's dir.
    :param app_config_raw: the raw app configuration dictionary.
    :param fresh_build: If specified will remove any cache and rebuild the application from scratch.
    :param build_for_upload: indicates whether or the package object aims for an upload.
    :param upload_datatypes: If specified, will upload locally defined datatypes.

    :return: a KelvinAppBuildingObject containing all the necessary variables for the building of a kelvin application.

    """
    # 1 - building a temp dir to copy the files into
    app_dir_path: KPath = KPath(app_dir)
    app_build_dir_path: KPath = app_dir_path / GeneralConfigs.default_build_dir
    app_datatype_dir_path: KPath = app_build_dir_path / GeneralConfigs.default_datatype_dir
    app_config_file_path: KPath = app_dir_path / GeneralConfigs.default_app_config_file
    app_config_raw = app_config_raw or app_config_file_path.read_yaml()
    app_config_model = KelvinAppConfiguration(**app_config_raw)
    app_name = str(app_config_model.info.name)
    app_version = str(app_config_model.info.version)
    dockerfile_path: KPath = app_build_dir_path / GeneralConfigs.default_dockerfile

    kelvin_app_object: Optional[KelvinAppType] = app_config_model.app.app_type_configuration
    if not kelvin_app_object:
        raise InvalidApplicationConfiguration()

    app_lang = ApplicationLanguage(kelvin_app_object.language.type)

    # Retrieve the metadata
    metadata_sdk_config: Optional[SDKMetadataEntry]
    registry_url: Optional[str]
    try:
        site_metadata = session_manager.get_current_session_metadata()
        registry_url = site_metadata.docker.full_docker_registry_url
        metadata_sdk_config = site_metadata.sdk
    except Exception:
        metadata_sdk_config = None
        registry_url = None

    # Setup the images
    base_data_model_builder_image: Optional[str] = None
    base_image: Optional[str] = None
    if kelvin_app_object.images:
        base_data_model_builder_image = kelvin_app_object.images.builder
        base_image = kelvin_app_object.images.base
    if not base_data_model_builder_image and metadata_sdk_config:
        base_data_model_builder_image = metadata_sdk_config.core.base_data_model_builder_image
    if not base_image and metadata_sdk_config:
        base_image = metadata_sdk_config.core.get_docker_image_for_lang(app_lang=app_lang)
    # Stop the process from going any further
    if not base_data_model_builder_image:
        raise ValueError(
            """No data type builder image provided.

            1) Please login on a valid platform to retrieve the recommended version,
            or
            2) Provide one in the app.yaml under \"images -> builder\".

        """
        )
    if not base_image:
        raise ValueError(
            """No base image provided.

            1) Please login on a valid platform to retrieve the recommended version,
            or
            2) Provide one in the app.yaml under \"images -> base\".

        """
        )

    check_if_image_is_allowed_on_platform(registry_url=registry_url, docker_image_name=base_data_model_builder_image)
    check_if_image_is_allowed_on_platform(registry_url=registry_url, docker_image_name=base_image)

    docker_image_name = app_name
    docker_image_version = app_version
    docker_image_labels = DockerConfigs.ksdk_app_identification_label
    docker_image_labels["name"] = NameWithVersion(name=app_name, version=app_version).full_name
    docker_image_labels["type"] = app_config_model.app.type.value_as_str

    build_args = {}
    if app_lang == ApplicationLanguage.python:
        build_args.update(get_pypi_credentials())

    return KelvinAppBuildingObject(
        # base building object
        fresh_build=fresh_build,
        build_for_upload=build_for_upload,
        upload_datatypes=upload_datatypes,
        app_config_file_path=app_config_file_path,
        app_config_raw=app_config_raw,
        app_config_model=app_config_model,
        app_dir_path=app_dir_path,
        app_build_dir_path=app_build_dir_path,
        docker_image_labels=docker_image_labels,
        docker_image_name=docker_image_name,
        # kelvin app building object
        dockerfile_path=dockerfile_path,
        docker_build_context_path=app_dir_path,
        base_image=base_image,
        base_data_model_builder_image=base_data_model_builder_image,
        docker_image_version=docker_image_version,
        build_args=build_args,
        app_datatype_dir_path=app_datatype_dir_path,
    )


def get_bridge_app_building_object(
    app_dir: str,
    app_config_raw: Optional[Dict] = None,
    fresh_build: bool = False,
    build_for_upload: bool = False,
    upload_datatypes: bool = False,
) -> BridgeAppBuildingObject:
    """
    Creates a BridgeAppBuildingObject from the specified parameters.

    This object will encapsulate all the necessary variables for the building of a kelvin application, thus resulting
    in reduced, cleaner and more testable code.

    Parameters
    ----------
    app_dir: the path to the application's dir.
    app_config_raw: the raw app configuration dictionary.
    fresh_build: If specified will remove any cache and rebuild the application from scratch.
    build_for_upload: indicates whether or the package object aims for an upload.
    upload_datatypes: If specified, will upload locally defined datatypes.

    Returns
    -------
    a BridgeAppBuildingObject containing all the necessary variables for the building of a kelvin application.

    """
    kelvin_app_building_object = get_kelvin_app_building_object(
        app_dir=app_dir,
        app_config_raw=app_config_raw,
        fresh_build=fresh_build,
        build_for_upload=build_for_upload,
        upload_datatypes=upload_datatypes,
    )
    return cast(BridgeAppBuildingObject, kelvin_app_building_object)


def get_default_app_configuration(
    app_dir_path: Optional[KPath] = None, app_config_file_path: Optional[KPath] = None
) -> KelvinAppConfiguration:
    """
    Retrieve the application's configuration from either the provided app directory of app configuration.

    :param app_dir_path: the path to the application's directory.
    :param app_config_file_path: the path to the application's configuration.

    :return: a KelvinAppConfiguration object matching the app configuration of the app.

    """
    if app_config_file_path:
        return KelvinAppConfiguration(**app_config_file_path.read_yaml())

    app_config_file_path_aux = KPath(GeneralConfigs.default_app_config_file)

    if app_dir_path:
        app_config_file_path_aux = app_dir_path / app_config_file_path

    return KelvinAppConfiguration(**app_config_file_path_aux.read_yaml())


def get_default_app_name(app_dir_path: Optional[KPath] = None) -> str:
    """
    Retrieve the app name from the default configuration file (usually, app.yaml)

    :param app_dir_path: the path to the application's directory.

    :return: a string  containing the default app name.

    """
    app_configuration = get_default_app_configuration(app_dir_path=app_dir_path)

    return app_configuration.info.app_name_with_version
