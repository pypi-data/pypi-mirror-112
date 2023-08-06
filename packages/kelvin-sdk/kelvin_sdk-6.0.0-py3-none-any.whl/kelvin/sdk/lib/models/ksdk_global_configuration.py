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

from __future__ import annotations

from typing import Any, Mapping, Optional, Tuple

from pydantic import Field, validator

from kelvin.sdk.lib.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.models.apps.kelvin_app import ApplicationLanguage
from kelvin.sdk.lib.models.generic import KPath, KSDKModel, KSDKSettings
from kelvin.sdk.lib.models.types import LogType, TableFormat


# 1 - Metadata oriented classes
class GenericMetadataEntry(KSDKModel):
    url: Optional[str] = None
    path: Optional[str] = None
    realm: Optional[str] = None
    port: Optional[str] = None
    client_id: Optional[str] = None


class DockerMetadataEntry(GenericMetadataEntry):
    @property
    def full_docker_registry_url(self) -> str:
        return f"{self.url}:{self.port}"


class SchemaMetadataEntry(GenericMetadataEntry):
    minimum_spec_version: str
    latest_spec_version: str


class CoreMetadataEntry(GenericMetadataEntry):
    base_image_python: str
    base_image_cpp: str
    base_data_model_builder_image: str

    def get_docker_image_for_lang(self, app_lang: Optional[ApplicationLanguage] = None) -> str:
        if app_lang and app_lang == ApplicationLanguage.cpp:
            return self.base_image_cpp
        return self.base_image_python


class ComponentsMetadataEntry(GenericMetadataEntry):
    kelvin_broker: str = Field(None, alias="kelvin-mqtt-broker")
    kelvin_studio: str = Field(None, alias="kelvin-studio")


class SDKMetadataEntry(GenericMetadataEntry):
    docker_minimum_version: Optional[str]
    ksdk_minimum_version: str
    ksdk_latest_version: str
    core: CoreMetadataEntry
    components: ComponentsMetadataEntry


class CompanyMetadata(KSDKModel):
    authentication: GenericMetadataEntry
    docker: DockerMetadataEntry
    documentation: GenericMetadataEntry
    sdk: SDKMetadataEntry
    kelvin_schema: SchemaMetadataEntry = Field(None, alias="schema")

    def get_min_and_latest_schema_versions(self) -> Tuple[str, str]:
        """
        Return the latest schema version from the metadata.

        :return: the tuple including both minimum and latest versions allowed from the schema.

        """
        minimum, latest = self.kelvin_schema.minimum_spec_version, self.kelvin_schema.latest_spec_version
        if latest < minimum:
            minimum = latest
        return minimum, latest


