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

from kelvin.sdk.lib.models.apps.kelvin_app import ApplicationLanguage
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import ProjectType
from kelvin.sdk.lib.models.apps.ksdk_app_setup import ProjectCreationParametersObject
from kelvin.sdk.lib.models.operation import OperationResponse


def app_create_from_wizard() -> OperationResponse:
    """
    The entry point for the creation of an application. (WizardTree)

    Usually initiated when no parameters are provided.

    - Creates the directory that will contain the app app.
    - Creates all necessary base files for the development of the app.

    Returns
    -------
    an OperationResponse object wrapping the result of the creation of the application.

    """
    from kelvin.sdk.lib.apps.local_apps_manager import app_create_from_wizard as _project_create_from_wizard

    return _project_create_from_wizard()


@typechecked
def app_create_from_parameters(
    app_dir: str,
    app_name: str,
    app_description: Optional[str],
    app_type: Optional[ProjectType],
    kelvin_app_lang: Optional[ApplicationLanguage],
) -> OperationResponse:
    """
    The entry point for the creation of an application. (Parameters)

    - Creates the directory that will contain the app app.
    - Creates all necessary base files for the development of the app.

    Parameters
    ----------
    app_dir: the app's targeted dir. Will contain all the application files.
    app_name: the name of the new app.
    app_description: the description of the new app.
    app_type: the type of the new application. # E.g. 'docker', 'kelvin'.
    kelvin_app_lang: the language the new app will be written on. For kelvin apps only. # E.g. python.

    Returns
    ----------
    an OperationResponse object wrapping the result of the creation of the application.

    """
    from kelvin.sdk.lib.apps.local_apps_manager import app_create_from_parameters as _project_create_from_parameters

    return _project_create_from_parameters(
        app_dir=app_dir,
        app_name=app_name,
        app_description=app_description,
        app_type=app_type,
        kelvin_app_lang=kelvin_app_lang,
    )


@typechecked
def app_create(project_creation_parameters: ProjectCreationParametersObject) -> OperationResponse:
    """
    The entry point for the creation of an application. (Parameters)

    - Creates the directory that will contain the app app.
    - Creates all necessary base files for the development of the app.

    Parameters
    ----------
    project_creation_parameters: the object containing all the required variables for App creation.

    Returns
    ----------
    an OperationResponse object wrapping the result of the creation of the application.
    """

    from kelvin.sdk.lib.apps.local_apps_manager import project_create as _project_create

    return _project_create(project_creation_parameters=project_creation_parameters)


@typechecked
def app_build(app_dir: str, fresh_build: bool = False) -> OperationResponse:
    """
    The entry point for the building of a App.

    Package the App on the provided app directory.

    Parameters
    ----------
    app_dir: the path where the application is hosted.
    fresh_build: If specified will remove any cache and rebuild the application from scratch.

    Returns
    ----------
    an OperationResponse object wrapping the result of the application build process.

    """
    from kelvin.sdk.lib.apps.local_apps_manager import project_build as _project_build

    return _project_build(app_dir=app_dir, fresh_build=fresh_build)


@typechecked
def app_migrate(app_dir: str) -> OperationResponse:
    """
    Migrate the application configuration to the new schema version.

    Parameters
    ----------
    app_dir: the path to the application that requires migrate.

    Returns
    ----------
    an OperationResponse object wrapping the result of the application migration process.

    """
    from kelvin.sdk.lib.apps.local_apps_manager import app_migrate as _app_migrate

    return _app_migrate(app_dir=app_dir)


@typechecked
def app_images_list(should_display: bool = False) -> OperationResponse:
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
    from kelvin.sdk.lib.emulation.emulation_manager import get_all_app_images_and_running_containers

    return get_all_app_images_and_running_containers(should_display=should_display)


@typechecked
def app_images_remove(app_name_with_version: str) -> OperationResponse:
    """
    Remove the specified application from the existing image list (in the docker instance).

    Parameters
    ----------
    app_name_with_version: the app to be removed. Must include the version.

    Returns
    ----------
    an OperationResponse object wrapping the result of the application image removal operation.

    """
    from kelvin.sdk.lib.apps.local_apps_manager import app_images_remove as _app_images_remove

    return _app_images_remove(app_name_with_version=app_name_with_version)


@typechecked
def app_images_unpack(app_name_with_version: str, output_dir: str) -> OperationResponse:
    """
    Extract the content of an application from its built image.

    Parameters
    ----------
    app_name_with_version: the name of the image to unpack the app from.
    output_dir: the output directory to output the application content.

    Returns
    ----------
    an OperationResponse object wrapping the result of the application image unpack operation.

    """
    from kelvin.sdk.lib.apps.local_apps_manager import app_images_unpack as _app_images_unpack

    return _app_images_unpack(app_name_with_version=app_name_with_version, output_dir=output_dir)
