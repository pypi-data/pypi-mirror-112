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

from fastapi import APIRouter, Body

from kelvin.sdk.lib.models.apps.ksdk_app_setup import ProjectCreationParametersObject
from kelvin.sdk.lib.models.operation import OperationResponse

router = APIRouter(
    prefix="/apps",
    tags=["apps"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def app_images_list() -> OperationResponse:
    """
    Retrieve the list of all application images as well as its running.

    Will yield 2 tables: the first containing the existing Apps and the second containing all the running
    processes.
    """
    from kelvin.sdk.interface import app_images_list as _app_images_list

    return _app_images_list(should_display=False)


@router.post("/")
def app_create(project_creation_parameters: ProjectCreationParametersObject) -> OperationResponse:
    """
    The entry point for the creation of an application. (Parameters)

    - Creates the directory that will contain the app app.
    - Creates all necessary base files for the development of the app.
    """

    from kelvin.sdk.interface import app_create as _app_create

    return _app_create(project_creation_parameters=project_creation_parameters)


@router.delete("/")
def app_images_remove(app_name_with_version: str) -> OperationResponse:
    """
    Remove the specified application from the existing image list (in the docker instance).
    """
    from kelvin.sdk.interface import app_images_remove as _app_images_remove

    return _app_images_remove(app_name_with_version=app_name_with_version)


@router.post("/build")
def app_build(app_dir_absolute_path: str = Body(...), fresh_build: bool = Body(False)) -> OperationResponse:
    """
    The entry point for the building of a App.

    Package the App on the provided app directory.
    """
    from kelvin.sdk.interface import app_build as _app_build

    return _app_build(app_dir=app_dir_absolute_path, fresh_build=fresh_build)


@router.post("/migrate")
def app_migrate(app_dir_absolute_path: str) -> OperationResponse:
    """
    Migrate the application configuration to the new schema version.
    """
    from kelvin.sdk.interface import app_migrate as _app_migrate

    return _app_migrate(app_dir=app_dir_absolute_path)


@router.post("/unpack")
def app_images_unpack(app_name_with_version: str = Body(...), output_dir: str = Body(...)) -> OperationResponse:
    """
    Extract the content of an application from its built image.
    """
    from kelvin.sdk.interface import app_images_unpack as _app_images_unpack

    return _app_images_unpack(app_name_with_version=app_name_with_version, output_dir=output_dir)
