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
from typing import Any, Dict, List, Optional

from kelvin.sdk.lib.exceptions import InvalidApplicationConfiguration
from kelvin.sdk.lib.legacy.kelvin_app import get_legacy_app_object
from kelvin.sdk.lib.legacy.models.ksdk_app import DataModel as DataModelLegacy
from kelvin.sdk.lib.legacy.models.ksdk_app import IOLegacy
from kelvin.sdk.lib.legacy.models.ksdk_app import KelvinAppConfiguration as KelvinAppConfigurationLegacy
from kelvin.sdk.lib.models.apps.docker_app import DockerAppType
from kelvin.sdk.lib.models.apps.kelvin_app import DataType, KelvinAppType, Metric
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import App, KelvinAppConfiguration, ProjectType
from kelvin.sdk.lib.models.generic import KPath
from kelvin.sdk.lib.schema.schema_manager import get_latest_app_schema_version


def migrate_app_configuration(app_dir_path: str, output_file_path: KPath) -> Optional[KelvinAppConfiguration]:
    """
    When provided with a path to an old project, return the migrated, corresponding KelvinAppConfiguration.

    :param app_dir_path: the path to the directory that holds the outdated app.
    :param output_file_path: the output file path where the new configuration should be written.

    :return: a new, up-to-date KelvinAppConfiguration object.

    """
    # 1 - load app configuration
    app_configuration_legacy: KelvinAppConfigurationLegacy = get_legacy_app_object(app_dir=app_dir_path)

    app_config: App = App(type=ProjectType[app_configuration_legacy.app.type.value_as_str])

    latest_schema_version, _, _ = get_latest_app_schema_version()

    # 2 - migrate app
    if app_config.type is ProjectType.kelvin:
        # migrate ios
        if app_configuration_legacy.app.kelvin and app_configuration_legacy.app.kelvin.core:
            inputs = build_ios(ios=app_configuration_legacy.app.kelvin.core.inputs, content="sources")
            outputs = build_ios(ios=app_configuration_legacy.app.kelvin.core.outputs, content="targets")
            # migrate datamodels to data_types
            data_types = build_data_types(datamodels=app_configuration_legacy.app.kelvin.core.data_models)

            language = app_configuration_legacy.app.kelvin.core.language

            kelvin_app_type: Dict[str, Any] = {"language": language.dict()}

            if len(inputs) > 0:
                kelvin_app_type.update({"inputs": inputs})
            if len(outputs) > 0:
                kelvin_app_type.update({"outputs": outputs})
            if len(data_types) > 0:
                kelvin_app_type.update({"data_types": data_types})

            system_packages = app_configuration_legacy.app.kelvin.system_packages
            if system_packages and (len(system_packages) > 0):
                kelvin_app_type.update({"system_packages": app_configuration_legacy.app.kelvin.system_packages})

            app_config.kelvin = KelvinAppType(**kelvin_app_type)
    elif app_config.type is ProjectType.docker:
        # migrate docker apps
        if app_configuration_legacy.app.docker and app_configuration_legacy.app.docker.build:
            app_config.docker = DockerAppType(**app_configuration_legacy.app.docker.build.dict())
        else:
            raise InvalidApplicationConfiguration(
                message="App cannot be migrated. "
                "Context docker applications are no longer supported. Please use a Dockerfile"
            )

    system: Optional[Dict[str, Any]] = (
        app_configuration_legacy.system.dict() if app_configuration_legacy.system else None
    )

    # define new configuration
    kelvin_app_configuration = KelvinAppConfiguration(
        **{
            "spec_version": latest_schema_version,
            "info": app_configuration_legacy.info.dict(),
            "system": system,
            "app": app_config,
        }
    )
    kelvin_app_configuration.to_file(output_file_path)
    return kelvin_app_configuration


def build_ios(ios: List[IOLegacy], content: str) -> List[Metric]:
    """Create a current list of io dicts from a legacy io instances

    Parameters
    ----------
    io: List[IOLegacy]
        - a list of legacy IO instances
    content: str
        if the ios list contains inputs use "sources" else "targets".
        Check `kelvin.sdk.lib.models.apps.kelvin_app.Metric`

    Returns
    -------
        Dict
            A list of io dicts from a legacy io instance
    """
    return [Metric(**build_io_data(io=io, content=content)) for io in ios]


def build_io_data(io: IOLegacy, content: str) -> Dict:
    """Create a current io dict from a legacy io instance

    Parameters
    ----------
    io: IOLegacy
        - a legacy IO instance
    content: str
        if the ios list contains inputs use "sources" else "targets".
        Check `kelvin.sdk.lib.models.apps.kelvin_app.Metric`

    Returns
    -------
        Dict
            An io dict from a legacy io instance
    """
    return {"name": str(io.name), "data_type": str(io.data_model), content: [{"workload_names": [], "asset_names": []}]}


def build_data_types(datamodels: List[DataModelLegacy]) -> List[DataType]:
    return [DataType(**datamodel.dict()) for datamodel in datamodels if "raw." not in str(datamodel.name)]
