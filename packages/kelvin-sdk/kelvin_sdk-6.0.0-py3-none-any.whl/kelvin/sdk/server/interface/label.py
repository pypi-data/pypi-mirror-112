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
from kelvin.sdk.server.models.parameter_models import LabelCreateRequest

router = APIRouter(
    prefix="/labels",
    tags=["labels"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def label_create(label_create_request: LabelCreateRequest) -> OperationResponse:
    """
    Create a label on the platform.
    """

    from kelvin.sdk.interface import label_create as _label_create

    return _label_create(label_name=label_create_request.label_name, label_title=label_create_request.label_title)


@router.get("/")
def label_list(query: Optional[str] = None) -> OperationResponse:
    """
    List all the available labels on the Platform.
    """
    from kelvin.sdk.interface import label_list as _label_list

    return _label_list(query=query, should_display=False)


@router.delete("/")
def label_delete(label_names: Sequence[str]) -> OperationResponse:
    """
    Delete labels on the platform.
    """
    from kelvin.sdk.interface import label_delete as _label_delete

    return _label_delete(label_names=label_names)
