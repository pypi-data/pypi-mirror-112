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
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Union

import click
from click import Context
from click import Group as _Group
from click import Option, Parameter, UsageError, echo
from click_shell import Shell

from kelvin.sdk.lib.configs.internal.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.models.generic import KPath
from kelvin.sdk.lib.models.types import LogColor, LogType, VersionStatus

if TYPE_CHECKING:
    from kelvin.sdk.lib.models.ksdk_global_configuration import KelvinSDKGlobalConfiguration


def _prompt(ctx: Context) -> str:
    """
    A custom prompt to get the invoked command chain and returns the pretty reversed version of it.

    :return: the 'pretty reversed' list of invoked commands.
    """
    command = Path(sys.argv[0]).stem
    result: List[str] = [""]
    root = ctx
    while root.parent:
        result += [root.command.name]
        root = root.parent
    result += [command]
    return " > ".join(reversed(result))


class ClickConfigs:
    all_verbose_commands = ["--verbose", "-v"]


class KSDKGroup(Shell):
    command_tree: dict = {}

    def group(self, *args: Any, **kwargs: Any) -> Callable[[Callable[..., Any]], _Group]:
        """
        A shortcut decorator for declaring and attaching a group to
        the group.  This takes the same arguments as :func:`group` but
        immediately registers the created command with this instance by
        calling into :meth:`add_command`.
        """
        kwargs.setdefault("cls", type(self))
        kwargs.setdefault("prompt", self.shell.prompt)
        kwargs.setdefault("intro", self.shell.intro)
        kwargs.setdefault("hist_file", self.shell.hist_file)
        kwargs.setdefault("on_finished", self.shell.on_finished)
        return super().group(*args, **kwargs)

    def add_command(self, cmd: Any, name: Any = None) -> None:
        if self.name not in self.command_tree:
            self.command_tree[self.name] = {}
        clean_description = str(cmd.help).split("\n")[0]
        self.command_tree.setdefault(self.name, {}).update({cmd.name: clean_description})
        super().add_command(cmd, name)

    def get_command_tree(self) -> dict:
        commands = self.command_tree.copy()
        commands_to_display = commands.pop("ksdk")
        for key, value in commands_to_display.items():
            if key in commands:
                commands_to_display[key] = commands.pop(key)
        KSDKGroup._look_down_the_tree(tree=commands_to_display, sub_tree=commands)
        return commands_to_display

    def invoke(self, ctx: Context) -> Any:
        from kelvin.sdk.lib.session.session_manager import session_manager

        ksdk_configuration = session_manager.get_global_ksdk_configuration()

        if (
            not ksdk_configuration.kelvin_sdk.configurations.ksdk_shell
            and not ctx.protected_args
            and not ctx.invoked_subcommand
        ):
            echo(ctx.get_help(), color=ctx.color)
            ctx.exit()

        return super().invoke(ctx)

    @staticmethod
    def _look_down_the_tree(tree: dict, sub_tree: dict) -> dict:
        copy_sub_tree = sub_tree.copy()
        for key in copy_sub_tree.keys():
            if isinstance(tree, dict) and key in tree.keys():
                value_to_set = sub_tree.pop(key)
                tree[key] = value_to_set
            else:
                for value in [value for value in tree.values() if isinstance(value, dict)]:
                    KSDKGroup._look_down_the_tree(value, sub_tree)
        return tree


