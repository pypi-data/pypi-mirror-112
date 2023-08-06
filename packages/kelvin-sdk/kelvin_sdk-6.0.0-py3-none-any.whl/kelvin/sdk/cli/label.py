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

import click

from kelvin.sdk.lib.configs.internal.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.utils.click_utils import KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def label() -> bool:
    """
    Manage labels on the platform.
    """


@label.command(cls=KSDKCommand)
@click.argument("name", nargs=1, type=click.STRING)
@click.argument("title", nargs=1, type=click.STRING)
def create(name: str, title: str) -> bool:
    """
    Create a label on the platform.

    """
    from kelvin.sdk.interface import label_create

    return label_create(label_name=name, label_title=title).success


@label.command(cls=KSDKCommand)
@click.option("query", "--filter", type=click.STRING, required=False, help=KSDKHelpMessages.label_list_filter)
def list(query: Optional[str]) -> bool:
    """
    List all the available labels on the platform.

    """
    from kelvin.sdk.interface import label_list

    return label_list(query=query, should_display=True).success


@label.command(cls=KSDKCommand)
@click.argument("label_names", nargs=-1, required=True, type=click.STRING)
def delete(label_names: Sequence[str]) -> bool:
    """
    Delete labels on the platform.

    """
    from kelvin.sdk.interface import label_delete

    return label_delete(label_names=label_names).success
