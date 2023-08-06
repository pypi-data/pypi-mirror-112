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

from typing import Any, List, Optional

from pydantic import Extra, Field

from kelvin.sdk.lib.models.apps.common import (
    DottedIdentifier,
    EnvironmentVar,
    Name,
    NameDNS,
    PositiveNumber,
    PythonEntryPoint,
    Uint16,
    Version,
    ZMQUrl,
)
from kelvin.sdk.lib.models.generic import KSDKModel
from kelvin.sdk.lib.models.types import BaseEnum
from kelvin.sdk.lib.utils.general_utils import standardize_string

try:
    from typing import Literal  # type: ignore
except ImportError:
    from typing_extensions import Literal  # type: ignore


class Images(KSDKModel):
    base: Optional[str] = Field(None, description="Base image.", title="Base Image")
    builder: Optional[str] = Field(None, description="Builder image.", title="Builder Image")


class ApplicationLanguage(BaseEnum):
    python = "python"  # default
    cpp = "cpp"

    def get_extension(self) -> str:
        return {ApplicationLanguage.python: ".py", ApplicationLanguage.cpp: ".cpp"}[self]

    def default_template(
        self,
        app_name: str,
        requirements: Optional[str] = None,
        makefile: Optional[str] = None,
        dso: Optional[str] = None,
    ) -> dict:
        from kelvin.sdk.lib.configs.internal.general_configs import GeneralConfigs

        standard_app_name = standardize_string(app_name)
        if self == ApplicationLanguage.python:
            entrypoint = f"{standard_app_name}:App"
            requirements = requirements or GeneralConfigs.default_requirements_file
            return {self.value_as_str: {"entry_point": entrypoint, "requirements": requirements}}
        if self == ApplicationLanguage.cpp:
            makefile = makefile or GeneralConfigs.default_makefile
            dso = dso or f"{standard_app_name}/{standard_app_name}.so"
            return {self.value_as_str: {"makefile": makefile, "dso": dso}}
        return {}


class CPPLanguageType(KSDKModel):
    dso: str = Field(..., description="Dynamic shared-object.", title="Dynamic Shared Object")
    makefile: Optional[str] = Field("CMakeLists.txt", description="Makefile.", title="Makefile")


class PythonLanguageType(KSDKModel):
    class Config:
        extra = Extra.allow

    entry_point: PythonEntryPoint
    requirements: Optional[str] = Field("requirements.txt", description="Package requirements", title="Requirements")
    version: Optional[Literal["3.7", "3.8"]] = Field(None, description="Python version.", title="Python Version")


class Credentials(KSDKModel):
    username: str
    password: str


class Authentication(KSDKModel):
    type: str
    credentials: Credentials


class Mqtt(KSDKModel):
    ip: str = Field(..., description="MQTT Broker IP address.", title="IP")
    port: Uint16 = Field(..., description="MQTT Broker Port.", title="Port")
    authentication: Optional[Authentication] = Field(
        None, description="MQTT Broker Authentication Settings.", title="Authentication"
    )

    @staticmethod
    def default_mqtt_configuration(ip_address: str) -> dict:
        return Mqtt(
            ip=ip_address,
            port=1883,
            authentication=Authentication(
                type="credentials", credentials=Credentials(username="kelvin", password="kelvin")  # nosec
            ),
        ).dict()  # nosec


class ApplicationInterface(BaseEnum):
    client = "client"  # Default
    data = "data"


class Language(KSDKModel):
    type: ApplicationLanguage = Field(..., description="Language type.", title="Language Type")
    python: Optional[PythonLanguageType] = None
    cpp: Optional[CPPLanguageType] = None


class InterfaceDescriptorType(BaseEnum):
    serial = "serial"
    ethernet = "ethernet"
    file = "file"


