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

from kelvin.sdk.lib.configs.internal.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.utils.click_utils import ClickExpandedPath, KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def model_service() -> bool:
    """
    Manage and view model services.

    """


@model_service.command(cls=KSDKCommand)
@click.argument("name", type=click.STRING, nargs=1)
@click.option(
    "--model-service-dir",
    "model_service_dir",
    type=click.Path(),
    required=False,
    default=".",
    help=KSDKHelpMessages.model_service_dir,
)
def create(name: str, model_service_dir: str) -> bool:
    """
    Create a model service.

    """
    from kelvin.sdk.interface import model_service_create

    return model_service_create(model_service_name=name, model_service_dir=model_service_dir).success


@model_service.command(cls=KSDKCommand)
@click.option(
    "--dir",
    "model_service_dir",
    type=click.Path(exists=True),
    required=False,
    default=".",
    help=KSDKHelpMessages.model_service_dir,
)
@click.option("--fresh", default=False, is_flag=True, show_default=True, help=KSDKHelpMessages.fresh)
def build(model_service_dir: str, fresh: bool) -> bool:
    """
    Build a local model service into a packaged image.

    """
    from kelvin.sdk.interface import model_service_build

    return model_service_build(model_service_dir=model_service_dir, fresh_build=fresh).success


@model_service.command(cls=KSDKCommand)
@click.argument("model_service_name_with_version", nargs=1, type=click.STRING, required=False)
@click.option(
    "--model-service-config",
    type=ClickExpandedPath(exists=True),
    required=False,
    help=KSDKHelpMessages.model_service_config,
)
def start(
    model_service_name_with_version: str,
    model_service_config: str,
) -> bool:
    """
    Start an model service locally.

    """
    from kelvin.sdk.interface import model_service_start

    return model_service_start(
        model_service_name_with_version=model_service_name_with_version,
        model_service_config=model_service_config,
    ).success


@model_service.command(cls=KSDKCommand)
@click.argument("model_service_name_with_version", type=click.STRING, nargs=1, required=False)
def stop(model_service_name_with_version: str) -> bool:
    """
    Stop a model service running locally.

    """
    from kelvin.sdk.interface import model_service_stop

    return model_service_stop(model_service_name_with_version=model_service_name_with_version).success
