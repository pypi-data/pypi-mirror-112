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

from typing import List, Optional, Sequence, cast

from kelvin.sdk.client.error import APIError
from kelvin.sdk.client.model.requests import LabelCreate
from kelvin.sdk.lib.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.session.session_manager import session_manager
from kelvin.sdk.lib.utils.display_utils import display_data_entries, display_yes_or_no_question
from kelvin.sdk.lib.utils.exception_utils import retrieve_error_message_from_api_exception
from kelvin.sdk.lib.utils.logger_utils import logger


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
    try:
        logger.info(f'Creating label "{label_name}" on the platform')

        client = session_manager.login_client_on_current_url()

        label_create_request = LabelCreate(name=label_name, title=label_title)

        client.label.create_label(data=label_create_request)

        success_message = f'Label "{label_name}" successfully created on the platform'
        logger.relevant(success_message)

        return OperationResponse(success=True, log=success_message)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error creating label: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error creating label: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def label_list(query: Optional[str], should_display: bool = False) -> OperationResponse:
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
    try:
        logger.info("Retrieving platform data labels..")

        client = session_manager.login_client_on_current_url()

        yielded_labels = cast(List, client.label.list_label(search=query)) or []

        display_data = display_data_entries(
            data=yielded_labels,
            header_names=["Label name", "Label title", "Created", "Updated"],
            attributes=["name", "title", "created", "updated"],
            table_title=GeneralConfigs.table_title.format(title="Labels"),
            should_display=False,
            no_data_message="No labels available",
        )

        if should_display and display_data:
            logger.info(f"{display_data.tabulated_data}")

        return OperationResponse(success=True, data=display_data.parsed_data)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving labels: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving labels: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


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
    labels_description = ", ".join(label_names)
    logger.info(f'Deleting label(s) "{labels_description}" from the platform')

    prompt_question = f'This operation will delete the label(s) "{labels_description}" from the platform'
    confirm = display_yes_or_no_question(question=prompt_question)

    if confirm:
        client = session_manager.login_client_on_current_url()

        for label_name in label_names:
            try:
                client.label.delete_label(label_name=label_name)
                logger.relevant(f'Label "{label_name}" successfully deleted from the platform')

            except APIError as exc:
                api_error = retrieve_error_message_from_api_exception(api_error=exc)
                api_error_message = f"Error deleting label: {api_error}"
                logger.error(api_error_message)
                return OperationResponse(success=False, log=api_error_message)

            except Exception as exc:
                error_message = f"Error deleting label: {str(exc)}"
                logger.exception(error_message)
                return OperationResponse(success=False, log=error_message)

        return OperationResponse(success=True, log="Successfully deleted labels")

    return OperationResponse(success=True, log="Cancelling label deletion")
