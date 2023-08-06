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
def secrets_create(secret_name: str, value: str) -> OperationResponse:
    """
    Create a secret on the platform.

    Parameters
    ----------
    secret_name: The name of the secret to create.
    value: The value corresponding to the secret.

    Returns
    -------
    an OperationResponse object encapsulating the result of the secrets creation operation.

    """
    from kelvin.sdk.lib.api.secrets import secrets_create as _secrets_create

    return _secrets_create(secret_name=secret_name, value=value)


@typechecked
def secrets_list(query: Optional[str] = None, should_display: bool = False) -> OperationResponse:
    """
    List all the available secrets on the Platform.

    Parameters
    ----------
    query: The query to filter the secrets by.
    should_display: specifies whether or not the display should output data.

    Returns
    -------
    an OperationResponse object encapsulating the secrets available on the platform.

    """
    from kelvin.sdk.lib.api.secrets import secrets_list as _secrets_list

    return _secrets_list(query=query, should_display=should_display)


@typechecked
def secrets_delete(secret_names: Sequence[str], ignore_destructive_warning: bool = False) -> OperationResponse:
    """
    Delete secrets on the platform.

    Parameters
    ----------
    secret_names: The names of the secrets to delete.
    ignore_destructive_warning: indicates whether it should ignore the destructive warning.

    Returns
    -------
    an OperationResponse object encapsulating the result of the secrets deletion operation.

    """
    from kelvin.sdk.lib.api.secrets import secrets_delete as _secrets_delete

    return _secrets_delete(secret_names=secret_names, ignore_destructive_warning=ignore_destructive_warning)
