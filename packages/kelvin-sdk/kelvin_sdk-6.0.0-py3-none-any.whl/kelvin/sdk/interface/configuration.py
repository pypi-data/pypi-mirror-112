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


@typechecked
def global_configurations_list(should_display: bool = False) -> OperationResponse:
    """
    List all available configurations for the Kelvin-SDK

    Parameters
    ----------
    should_display: specifies whether or not the display should output data.

    Returns
    ----------
    an OperationResponse object encapsulating the yielded Kelvin tool configurations.

    """
    from kelvin.sdk.lib.session.session_manager import session_manager

    return session_manager.global_configurations_list(should_display=should_display)


@typechecked
def global_configurations_set(configuration: str, value: str) -> OperationResponse:
    """
    Set the specified configuration on the platform system.

    Parameters
    ----------
    configuration: the configuration to change.
    value: the value that corresponds to the provided config.

    Returns
    ----------
    an OperationResponse object encapsulating the result the configuration set operation.

    """
    from kelvin.sdk.lib.session.session_manager import session_manager

    return session_manager.global_configurations_set(configuration=configuration, value=value)


@typechecked
def global_configurations_unset(configuration: str) -> OperationResponse:
    """
    Unset the specified configuration from the platform system

    Parameters
    ----------
    configuration: the configuration to unset.

    Returns
    ----------
    an OperationResponse object encapsulating the result the configuration unset operation.

    """
    from kelvin.sdk.lib.session.session_manager import session_manager

    return session_manager.global_configurations_unset(configuration=configuration)


@typechecked
def configurations_autocomplete(shell_type: str) -> bool:
    """
    Generate completion commands for shell.

    """
    from click._bashcomplete import get_completion_script

    print(get_completion_script("ksdk", "_KSDK_COMPLETE", shell_type))  # noqa

    return True