class KSDKCommand(click.Command):
    version_status: Optional[VersionStatus]
    ksdk_configuration: Optional["KelvinSDKGlobalConfiguration"]

    @staticmethod
    def get_verbose_option(_: Context) -> Option:
        def show_verbose(context: Context, _: Union[Option, Parameter], value: Optional[str]) -> None:
            if value and not context.resilient_parsing:
                echo(context.get_help(), color=context.color)
                context.exit()

        return Option(
            ClickConfigs.all_verbose_commands,
            default=False,
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=show_verbose,
            help=KSDKHelpMessages.verbose,
        )

    @staticmethod
    def _setup_logger(verbose: bool, ksdk_configuration: "KelvinSDKGlobalConfiguration") -> Any:

        from .logger_utils import setup_logger

        # 1 - Check if the verbose flag was passed OR if it is set in the configuration menu
        verbose = verbose or ksdk_configuration.kelvin_sdk.configurations.ksdk_verbose_mode
        log_type = ksdk_configuration.kelvin_sdk.configurations.ksdk_output_type
        debug = ksdk_configuration.kelvin_sdk.configurations.ksdk_debug
        ksdk_colored_logs = sys.__stdout__.isatty() and ksdk_configuration.kelvin_sdk.configurations.ksdk_colored_logs
        log_color = LogColor.COLORED if ksdk_colored_logs else LogColor.COLORLESS

        # 2 - Finally, setup the logger and yield
        from kelvin.sdk.lib.session.session_manager import session_manager

        ksdk_history_file_path: KPath = session_manager.get_global_ksdk_configuration().ksdk_history_file_path

        return setup_logger(
            log_type=LogType(log_type),
            log_color=log_color,
            verbose=verbose,
            debug=debug,
            history_file=ksdk_history_file_path,
        )

    def get_params(self, ctx: Context) -> List:
        # Retrieve the params and ensure both '--help' and '--verbose'
        rv = self.params
        help_option = self.get_help_option(ctx)
        verbose_option = self.get_verbose_option(ctx)
        if verbose_option is not None:
            rv = rv + [verbose_option]
        if help_option is not None:
            rv = rv + [help_option]
        return rv

    def parse_args(self, ctx: Any, args: Any) -> list:
        # 1 - Retrieve the global kelvin-sdk configuration

        from kelvin.sdk.lib.session.session_manager import session_manager

        self.ksdk_configuration = session_manager.get_global_ksdk_configuration()

        # 2 - setup the logger
        verbose_flag_specified = any([item for item in ClickConfigs.all_verbose_commands if item in args])
        self._setup_logger(verbose=verbose_flag_specified, ksdk_configuration=self.ksdk_configuration)

        # 3 - Refresh the metadata, if that is the case, and assess the version status
        from kelvin.sdk.lib.utils.version_utils import assess_version_status

        refreshed_configuration = session_manager.refresh_metadata()
        if refreshed_configuration:
            self.ksdk_configuration = refreshed_configuration

        should_warn = self.ksdk_configuration.kelvin_sdk.configurations.ksdk_version_warning
        self.version_status = (
            assess_version_status(
                current_version=self.ksdk_configuration.kelvin_sdk.ksdk_current_version,
                minimum_version=self.ksdk_configuration.kelvin_sdk.ksdk_minimum_version,
                latest_version=self.ksdk_configuration.kelvin_sdk.ksdk_latest_version,
                should_warn=should_warn,
            )
            if should_warn
            else VersionStatus.UP_TO_DATE
        )

        # 4 - Dropping the verbose option from the args and proceeding
        args = [item for item in args if item not in ClickConfigs.all_verbose_commands]
        return super().parse_args(ctx, args)

    def invoke(self, ctx: Any) -> Any:
        from .logger_utils import logger

        result = None
        try:

            from kelvin.sdk.lib.session.session_manager import session_manager

            ksdk_configuration = self.ksdk_configuration or session_manager.get_global_ksdk_configuration()
            # 1 - setup imports
            from .version_utils import check_if_is_pre_release, color_formats

            # 2 - Display the correct messages for the current version status situation
            if not self.version_status == VersionStatus.UP_TO_DATE:
                from kelvin.sdk.lib.configs.internal.pypi_configs import PypiConfigs

                repository = ""
                if check_if_is_pre_release(version=ksdk_configuration.kelvin_sdk.ksdk_latest_version):
                    repository = f"--index-url {PypiConfigs.kelvin_pypi_internal_repository} "

                result = super().invoke(ctx)
                ksdk_version_warning: str = """\n
                        A {yellow}new version{reset} of the SDK is available! {red}{current_version}{reset} → {green}{latest_version}{reset} \n
                        {yellow}Changelog{reset}: https://docs.kelvininc.com \n
                        Run {green}pip3 install {repository}kics --upgrade{reset} to update\n
                        And log in again with {green}kelvin auth login <url>{reset}.
                """
                out_of_date_message = ksdk_version_warning.format_map(
                    {
                        **color_formats,
                        **ksdk_configuration.kelvin_sdk.versions,
                        "repository": repository,
                    }
                )
                logger.info(out_of_date_message)
            else:
                result = super().invoke(ctx)
        except UsageError:
            raise
        except click.exceptions.Exit:
            pass
        except Exception as e:
            logger.exception(f"Error executing kelvin command: {e}")
            sys.exit(1)

        if not result:
            sys.exit(1)

        return result


class ClickExpandedPath(click.Path):
    """
    A Click path argument that returns a ``Path``, not a string.
    """

    def convert(
        self, value: str, param: Optional[click.core.Parameter] = None, ctx: Optional[click.core.Context] = None
    ) -> Any:
        """
        Return a ``Path`` from the string ``click`` would have created with
        the given options.
        """
        import pathlib

        resolved_path = pathlib.Path(value).expanduser().resolve()
        content = super().convert(value=str(resolved_path), param=param, ctx=ctx)

        return content
