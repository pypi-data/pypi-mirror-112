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

from typing import List, Optional, cast

from kelvin.sdk.client.error import APIError
from kelvin.sdk.client.model.responses import ACP, ACPMetrics, ACPStatus
from kelvin.sdk.lib.api.workload import retrieve_workload_and_workload_status_data
from kelvin.sdk.lib.configs.internal.general_configs import GeneralConfigs, GeneralMessages
from kelvin.sdk.lib.models.generic import GenericObject
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.models.types import StatusDataSource
from kelvin.sdk.lib.session.session_manager import session_manager
from kelvin.sdk.lib.utils.display_utils import (
    DisplayObject,
    display_data_entries,
    display_data_object,
    display_yes_or_no_question,
    error_colored_message,
    success_colored_message,
    warning_colored_message,
)
from kelvin.sdk.lib.utils.exception_utils import retrieve_error_message_from_api_exception
from kelvin.sdk.lib.utils.general_utils import get_bytes_as_human_readable, get_datetime_as_human_readable
from kelvin.sdk.lib.utils.logger_utils import logger


def acp_list(
    query: Optional[str] = None, source: StatusDataSource = StatusDataSource.CACHE, should_display: bool = False
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
    try:
        acp_list_step_1 = "Retrieving ACPs.."
        if query:
            acp_list_step_1 = f'Searching ACPs that match "{query}"'

        logger.info(acp_list_step_1)

        display_obj: DisplayObject = retrieve_acp_and_acp_status_data(
            query=query, source=source, should_display=should_display, should_colorize=should_display
        )

        return OperationResponse(success=True, data=display_obj.parsed_data)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving ACPs: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving ACPs: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


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
    try:
        logger.info(f'Retrieving ACP details for "{acp_name}"')

        client = session_manager.login_client_on_current_url()

        # 1 - Retrieve the ACP data
        acp_info: ACP = client.acp.get_acp(acp_name=acp_name)
        acp_info_display: DisplayObject = display_data_object(
            data=acp_info, object_title=GeneralConfigs.table_title.format(title="ACP Info"), should_display=False
        )

        # 2 - If enabled, retrieve the ACP metrics
        acp_metrics_display_output: str = ""
        acp_metrics_data_display: Optional[DisplayObject] = None
        if acp_info.metrics_enabled:
            logger.info(f'ACP metrics available. Retrieving metrics for "{acp_name}"')
            acp_metrics_data = client.acp_metrics.get_acp_metrics(acp_name=acp_name)
            acp_metrics_data_display = retrieve_acp_metrics_data(acp_metrics_data=acp_metrics_data, title="ACP Metrics")
            acp_metrics_display_output = acp_metrics_data_display.tabulated_data

        # 3 - Retrieve the workload data corresponding to the ACP
        workloads_display = retrieve_workload_and_workload_status_data(
            acp_name=acp_name, source=source, should_display=False
        )
        acp_info_display_output = acp_info_display.tabulated_data

        workloads_display_output = workloads_display.tabulated_data

        if should_display:
            logger.info(f"{acp_info_display_output}\n{acp_metrics_display_output}\n{workloads_display_output}")

        complete_acp_info = {}
        if acp_info_display:
            complete_acp_info["acp"] = acp_info_display.parsed_data
        if acp_metrics_data_display:
            complete_acp_info["acp_metrics"] = acp_metrics_data_display.parsed_data
        if workloads_display:
            complete_acp_info["acp_workloads"] = workloads_display.parsed_data

        return OperationResponse(success=True, data=complete_acp_info)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving ACP: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving ACP: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


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
    try:
        if not ignore_destructive_warning:
            acp_delete_confirmation: str = """
                This operation will remove the ACP from the platform.
                All ACP local data will be lost.
            """
            ignore_destructive_warning = display_yes_or_no_question(acp_delete_confirmation)

        success_message = ""
        if ignore_destructive_warning:
            logger.info(f'Deleting ACP "{acp_name}"')

            client = session_manager.login_client_on_current_url()

            client.acp.delete_acp(acp_name=acp_name)

            success_message = f'ACP "{acp_name}" successfully deleted'
            logger.relevant(success_message)

        return OperationResponse(success=True, log=success_message)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error deleting ACP: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error deleting ACP: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def retrieve_acp_metrics_data(acp_metrics_data: ACPMetrics, title: str = "") -> DisplayObject:
    """
    Unpack the data provided by the ACPMetrics object.

    Parameters
    ----------
    acp_metrics_data :  the ACPMetrics object.
    title : the title to associate to the the ACP metrics detail info.

    Returns
    -------
    a DisplayObject containing a simplified, pretty metrics object.

    """
    final_object: dict = {}

    allocation_data = acp_metrics_data.allocation
    cpu_utilization_data = acp_metrics_data.cpu_utilization
    disk_data = acp_metrics_data.disk
    memory_usage_data = acp_metrics_data.memory_usage
    network_data = acp_metrics_data.network

    if allocation_data:
        final_object["Allocation"] = {
            "CPU capacity": allocation_data.cpu_capacity,
            "CPU usage": allocation_data.cpu_requests,
            "Memory capacity": get_bytes_as_human_readable(input_bytes_data=allocation_data.memory_capacity),
            "Memory usage": get_bytes_as_human_readable(input_bytes_data=allocation_data.memory_requests),
        }

    if cpu_utilization_data:
        last_cpu_utilization_entry = cpu_utilization_data[-1] if cpu_utilization_data else None
        if last_cpu_utilization_entry:
            final_object["CPU utilization"] = {
                "Timestamp (date)": get_datetime_as_human_readable(input_date=last_cpu_utilization_entry.timestamp),
                "Value": last_cpu_utilization_entry.value,
            }

    if disk_data:
        final_object["Disk data"] = {
            "Total capacity": get_bytes_as_human_readable(input_bytes_data=disk_data.total_bytes),
            "Used capacity": get_bytes_as_human_readable(input_bytes_data=disk_data.used_bytes),
        }

    if memory_usage_data:
        last_memory_usage_entry = memory_usage_data[-1] if memory_usage_data else None
        if last_memory_usage_entry:
            final_object["Memory usage"] = {
                "Timestamp (date)": get_datetime_as_human_readable(input_date=last_memory_usage_entry.timestamp),
                "Value": get_bytes_as_human_readable(input_bytes_data=last_memory_usage_entry.value),
            }

    if network_data:
        final_object["Network data"] = {
            "Transmitted (Tx)": get_bytes_as_human_readable(input_bytes_data=network_data.total_tx),
            "Received (Rx)": get_bytes_as_human_readable(input_bytes_data=network_data.total_rx),
        }

    return display_data_object(data=final_object, object_title=title, should_display=False)


def retrieve_acp_and_acp_status_data(
    query: Optional[str] = None,
    source: StatusDataSource = StatusDataSource.CACHE,
    should_display: bool = True,
    should_colorize: bool = True,
) -> DisplayObject:
    """
    Centralize all calls to acps.
    First, retrieve all acps that match the provided criteria.
    Second, retrieve all acps status.
    Last, merge both results and yield the result.

    Parameters
    ----------
    query: the query to search specific acps.
    source: the acp status data source from where to obtain data.
    should_display: if specified, will display the results of this retrieve operation.
    should_colorize: if set to False, will return the contents in its raw format.

    Returns
    -------
    a DisplayObject containing the acps and respective status data.

    """
    client = session_manager.login_client_on_current_url()

    acps = cast(List, client.acp.list_acp(search=query))
    acps_status = []

    if acps:
        acp_names_search_query = ",".join([acp.name for acp in acps])
        result = client.acp.list_acp_status(search=acp_names_search_query, source=source.value)
        acps_status = cast(List, result)

    data_to_display: List[GenericObject] = _combine_acp_and_acp_status_data(
        acps=acps, acps_status=acps_status, should_colorize=should_colorize
    )

    return display_data_entries(
        data=data_to_display,
        header_names=["Name", "Title", "ACP Status", "Last seen"],
        attributes=["name", "title", "acp_status", "last_seen"],
        table_title=GeneralConfigs.table_title.format(title="ACPs"),
        should_display=should_display,
        no_data_message="No ACPs available",
    )


def _combine_acp_and_acp_status_data(
    acps: List[ACP], acps_status: List, should_colorize: bool = True
) -> List[GenericObject]:
    """
    When provided with a list of acps and a list of acp statuses, combined them into a list of compound objects.
    This list consists of a custom object that results from the merge of an acp and its status data.


    Parameters
    ----------
    acps: the list of acps to combine.
    acps_status: the list of acp status objects to combine.
    should_colorize: if set to False, will return the contents in its raw format.

    Returns
    -------
    a list of GenericObjects.

    """
    acps = acps or []
    acps_status = acps_status or []
    data_to_display: List[GenericObject] = []
    default_status = _get_parsed_acp_status()
    for acp in acps:
        custom_object: dict = {
            "name": acp.name,
            "title": acp.title,
            "acp_status": default_status,
            "last_seen": default_status,
        }
        for status_entry in acps_status:
            if acp.name == status_entry.name and status_entry.status:
                acp_status = _get_parsed_acp_status(
                    acp_status_item=status_entry.status, should_colorize=should_colorize
                )
                custom_object["acp_status"] = acp_status
                custom_object["last_seen"] = get_datetime_as_human_readable(input_date=status_entry.status.last_seen)
                break
        data_to_display.append(GenericObject(data=custom_object))

    return data_to_display


def _get_parsed_acp_status(acp_status_item: Optional[ACPStatus] = None, should_colorize: bool = True) -> str:
    """
    When provided with an ACPStatus, yield the message the message with the provided color schema and format.

    Parameters
    ----------
    acp_status_item: the ACPs status item containing all necessary information.
    should_colorize: if set to False, will return the contents in its raw format.

    Returns
    -------
    a formatted string with the correct color schema.

    """
    message = GeneralMessages.no_data_available
    state = GeneralMessages.no_data_available

    if acp_status_item:
        message = acp_status_item.message or message
        state = acp_status_item.state or state

    formatter = None
    if should_colorize:
        formatter_structure = {
            "connected": success_colored_message,
            "warning": warning_colored_message,
            "no_connection": error_colored_message,
        }
        formatter = formatter_structure.get(state)

    return formatter(message=message) if formatter else message
