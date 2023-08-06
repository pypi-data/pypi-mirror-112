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

import click
from click import Choice

from kelvin.sdk.lib.configs.internal.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.models.types import ShellType
from kelvin.sdk.lib.utils.click_utils import KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def configuration() -> bool:
    """
    Local configurations that enhance the usage of this tool.

    """


@configuration.command(cls=KSDKCommand)
def list() -> bool:
    """
    List all the available configurations for this tool.
    """
    from kelvin.sdk.interface import global_configurations_list

    return global_configurations_list(should_display=True).success


@configuration.command(cls=KSDKCommand)
@click.argument("configuration", type=click.STRING, nargs=1, required=True)
@click.argument("value", type=click.STRING, nargs=1, required=True)
def set(configuration: str, value: str) -> bool:
    """
    Set a local configuration for this tool.

    e.g. kelvin configuration set KSDK_VERBOSE_MODE True

    Configurations can also be set with environment variables:

    e.g (Unix) export KSDK_VERBOSE_MODE=1
    """
    from kelvin.sdk.interface import global_configurations_set

    return global_configurations_set(configuration=configuration, value=value).success


@configuration.command(cls=KSDKCommand)
@click.argument("configuration", type=click.STRING, nargs=1, required=True)
def unset(configuration: str) -> bool:
    """
    Unset a local configuration for this tool.

    e.g. kelvin configuration unset KSDK_VERBOSE_MODE

    If the configuration is set as an environment variable, it can also be unset with:

    e.g (Unix) unset KSDK_VERBOSE_MODE
    """
    from kelvin.sdk.interface import global_configurations_unset

    return global_configurations_unset(configuration=configuration).success


@configuration.command(cls=KSDKCommand, help=KSDKHelpMessages.autocomplete_message)
@click.option("--shell", type=Choice(ShellType.as_list()), required=True, help=KSDKHelpMessages.shell)
def autocomplete(shell: str) -> bool:
    """
    Generate completion commands for shell.

    """

    from kelvin.sdk.interface import configurations_autocomplete

    return configurations_autocomplete(shell_type=shell)
