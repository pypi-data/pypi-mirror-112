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
from typing import Optional

from fastapi import APIRouter

from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.models.types import StatusDataSource

router = APIRouter(
    prefix="/acps",
    tags=["acps"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def acp_list(query: Optional[str] = None, source: StatusDataSource = StatusDataSource.CACHE) -> OperationResponse:
    """
    Returns the list of ACPS available on the platform.
    """
    if query:
        from kelvin.sdk.interface import acp_search as _acp_search

        return _acp_search(query=query, source=source, should_display=False)
    else:
        from kelvin.sdk.interface import acp_list as _acp_list

        return _acp_list(source=source, should_display=False)


@router.get("/provision_script")
def acp_provision_script() -> OperationResponse:
    """
    Get the provisioning script to setup an ACP.
    """
    from kelvin.sdk.interface import acp_provision_script as _acp_provision_script

    return _acp_provision_script()


@router.get("/{acp_name}")
def acp_show(acp_name: str, source: StatusDataSource = StatusDataSource.CACHE) -> OperationResponse:
    """
    Displays all the details of the specified acp from the platform.
    """
    from kelvin.sdk.interface import acp_show as _acp_show

    return _acp_show(acp_name=acp_name, source=source, should_display=False)
