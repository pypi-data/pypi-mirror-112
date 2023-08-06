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
from dataclasses import dataclass
from typing import Mapping


class EmulationConfigs:
    emulation_system_acp: str = "emulation"
    emulation_data_app_version: str = "0.0.0"
    # Injector
    injector_app_name: str = "injector"
    injector_app_entry_point: str = "kelvin.sdk.injector:InjectorApp"
    injector_app_config_data_type: str = "kelvin.sdk.injector.config"
    injector_app_routing: Mapping = {"inputs": "outputs"}
    injector_param_filenames: str = "filenames"
    injector_param_repeat: str = "repeat"
    injector_param_ignore_timestamps: str = "ignore_timestamps"
    # Extractor
    extractor_app_name: str = "extractor"
    extractor_app_entry_point: str = "kelvin.sdk.extractor:ExtractorApp"
    extractor_app_config_data_type: str = "kelvin.sdk.extractor.config"
    extractor_app_routing: Mapping = {"outputs": "inputs"}
    extractor_param_batch: str = "batch"
    extractor_param_output_path: str = "output_path"
    # model services
    model_service_docs_url: str = "http://{host}:{port}/docs"  # noqa


@dataclass
class StudioConfigs:
    host: str = "localhost"
    port: int = 8000
    default_port: int = 8000
    studio_schema_file_bind: str = "{schema_file_path}:/opt/kelvin/app/server/data/{schema_file_name}:Z"
    studio_input_file_bind: str = "{input_file_path}:/opt/kelvin/app/server/data/{input_file_name}:Z"

    def get_url(self) -> str:
        return f"http://{self.host}:{self.port}"  # noqa

    def is_port_open(self) -> bool:
        from kelvin.sdk.lib.utils.general_utils import is_port_open

        return is_port_open(host=self.host, port=self.port)