class ClientInterfaceType(KSDKModel):
    sub_url: Optional[ZMQUrl] = Field(
        None,
        description="The URL for clients to connect to when subscribing to the core server",
        examples=["tcp://127.0.0.1:10411"],
        title="Subscription URL",
    )
    pub_url: Optional[ZMQUrl] = Field(
        None,
        description="The URL for clients to connect to when publishing to the core server",
        examples=["tcp://127.0.0.1:21813"],
        title="Publish URL",
    )
    topic: Optional[str] = Field(
        None, description="Message topic to allow multiple clients to share the same pub/sub sockets.", title="Topic"
    )
    compress: Optional[bool] = Field(None, description="If true, data is compressed", title="Compress Data")
    period: Optional[PositiveNumber] = Field(1.0, description="Polling period.", title="Polling Period")
    executable: Optional[str] = Field(None, description="Executable name.", title="Executable Name")
    args: Optional[List[str]] = Field(None, description="Executable arguments.", title="Executable Arguments")
    environment_vars: Optional[List[EnvironmentVar]] = Field(
        None,
        description="Environment variables. Non-strings will be json-encoded as strings.",
        title="Environment Variables",
    )
    spawn: Optional[bool] = Field(
        None, description="If true, core automatically spawns the executable at startup.", title="Spawn Executable"
    )
    dso: Optional[str] = Field(
        None, description="Dynamic shared-object for Core RPC app.", title="Dynamic Shared Object for Core RPC App"
    )


class DataInterfaceType(KSDKModel):
    period: PositiveNumber = Field(..., description="Polling period.", title="Polling Period")
    timeout: Optional[PositiveNumber] = Field(10, description="Timeout period.", title="Timeout Period")


class PollerInterfaceType(KSDKModel):
    period: PositiveNumber = Field(..., description="Polling period.", title="Polling Period")


class DataType(KSDKModel):
    name: DottedIdentifier = Field(..., description="Data type name.", title="Data Type Name")
    version: Version = Field(..., description="Data type version.", title="Data Type Version")
    path: Optional[str] = Field(None, description="Data type path.", title="Data Type Path")

    @property
    def name_with_version(self) -> str:
        return f"{str(self.name)}:{str(self.version)}"


class Interface(KSDKModel):
    type: ApplicationInterface = Field(..., description="Interface type.", title="Interface Type")
    client: Optional[ClientInterfaceType] = None
    data: Optional[DataInterfaceType] = None


class Item(KSDKModel):
    name: DottedIdentifier = Field(..., description="Item name.", title="Item name")
    value: Any = Field(..., description="Item value.", title="Item value")


class IO(KSDKModel):
    name: DottedIdentifier = Field(..., description="Input/Output name.", title="Input/Output name")
    data_type: DottedIdentifier = Field(None, description="Data type name.", title="Data Type Name")
    values: List[Item] = []


class MetricInfo(KSDKModel):
    acp_names: Optional[List[NameDNS]] = Field(None, description="List of ACP names.", title="ACP Names")
    workload_names: Optional[List[NameDNS]] = Field(None, description="List of Workload names.", title="Workload Names")
    asset_names: Optional[List[Name]] = Field(None, description="List of asset names.", title="Asset Names")
    names: Optional[List[Name]] = Field(None, description="List of external metric names.", title="Names")


class Metric(KSDKModel):
    name: Name = Field(..., description="Name.", title="Name")
    data_type: str = Field(..., description="Data type.", title="Data Type")
    sources: Optional[List[MetricInfo]] = None
    targets: Optional[List[MetricInfo]] = None


class KelvinAppType(KSDKModel):
    images: Optional[Images] = Field(
        None, description="Image configuration for building a Kelvin application.", title="Kelvin Application Images"
    )
    system_packages: Optional[List[str]] = Field(
        None, description="Packages to install into image.", title="System Packages"
    )
    mqtt: Optional[Mqtt] = None
    language: Language
    interface: Optional[Interface] = None
    data_types: Optional[List[DataType]] = []
    inputs: Optional[List[Metric]] = Field(None, description="Inputs.", title="Inputs")
    outputs: Optional[List[Metric]] = Field(None, description="Outputs.", title="Outputs")
    configuration: Optional[Any] = Field(None, description="Configuration.", title="Configuration")