# 2 - Top level configuration classes
class KelvinSDKEnvironmentVariables(KSDKSettings):
    ksdk_version_warning: bool = True
    ksdk_docker_image_version_warning: bool = True
    ksdk_verbose_mode: bool = False
    ksdk_output_type: str = LogType.KSDK.value_as_str
    ksdk_colored_logs: bool = True
    ksdk_shell: bool = False
    ksdk_debug: bool = False
    ksdk_table_format: TableFormat = TableFormat.psql

    class Config:
        fields = {
            "ksdk_version_warning": {
                "env": "KSDK_VERSION_WARNING",
                "description": "If outdated, KSDK will warn the user. If the minimum version is not respected, "
                "it will block any operation until upgrade.",
            },
            "ksdk_docker_image_version_warning": {
                "env": "KSDK_DOCKER_IMAGE_VERSION_WARNING",
                "description": "Will warn the user if the base docker image present on the `app.yaml` is deprecated.",
            },
            "ksdk_verbose_mode": {
                "env": "KSDK_VERBOSE_MODE",
                "description": "If set to True, will activate --verbose mode by default on every command.",
            },
            "ksdk_output_type": {
                "env": "KSDK_OUTPUT_TYPE",
                "description": "Sets the output type: KSDK or JSON.",
            },
            "ksdk_colored_logs": {
                "env": "KSDK_COLORED_LOGS",
                "description": "If disabled, all logs will be output in the default OS color, ready to be captured.",
            },
            "ksdk_shell": {
                "env": "KSDK_SHELL",
                "description": "Enable built-in command shell.",
            },
            "ksdk_debug": {
                "env": "KSDK_DEBUG",
                "description": "If enabled, display debug information for errors.",
            },
            "ksdk_table_format": {
                "env": "KSDK_TABLE_FORMAT",
                "description": 'Set the table format for all data display operations. Check "tabulate" pypi page.',
            },
        }

    @validator(
        "ksdk_version_warning",
        "ksdk_docker_image_version_warning",
        "ksdk_verbose_mode",
        "ksdk_colored_logs",
        "ksdk_debug",
        pre=True,
    )
    def invalid_value(cls, v: Any, field: Any) -> Any:  # noqa
        if v is None or v in ["True", "False", "1", "0", True, False, 1, 0]:
            return v
        return False

    @validator(
        "ksdk_output_type",
        pre=True,
    )
    def invalid_output_type_value(cls, v: Any) -> Any:  # noqa
        if v in LogType.as_list():
            return v
        return LogType.KSDK.value_as_str

    @validator(
        "ksdk_table_format",
        pre=True,
    )
    def invalid_table_format_value(cls, v: Any) -> TableFormat:  # noqa
        if isinstance(v, TableFormat):
            return v
        elif isinstance(v, str):
            return TableFormat(v)
        return TableFormat.psql

    @property
    def descriptions(self) -> dict:
        fields = KelvinSDKEnvironmentVariables.Config.fields
        for k, v in self.dict().items():
            fields[k]["current_value"] = v
        return fields

    @property
    def private_fields(self) -> list:
        return ["ksdk_debug"]

    def dict(self, *args: Any, **kwargs: Any) -> Mapping[str, Any]:  # type: ignore
        result = super().dict(*args, **kwargs)
        table_format = result["ksdk_table_format"]
        result["ksdk_table_format"] = table_format.value if isinstance(table_format, TableFormat) else table_format
        return result


class KelvinSDKConfiguration(KSDKSettings):
    last_metadata_refresh: float
    current_url: str
    current_user: str
    ksdk_current_version: str
    ksdk_minimum_version: str
    ksdk_latest_version: str
    configurations: KelvinSDKEnvironmentVariables = KelvinSDKEnvironmentVariables()

    @validator(
        "configurations",
        pre=True,
    )
    def validate_configurations(cls, v: Any) -> KelvinSDKEnvironmentVariables:  # noqa
        return v if v is not None else KelvinSDKEnvironmentVariables()

    @property
    def versions(self) -> dict:
        return {
            "current_version": self.ksdk_current_version,
            "minimum_version": self.ksdk_minimum_version,
            "latest_version": self.ksdk_latest_version,
        }

    def reset(self) -> Any:
        self.current_url = ""
        self.current_user = ""
        return self

    @classmethod
    def from_file(cls, ksdk_config_file_path: KPath) -> Any:
        from kelvin.sdk.cli.version import version

        ksdk_config_dict = ksdk_config_file_path.read_yaml(verbose=False) if ksdk_config_file_path else {}
        ksdk_config_dict.update({"ksdk_current_version": version})
        return cls(**ksdk_config_dict)

    @classmethod
    def default_constructor(cls) -> KelvinSDKConfiguration:
        from kelvin.sdk.cli.version import version

        return cls(
            last_metadata_refresh=0,
            current_url="",
            current_user="",
            ksdk_current_version=version,
            ksdk_minimum_version=version,
            ksdk_latest_version=version,
        )


