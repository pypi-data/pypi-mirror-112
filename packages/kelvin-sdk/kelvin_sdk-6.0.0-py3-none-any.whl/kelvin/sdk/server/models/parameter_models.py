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

from typing import List, Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
    url: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    totp: Optional[str] = None
    reset_credentials: bool = True


class AuthenticationTokenRequest(BaseModel):
    full: bool = False
    margin: float = 10.0


class LabelCreateRequest(BaseModel):
    label_name: str
    label_title: str


class SecretCreateRequest(BaseModel):
    secret_name: str
    value: str


class DatatypeCreateRequest(BaseModel):
    datatype_name: str
    output_dir: Optional[str]


class DataTypeUploadRequest(BaseModel):
    input_dir: Optional[str]
    datatypes: Optional[List[str]]


class AssetCreationObject(BaseModel):
    asset_name: str
    asset_type_name: str
    asset_title: str


class AssetTypeCreationObject(BaseModel):
    asset_type_name: str
    asset_type_title: str


class EmulationStartRequest(BaseModel):
    app_config_path: Optional[str] = None
    app_name_with_version: Optional[str] = None
    tail: Optional[int] = None
    stream: bool = False
