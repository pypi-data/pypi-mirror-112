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

from typeguard import typechecked

from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.models.types import StatusDataSource


@typechecked
def acp_list(source: StatusDataSource = StatusDataSource.CACHE, should_display: bool = False) -> OperationResponse:
    """
    Returns the list of ACPs available on the platform.

    Parameters
    ----------
    source: the status data source from where to obtain data.
    should_display: specifies whether or not the display should output data.

    Returns
    ----------
    an OperationResponse object encapsulating the ACPS available on the platform.

    """
    from kelvin.sdk.lib.api.acp import acp_list as _acp_list

    return _acp_list(query=None, source=source, should_display=should_display)


@typechecked
def acp_search(
    query: str, source: StatusDataSource = StatusDataSource.CACHE, should_display: bool = False
) -> OperationResponse:
    """
    Search for ACPs on the platform that match the provided query.

    Parameters
    ----------
    query: the query to search for.
    source: the status data source from where to obtain data.
    should_display: specifies whether or not the display should output data.

    Returns
    ----------
    an OperationResponse object encapsulating the matching ACPs available on the platform.

    """
    from kelvin.sdk.lib.api.acp import acp_list as _acp_list

    return _acp_list(query=query, source=source, should_display=should_display)


@typechecked
def acp_show(
    acp_name: str, source: StatusDataSource = StatusDataSource.CACHE, should_display: bool = False
) -> OperationResponse:
    """
    Displays all the details of the specified acp from the platform.

    Parameters
    ----------
    acp_name: the name of the acp.
    source: the status data source from where to obtain data.
    should_display: specifies whether or not the display should output data.

    Returns
    ----------
    an OperationResponse object encapsulating the yielded ACP instance and its detailed data.

    """
    from kelvin.sdk.lib.api.acp import acp_show as _acp_show

    return _acp_show(acp_name=acp_name, source=source, should_display=should_display)


@typechecked
def acp_delete(acp_name: str, ignore_destructive_warning: bool = False) -> OperationResponse:
    """
    Delete acp from the platform.

    Parameters
    ----------
    acp_name: the name of the acp.
    ignore_destructive_warning: indicates whether it should ignore the destructive warning.

    Returns
    ----------
    an OperationResponse object encapsulating the result of the ACP deletion operation.

    """
    from kelvin.sdk.lib.api.acp import acp_delete as _acp_delete

    return _acp_delete(acp_name=acp_name, ignore_destructive_warning=ignore_destructive_warning)


@typechecked
def acp_provision_script() -> OperationResponse:
    """
    Get the provisioning script to setup an ACP.

    Returns
    ----------
    an OperationResponse object encapsulating the ACP provision script.

    """
    from kelvin.sdk.lib.api.orchestration_provision import acp_provision_script as _acp_provision_script

    return _acp_provision_script()