class KelvinSDKGlobalConfiguration(KSDKSettings):
    ksdk_config_dir_path: KPath
    kelvin_sdk: KelvinSDKConfiguration = KelvinSDKConfiguration.default_constructor()

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.ksdk_config_dir_path = KPath(self.ksdk_config_dir_path).expanduser().resolve().create_dir()
        if self.ksdk_config_file_path.exists():
            self.kelvin_sdk = KelvinSDKConfiguration.from_file(self.ksdk_config_file_path)

    @staticmethod
    def default_ksdk_configuration_dir_path() -> KPath:
        """
        Yield the configuration directory where all configurations will be hosted.
        Usually hosted under `~/.config/kelvin/`

        Returns
        -------
        The ksdk configuration directory.
        """
        return KPath(GeneralConfigs.default_ksdk_configuration_dir).expanduser().resolve()

    @property
    def ksdk_temp_dir_path(self) -> KPath:
        """
        Return the path to the KSDK's temporary directory.
        Usually hosted under `~/.config/kelvin/temp/`

        Returns
        -------
        The KPath object to the temporary directory.
        """
        ksdk_temp_dir: str = GeneralConfigs.default_ksdk_temp_dir
        return KPath(self.ksdk_config_dir_path / ksdk_temp_dir).expanduser().resolve()

    @property
    def ksdk_schema_dir_path(self) -> KPath:
        """
        Return the path to the app schema hosting directory.
        Usually hosted under `~/.config/kelvin/schemas/`

        Returns
        -------
        The KPath object to the app schema directory.
        """
        ksdk_schema_storage_dir: str = GeneralConfigs.default_ksdk_schema_storage_dir
        return KPath(self.ksdk_config_dir_path / ksdk_schema_storage_dir).expanduser().resolve()

    @property
    def ksdk_datatype_dir_path(self) -> KPath:
        """
        Return the path to the raw datatype hosting directory.
        Usually hosted under `~/.config/kelvin/datatypes/`

        Returns
        -------
        The KPath object to the app schema directory.
        """
        ksdk_datatype_storage_dir: str = GeneralConfigs.default_ksdk_datatype_storage_dir
        return KPath(self.ksdk_config_dir_path / ksdk_datatype_storage_dir).expanduser().resolve()

    @property
    def ksdk_config_file_path(self) -> KPath:
        """
        Return the complete path to the ksdk config file.
        Usually hosted under `~/.config/kelvin/ksdk.yaml`

        Returns
        -------
        The KPath object to the ksdk configuration file.
        """
        ksdk_file: str = GeneralConfigs.default_ksdk_configuration_file
        return KPath(self.ksdk_config_dir_path / ksdk_file).expanduser().resolve()

    @property
    def ksdk_client_config_file_path(self) -> KPath:
        """
        Return the complete path to the ksdk client config file.
        Usually hosted under `~/.config/kelvin/client.yaml`

        Returns
        -------
        The KPath object to the ksdk client configuration file.
        """
        kelvin_client_file: str = GeneralConfigs.default_kelvin_sdk_client_configuration_file
        return KPath(self.ksdk_config_dir_path / kelvin_client_file).expanduser().resolve()

    @property
    def ksdk_history_file_path(self) -> KPath:
        """
        Return the complete path to the ksdk history log file.
        Usually hosted under `~/.config/kelvin/ksdk_history.log`

        Returns
        -------
        The KPath object to the ksdk history log file.
        """
        history_file: str = GeneralConfigs.default_ksdk_history_file
        return KPath(self.ksdk_config_dir_path / history_file).expanduser().resolve()

    def commit_ksdk_configuration(self) -> KelvinSDKGlobalConfiguration:
        self.kelvin_sdk.to_file(path=self.ksdk_config_file_path)
        return self

    def reset_ksdk_configuration(self) -> Any:
        self.kelvin_sdk.reset()
        return self

    def set_configuration(self, configuration: str, value: Any) -> bool:
        if configuration:
            configuration = configuration.lower()
            if not self.kelvin_sdk.configurations:
                self.kelvin_sdk.configurations = KelvinSDKEnvironmentVariables()
            if self.kelvin_sdk.configurations and configuration in self.kelvin_sdk.configurations.dict().keys():
                setattr(self.kelvin_sdk.configurations, configuration, value)
                self.commit_ksdk_configuration()
                return True
            raise ValueError("The configuration you provided is invalid")
        else:
            raise ValueError(f'Provided configuration "{configuration}" does not exist')

    def unset_configuration(self, configuration: str) -> bool:
        if configuration:
            configuration = configuration.lower()
            if not self.kelvin_sdk.configurations:
                self.kelvin_sdk.configurations = KelvinSDKEnvironmentVariables()
            if self.kelvin_sdk.configurations and configuration in self.kelvin_sdk.configurations.dict().keys():
                self.kelvin_sdk.configurations.__setattr__(configuration, None)
                self.commit_ksdk_configuration()
                return True
            raise ValueError("The configuration you provided is invalid")
        else:
            raise ValueError(f'Provided configuration "{configuration}" does not exist')
