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

from typeguard import typechecked

from kelvin.sdk.lib.models.operation import OperationResponse


@typechecked
def label_create(label_name: str, label_title: str) -> OperationResponse:
    """
    Create a label on the platform.

    Parameters
    ----------
    label_name: The name of the label to create.
    label_title: The title of the label to create.

    Returns
    -------
    an OperationResponse object encapsulating the result of the label creation process.

    """
    from kelvin.sdk.lib.api.label import label_create as _label_create

    return _label_create(label_name=label_name, label_title=label_title)


@typechecked
def label_list(query: Optional[str] = None, should_display: bool = False) -> OperationResponse:
    """
    List all the available labels on the Platform.

    Parameters
    -------
    query: The query to filter the labels by.
    should_display: specifies whether or not the display should output data.

    Returns
    -------
    an OperationResponse object encapsulating the yielded labels on the platform.

    """
    from kelvin.sdk.lib.api.label import label_list as _label_list

    return _label_list(query=query, should_display=should_display)


@typechecked
def label_delete(label_names: Sequence[str]) -> OperationResponse:
    """
    Delete labels on the platform.

    Parameters
    -------
    label_names: The names of the labels to delete.

    Returns
    -------
    an OperationResponse object encapsulating the result of the label deletion operation.

    """
    from kelvin.sdk.lib.api.label import label_delete as _label_delete

    return _label_delete(label_names=label_names)
