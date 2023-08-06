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

from pydantic import Field, conint
from pydantic.types import constr

from kelvin.sdk.lib.legacy.models.common import (
    DottedIdentifier,
    EnvironmentVar,
    Name,
    OPCUAEndpoint,
    Port,
    PositiveNumber,
    PythonEntryPoint,
    Version,
    ZMQUrl,
)
from kelvin.sdk.lib.legacy.models.docker import DockerAppType
from kelvin.sdk.lib.legacy.models.flow_app import FlowAppType
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
            entrypoint = f"{standard_app_name}.{standard_app_name}:App"
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
    entry_point: PythonEntryPoint
    requirements: Optional[str] = Field("requirements.txt", description="Package requirements", title="Requirements")
    version: Optional[Literal["3.7", "3.8"]] = Field(None, description="Python version.", title="Python Version")


class ApplicationInterface(BaseEnum):
    client = "client"  # Default
    data = "data"

    @property
    def default_template(self) -> dict:
        value = {
            "period": 1.0,
        }
        if self == ApplicationInterface.data:
            value["timeout"] = 10.0

        return {self.value_as_str: value}


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
        title="Subscription URL",
        description="The URL for clients to connect to when subscribing to the core server",
    )
    pub_url: Optional[ZMQUrl] = Field(
        None,
        title="Publish URL",
        description="The URL for clients to connect to when publishing to the core server",
    )
    topic: Optional[str] = Field(
        "",
        title="Topic",
        description="Message topic to allow multiple clients to share the same pub/sub sockets.",
    )
    compress: bool = Field(False, title="Compress Data", description="If true, data is compressed")
    period: Optional[PositiveNumber] = Field(1.0, title="Polling Period", description="Polling period.")

    environment_vars: Optional[List[EnvironmentVar]] = Field(
        None,
        description="Environment variables. Non-strings will be json-encoded as strings.",
        title="Environment Variables",
    )
    executable: Optional[str] = Field(None, title="Executable Name", description="Executable name.")
    args: Optional[List[str]] = Field([], title="Executable Arguments", description="Executable arguments.")
    spawn: bool = Field(
        False,
        title="Spawn Executable",
        description="If true, core automatically spawns the executable at startup.",
    )
    dso: Optional[str] = Field(
        None,
        title="Dynamic Shared Object for Core RPC App",
        description="Dynamic shared-object for Core RPC app.",
    )


class DataInterfaceType(KSDKModel):
    period: PositiveNumber = Field(..., description="Polling period.", title="Polling Period")
    timeout: Optional[PositiveNumber] = Field(10, description="Timeout period.", title="Timeout Period")


class PollerInterfaceType(KSDKModel):
    period: PositiveNumber = Field(..., description="Polling period.", title="Polling Period")


class DataModel(KSDKModel):
    name: DottedIdentifier = Field(..., description="Data model name.", title="Data Model Name")
    version: Version = Field(..., description="Data model version.", title="Data Model Version")
    path: Optional[str] = Field(None, description="Data model path.", title="Data Model Path")


class Interface(KSDKModel):
    type: ApplicationInterface = Field(..., description="Interface type.", title="Interface Type")
    client: Optional[ClientInterfaceType] = None
    data: Optional[DataInterfaceType] = None


class Item(KSDKModel):
    name: DottedIdentifier = Field(..., description="Item name.", title="Item name")
    value: Any = Field(..., description="Item value.", title="Item value")


class IOLegacy(KSDKModel):
    name: DottedIdentifier = Field(..., description="Input/Output name.", title="Input/Output name")
    data_model: DottedIdentifier = Field(None, description="Data model name.", title="Data Model Name")
    values: List[Item] = []


class RegistryMapIO(KSDKModel):
    historize: bool = False
    upload: bool = False
    name: DottedIdentifier
    node: str
    external_tag: Optional[str] = None
    access: Literal["RO", "RW"] = "RW"


class RegistryMap(KSDKModel):
    inputs: List[RegistryMapIO] = []
    outputs: List[RegistryMapIO] = []
    parameters: List[RegistryMapIO] = []


class ConnectionType(BaseEnum):
    opcua = "opcua"


class OPCUAConnectionType(KSDKModel):
    registry_map: RegistryMap
    endpoint: OPCUAEndpoint


class Connection(KSDKModel):
    name: Name = Field(..., description="Connection name.", title="Connection name")
    type: ConnectionType = Field(ConnectionType.opcua, description="Connection type.", title="Connection type")
    opcua: OPCUAConnectionType


# required by migration command
class RunTime(KSDKModel):
    historize_inputs: bool = False
    historize_outputs: bool = True
    type: str = "opcua"


