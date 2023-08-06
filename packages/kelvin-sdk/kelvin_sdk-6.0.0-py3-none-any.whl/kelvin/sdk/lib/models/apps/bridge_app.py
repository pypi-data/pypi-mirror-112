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

from pydantic import Field

from kelvin.sdk.lib.models.apps.common import Name
from kelvin.sdk.lib.models.apps.kelvin_app import KelvinAppType
from kelvin.sdk.lib.models.generic import KSDKModel
from kelvin.sdk.lib.models.types import BaseEnum


class Access(BaseEnum):
    RO = "RO"
    RW = "RW"


class MetricsMapEntry(KSDKModel):
    name: Name = Field(..., description="Name.", title="Name")
    asset_name: Optional[Name] = Field(None, description="Asset Name.", title="Asset Name")
    data_type: str = Field(..., description="Data model.", title="Data Model")
    access: Optional[Access] = Field("RO", description="Metric Access.", title="Access")
    configuration: Optional[Any] = Field(None, description="Configuration.", title="Configuration")


class BridgeAppType(KelvinAppType):
    metrics_map: Optional[List[MetricsMapEntry]] = Field(None, description="Metrics Map.", title="Metrics Map")
