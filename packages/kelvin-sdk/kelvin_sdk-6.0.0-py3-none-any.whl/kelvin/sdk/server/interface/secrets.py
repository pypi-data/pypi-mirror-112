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

from typing import Optional, Sequence

from fastapi import APIRouter

from kelvin.sdk.lib.models.operation import OperationResponse

from ..models.parameter_models import SecretCreateRequest

router = APIRouter(
    prefix="/secrets",
    tags=["secrets"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def secrets_create(secret_create_request: SecretCreateRequest) -> OperationResponse:
    """
    Create a secret on the platform.
    """
    from kelvin.sdk.interface import secrets_create as _secrets_create

    return _secrets_create(secret_name=secret_create_request.secret_name, value=secret_create_request.value)


@router.get("/")
def secrets_list(query: Optional[str] = None) -> OperationResponse:
    """
    List all the available secrets on the Platform.
    """
    from kelvin.sdk.interface import secrets_list as _secrets_list

    return _secrets_list(query=query, should_display=False)


@router.delete("/")
def secrets_delete(secret_names: Sequence[str]) -> OperationResponse:
    """
    Delete secrets on the platform.
    """
    from kelvin.sdk.interface import secrets_delete as _secrets_delete

    return _secrets_delete(secret_names=secret_names)