class Core(KSDKModel):
    version: Version = Field(..., description="Core version.", title="Core Version")
    language: Language
    interface: Interface
    # required by injector & extractor
    data_models: List[DataModel] = []
    runtime: RunTime = Field(
        description="Runtime configuration.", title="Runtime configuration", default_factory=RunTime
    )
    connections: List[Connection] = []
    inputs: List[IOLegacy] = []
    outputs: List[IOLegacy] = []
    configuration: List[IOLegacy] = []
    parameters: List[IOLegacy] = []


class KelvinAppType(KSDKModel):
    core: Core
    images: Optional[Images] = None
    system_packages: Optional[List[str]] = Field(None, description="System packages.", title="System packages")


class Info(KSDKModel):
    name: Name = Field(..., description="Application name.", title="Application name")
    version: Version = Field(..., description="Application version.", title="Application Version")
    title: str = Field(..., description="Application title.", title="Application title")
    description: str = Field(..., description="Application description.", title="Application description")

    @property
    def app_name_with_version(self) -> str:
        return f"{str(self.name)}:{str(self.version)}"


class SystemResources(KSDKModel):
    memory: Optional[constr(regex="^[0-9]+(\.[0-9]+)?(K|M|G|Ki|Mi|Gi)$")] = Field(  # type: ignore # noqa
        "256Mi", description="Memory requirements.", title="Memory Requirements"
    )
    cpu: Optional[constr(regex="^[0-9]+(\.[0-9]+)?(m|)$")] = Field(  # type: ignore # noqa
        "0.4",
        description="CPU requirements defined as units. One CPU is equivalent of 1 vCPU/Core.",
        title="CPU Requirements",
    )


class PortMappingType(BaseEnum):
    host = "host"
    service = "service"


class PortMappingService(KSDKModel):
    container_port: Optional[Port] = Field(None, description="Container Port", title="Container Port")
    port: Port = Field(..., description="Port", title="Port")
    exposed: Optional[bool] = Field(False, description="Exposed", title="Exposed")
    exposed_port: Optional[conint(le=32767, gt=30000)] = Field(None, description="Exposed port.", title="Exposed Port")  # type: ignore # noqa


class PortMappingHostPort(KSDKModel):
    port: Port = Field(..., description="Port", title="Port")


class PortMapping(KSDKModel):
    name: Name = Field(..., description="Port name.", title="Port Name")
    type: PortMappingType = Field(..., description="Port Type.", title="Port Type")
    host: Optional[PortMappingHostPort] = Field(None, description="Host Port.", title="Host Port")
    service: Optional[PortMappingService] = Field(None, description="Service Port.", title="Service Port")


class Encoding(BaseEnum):
    utf_8 = "utf-8"
    ascii = "ascii"
    latin_1 = "latin_1"


class VolumeType(BaseEnum):
    text = "text"
    host = "host"
    persistent = "persistent"


class VolumeText(KSDKModel):
    data: str
    base64: Optional[bool] = False
    encoding: Optional[Encoding] = Field(Encoding.utf_8, description="File encoding.", title="File Encoding")


class VolumeHost(KSDKModel):
    source: str


class Volume(KSDKModel):
    name: Optional[Name] = Field(None, description="Volume name.", title="Volume Name")
    target: str = Field(..., description="Volume target directory.", title="Volume Target")
    type: VolumeType = Field(..., description="Volume type.", title="Volume Type")
    text: Optional[VolumeText] = Field(None, description="Text volume.", title="Text Volume")
    host: Optional[VolumeHost] = Field(None, description="Host directory or file.", title="Host Volume")
    persistent: Optional[Any] = Field(None, description="Persistent volume.", title="Persistent Volume")


class System(KSDKModel):
    resources: Optional[SystemResources] = Field(
        None,
        description="The runtime prevents the container from using more than the configured resource limits.",
        title="Resource Requirements",
    )
    privileged: Optional[bool] = Field(
        False,
        description="Give extended privileges to this application. Allows the application to access any devices on "
        "the host (ex: Serial).",
        title="Privileged Flag",
    )
    environment_vars: Optional[List[EnvironmentVar]] = Field(
        None,
        description="Environment variables. Non-strings will be json-encoded as strings.",
        title="Environment Variables",
    )
    ports: Optional[List[PortMapping]] = Field(None, description="Network port mappings.", title="Port Mappings")
    volumes: Optional[List[Volume]] = Field(None, description="Volume definitions.", title="Volumes")


class AppType(BaseEnum):
    kelvin = "kelvin"
    docker = "docker"


class App(KSDKModel):
    type: AppType = Field(..., description="Application type.", title="Application Type")
    docker: Optional[DockerAppType] = None
    kelvin: Optional[KelvinAppType] = None
    flow: Optional[FlowAppType] = None


class KelvinAppConfiguration(KSDKModel):
    spec_version: Version = Field(..., description="Specification version.", title="Specification Version")
    info: Info
    system: Optional[System] = None
    app: App
