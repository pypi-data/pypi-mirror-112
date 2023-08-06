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

from functools import total_ordering
from typing import Optional

from packaging.version import Version as _Version
from pydantic import Field, PositiveFloat, conint, constr

from kelvin.sdk.lib.models.generic import KSDKModel


@total_ordering
class Version(KSDKModel):
    __root__: constr(regex="^([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?$")  # type: ignore # noqa

    def __lt__(self, other: Version) -> bool:
        """Less than comparison."""

        return _Version(str(self)) < _Version(str(other))


class NameDNS(KSDKModel):
    __root__: constr(regex="^[a-z]([-a-z0-9]*[a-z0-9])?$")  # type: ignore # noqa


class Identifier(KSDKModel):
    __root__: constr(regex="^[a-zA-Z]\w*$")  # type: ignore # noqa


class Port(KSDKModel):
    __root__: conint(le=65535, gt=0)  # type: ignore # noqa


class PythonEntryPoint(KSDKModel):
    __root__: constr(regex="^[a-zA-Z]\w*(\.[a-zA-Z]\w*)*:[a-zA-Z]\w*$")  # type: ignore # noqa


class PositiveNumber(KSDKModel):
    __root__: PositiveFloat  # type: ignore # noqa


class ZMQUrl(KSDKModel):
    __root__: constr(regex="^(tcp://[^:]+:[0-9]+|ipc://.+)$")  # type: ignore # noqa


class DottedIdentifier(KSDKModel):
    __root__: constr(regex="^([a-z][a-z0-9_]*\.)*[a-z][a-z0-9_]*$")  # type: ignore # noqa


class Name(KSDKModel):
    __root__: constr(regex="^[a-z]([-_.a-z0-9]*[a-z0-9])?$")  # type: ignore # noqa


class Uint16(KSDKModel):
    __root__: conint(ge=0, le=65365)  # type: ignore # noqa


class EnvironmentVar(KSDKModel):
    name: Identifier = Field(..., description="Environment variable name.", title="Environment Variable Name")
    value: Optional[str] = Field(None, description="Environment variable value.", title="Environment Variable Value")
