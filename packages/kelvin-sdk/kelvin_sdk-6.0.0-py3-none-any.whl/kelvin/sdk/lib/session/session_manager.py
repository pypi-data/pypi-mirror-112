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
import json
import sys
import time
from getpass import getpass
from typing import Any, List, Optional, Sequence

from keycloak.exceptions import KeycloakError
from pydantic import ValidationError

from kelvin.sdk.client import Client
from kelvin.sdk.lib.configs.internal.auth_manager_configs import AuthManagerConfigs
from kelvin.sdk.lib.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.exceptions import KSDKException, MandatoryConfigurationsException
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.utils.display_utils import (
    display_data_entries,
    display_yes_or_no_question,
    pretty_colored_content,
    success_colored_message,
)
from kelvin.sdk.lib.utils.logger_utils import logger

from ..configs.internal.general_configs import KSDKHelpMessages
from ..models.generic import KPath
from ..models.ksdk_docker import KSDKDockerAuthentication
from ..models.ksdk_global_configuration import CompanyMetadata, KelvinSDKConfiguration, KelvinSDKGlobalConfiguration
from ..utils.exception_utils import retrieve_error_message_from_keycloak_exception
from ..utils.general_utils import get_system_information


class Singleton(type):
    _instances: dict = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SessionManager(metaclass=Singleton):
    # 1 - Central piece
    global_ksdk_configuration: Optional[KelvinSDKGlobalConfiguration] = None
    # 2 - Cached blocks
    docker_credentials: Optional[KSDKDockerAuthentication] = None
    current_site_metadata: Optional[CompanyMetadata] = None
    current_client: Optional[Client] = None

    # 1 - Global Session Manager
    def reset_session(self, full_reset: bool = False, ignore_destructive_warning: bool = False) -> OperationResponse:
        """Logs off the client all currently stored sessions.

        Parameters
        ----------
        full_reset: bool, default=False
            Indicates whether it should proceed with a full reset.
        ignore_destructive_warning: bool, default=False
            Ignore_destructive_warning: indicates whether it should ignore the destructive warning.
        Returns
        -------
        OperationResponse
            An OperationResponse object encapsulating the result of the logout request.
        """

        try:
            # 1 - Logout from all sessions
            if not ignore_destructive_warning:
                ignore_destructive_warning = display_yes_or_no_question("")

            if ignore_destructive_warning:
                if self.current_client:
                    self.current_client.logout()
                    self.current_client = None
                    self.current_site_metadata = None

                self.get_global_ksdk_configuration().reset_ksdk_configuration().commit_ksdk_configuration()

            ksdk_configuration = self.get_global_ksdk_configuration()

            # 2 - If it is a full reset, purge all the configuration files
            if full_reset:
                logger.info("Resetting KSDK configurations..")
                self._reset_configuration_files(ksdk_configuration=ksdk_configuration)

            success_message = "Session successfully reset."
            logger.relevant(success_message)
            return OperationResponse(success=True, log=success_message)
        except Exception as exc:
            error_message = f"Error resetting session: {str(exc)}"
            logger.exception(error_message)
            return OperationResponse(success=False, log=error_message)

    @staticmethod
    def _reset_configuration_files(ksdk_configuration: KelvinSDKGlobalConfiguration) -> None:
        """Clear all configuration files and folders

        Parameters
        ----------
        ksdk_configuration: KelvinSDKGlobalConfiguration
            A KSDK global configuration instance
        """
        # 1 - get the variables
        files_to_reset: List[KPath] = [
            ksdk_configuration.ksdk_history_file_path,
            ksdk_configuration.ksdk_client_config_file_path,
            ksdk_configuration.ksdk_config_file_path,
            ksdk_configuration.ksdk_temp_dir_path,
            ksdk_configuration.ksdk_schema_dir_path,
            ksdk_configuration.ksdk_datatype_dir_path,
        ]
        # 2 - delete all files
        for item in files_to_reset:
            if item.exists():
                if item.is_dir():
                    item.delete_dir()
                else:
                    item.unlink()

    # 2 - Client access and instantiation
    def login_on_url(
        self,
        url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        totp: Optional[str] = None,
        reset: bool = False,
    ) -> OperationResponse:
        """Logs the user into the provided url.

        Parameters
        ----------
        url: str, optional
            The url to log on.
        username: str, optional
            The username of the client site.
        password: str, optional
            The password corresponding to the username.
        totp: str, optional
            The current TOTP corresponding to the username.
        reset: bool, default=False
            If set to True, will clear the existing configuration prior to the new session.

        Returns
        -------
        OperationResponse
            An OperationResponse object encapsulating the result of the authentication request.

        """
        try:
            if reset:
                self.reset_session(full_reset=reset, ignore_destructive_warning=True)

            url = url or input("Platform: ")
            username_missing = username is None and password is not None
            password_missing = username is not None and password is None
            empty_credentials = username is None and password is None

            if username_missing or password_missing:
                ksdk_auth_incomplete_credentials: str = """Incomplete credentials. \n
                    Either provide both credentials or follow the prompt."""
                raise KSDKException(ksdk_auth_incomplete_credentials)

            if empty_credentials:
                username = input("Enter your username: ")
                password = getpass(prompt="Enter your password: ")
                totp_prompt: str = "Enter 2 Factor Authentication (2FA) one-time password (blank if not required): "
                totp = getpass(totp_prompt) or None

            if not username or not password:
                raise KSDKException(message="Please provide a valid set of credentials")

            # 1 - Ensure the ksdk configuration file exists before proceeding
            if not url:
                raise KSDKException(message="No session currently available. Please provide a valid url argument")

            # 2 - Save the client configuration to the client configuration
            self.current_client = self._fresh_client_login_for_url(
                url=url, username=username, password=password, totp=totp
            )
            success_message = f'Successfully logged on "{url}"'
            logger.relevant(success_message)
            return OperationResponse(success=True, log=success_message)
        except KeycloakError as exc:
            error_message = retrieve_error_message_from_keycloak_exception(keycloak_exception=exc)
            keycloak_auth_failure: str = f"""Error authenticating: {error_message}. \n
                Contact Kelvin's support team.
            """
            logger.exception(keycloak_auth_failure)
            return OperationResponse(success=False, log=keycloak_auth_failure)
        except Exception as exc:
            api_auth_failure: str = f"""Error authenticating: {str(exc)}. \n
                Consider invalidating authentication cache with `kelvin auth login --reset`.
            """
            logger.exception(api_auth_failure)
            return OperationResponse(success=False, log=api_auth_failure)

    def login_client_on_current_url(
        self, login: bool = True, verbose: bool = True, force_metadata: bool = False
    ) -> Client:
        """Performs a fresh login on the current url, retrieving the instantiated KelvinClient object.

        Parameters
        ----------
        login: bool, default=True
            Hints the Kelvin SDK Client object it should perform a login.
        verbose: bool, default=True
            Indicates whether the Kelvin SDK Client object should display all verbose logs.
        force_metadata: bool, default=True
            Indicates whether the Kelvin SDK Client object should force fetch metadata.

        Returns
        -------
        Client
            A ready-to-use KelvinClient object.

        """

        try:
            ksdk_configuration = self.get_global_ksdk_configuration()
            current_url = ksdk_configuration.kelvin_sdk.current_url
            current_user = ksdk_configuration.kelvin_sdk.current_user
            kwargs = {"metadata": None} if force_metadata else {}

            self.current_client = Client.from_file(
                ksdk_configuration.ksdk_client_config_file_path,
                site=current_url,
                url=current_url,
                username=current_user,
                login=login,
                verbose=verbose,
                timeout=AuthManagerConfigs.kelvin_client_timeout_thresholds,
                **kwargs,  # type: ignore
            )
            if not self.current_site_metadata:
                self._set_metadata_for_current_url()
            return self.current_client
        except Exception:
            raise ConnectionError(AuthManagerConfigs.invalid_session_message)

    def authentication_token(self, full: bool, margin: float = 10.0) -> OperationResponse:
        """Obtain an authentication authentication_token from the API.

        Parameters
        ----------
        full: bool
            Return the full authentication_token.
        margin: float, default=10.0
            Minimum time to expiry.
        Returns
        -------
        OperationResponse
            OperationResponse object encapsulating the authentication token.
        """

        margin = max(margin, 0.0)
        force = margin <= 0.0

        try:
            client = self.login_client_on_current_url(login=False, verbose=False)
            client.login(force=force, margin=margin)
        except Exception as exc:
            logger.error(str(exc))
            return OperationResponse(success=False, log=str(exc))

        if full:
            json.dump(client.token, sys.stdout, indent=2)
        else:
            sys.stdout.write(client.token["access_token"])

        return OperationResponse(success=True, log=str(client.token))

    def _fresh_client_login_for_url(
        self,
        url: str,
        username: str,
        password: str,
        totp: Optional[str],
    ) -> Client:
        """Setup a fresh login, writing the required configurations to target ksdk configuration file path.

        Sets up the kelvin API client configuration to allow api interaction.
        Sets up the kelvin sdk configuration to allow the storage of specific ksdk variables.

        Parameters
        ----------
        url: str
            The url to login to.
        username: str
            The username of the client site.
        password: str
            The password corresponding to the username.
        totp: str, optional
            The TOTP corresponding to the username.
        Returns
        -------
        Client
            A ready-to-use KelvinClient object.
        """

        ksdk_configuration: KelvinSDKGlobalConfiguration = self.get_global_ksdk_configuration()
        try:
            # Prepare metadata retrieval
            logger.info(f'Attempting to log on "{url}"')

            self.current_client = Client.from_file(
                ksdk_configuration.ksdk_client_config_file_path,
                site=url,
                username=username,
                create=True,
                verbose=True,
                timeout=AuthManagerConfigs.kelvin_client_timeout_thresholds,
            )
            self.current_client.login(password=password, totp=totp, force=True)

            # Retrieve the versions and set them once the client access is done
            url_metadata = self._set_metadata_for_current_url()

            ksdk_configuration.kelvin_sdk.last_metadata_refresh = time.time()
            ksdk_configuration.kelvin_sdk.current_url = url
            ksdk_configuration.kelvin_sdk.current_user = username
            ksdk_configuration.kelvin_sdk.ksdk_minimum_version = url_metadata.sdk.ksdk_minimum_version
            ksdk_configuration.kelvin_sdk.ksdk_latest_version = url_metadata.sdk.ksdk_latest_version
            ksdk_configuration.commit_ksdk_configuration()

            return self.current_client
        except Exception as inner_exception:
            try:
                ksdk_configuration.reset_ksdk_configuration().commit_ksdk_configuration()
            except Exception:
                raise inner_exception
            raise inner_exception

    def get_global_ksdk_configuration(self) -> KelvinSDKGlobalConfiguration:
        """Attempt to retrieve the KelvinSDKGlobalConfiguration from specified file path.

        Returns
        -------
        KelvinSDKGlobalConfiguration
            A KelvinSDKGlobalConfiguration object corresponding to the current configuration.
        """

        if self.global_ksdk_configuration:
            return self.global_ksdk_configuration

        try:
            self.global_ksdk_configuration = KelvinSDKGlobalConfiguration()
            return self.global_ksdk_configuration.commit_ksdk_configuration()
        except Exception:
            self.global_ksdk_configuration = KelvinSDKGlobalConfiguration(
                ksdk_config_dir_path=KelvinSDKGlobalConfiguration.default_ksdk_configuration_dir_path(),
                kelvin_sdk=KelvinSDKConfiguration.default_constructor(),
            )
            return self.global_ksdk_configuration.commit_ksdk_configuration()

    def get_documentation_link_for_current_url(self) -> Optional[str]:
        """Retrieve, if existent, the complete url to the documentation page.

        Returns
        -------
        str
            a string containing a link to the documentation page.
        """
        try:
            return self.get_current_session_metadata().documentation.url
        except Exception:
            return None

    def display_current_system_info(self) -> str:
        """Display system information as well as, if existent, the current session's url.

        Returns
        -------
        str
            a string containing the system's information.
        """

        try:
            system_information = get_system_information(pretty_keys=True)
            ksdk_configuration = self.get_global_ksdk_configuration()
            current_url = ksdk_configuration.kelvin_sdk.current_url or KSDKHelpMessages.current_session_login
            # display utils
            pretty_current_url = success_colored_message(message=current_url)
            pretty_system_info = pretty_colored_content(content=system_information, indent=2, initial_indent=2)
            return f"\nCurrent session: {pretty_current_url}\nSystem Information: {pretty_system_info}"
        except Exception:
            return KSDKHelpMessages.current_session_login

    def get_docker_credentials_for_current_url(self) -> KSDKDockerAuthentication:
        """Returns the current credentials for the specified url.

        Returns
        -------
        KSDKDockerAuthentication
            An KSDKDockerAuthentication instance containing the Kelvin API Client credentials for the specified url.
        """
        try:
            if self.docker_credentials:
                return self.docker_credentials

            ksdk_configuration = self.get_global_ksdk_configuration()
            current_client = self.login_client_on_current_url()
            current_site_metadata = self.get_current_session_metadata()

            self.docker_credentials = KSDKDockerAuthentication(
                **{
                    "registry_url": current_site_metadata.docker.url,
                    "registry_port": current_site_metadata.docker.port,
                    "username": ksdk_configuration.kelvin_sdk.current_user,
                    "password": current_client.password,
                }
            )
            return self.docker_credentials
        except Exception:
            raise ConnectionError(AuthManagerConfigs.invalid_session_message)

    def get_current_session_metadata(self) -> CompanyMetadata:
        """Returns the current session company metadata

        Returns
        -------
        CompanyMetadata
            An object containing the company metadata
        """

        if self.current_site_metadata:
            return self.current_site_metadata

        return self._set_metadata_for_current_url()

    def _set_metadata_for_current_url(self) -> CompanyMetadata:
        """
        Retrieve the metadata from the specified url.

        Returns
        -------
        The CompanyMetadata object that encapsulates all the metadata.
        """

        try:
            if not self.current_client:
                self.current_client = self.login_client_on_current_url()
            if self.current_client and self.current_client.config.metadata:
                self.current_site_metadata = CompanyMetadata(**self.current_client.config.metadata)
                return self.current_site_metadata
            raise
        except ValidationError as exc:
            raise MandatoryConfigurationsException(exc)
        except Exception:
            raise ValueError(AuthManagerConfigs.invalid_session_message)

    def refresh_metadata(self) -> Optional[KelvinSDKGlobalConfiguration]:
        """
        A simple wrapper method to refresh metadata on request.

        :return: a boolean indicating whether or not the metadata was successfully refreshed.
        """
        try:
            # 1 - Get the current configuration
            ksdk_configuration = self.get_global_ksdk_configuration()

            # 2 - Assess the last timestamp
            try:
                last_metadata_retrieval = int(ksdk_configuration.kelvin_sdk.last_metadata_refresh)
            except TypeError:
                last_metadata_retrieval = 0
            # 3 - check the difference
            time_difference = time.time() - last_metadata_retrieval
            twelve_hours_cap_is_crossed = time_difference >= 12 * 3600
            # 4 - If it crosses the 12h threshold, force refresh
            if twelve_hours_cap_is_crossed:
                logger.info("Refreshing metadata..")
                self.login_client_on_current_url(force_metadata=True)
                url_metadata = self.get_current_session_metadata()

                ksdk_configuration.ksdk_schema_dir_path.delete_dir()
                ksdk_configuration.kelvin_sdk.last_metadata_refresh = time.time()
                ksdk_configuration.kelvin_sdk.ksdk_minimum_version = url_metadata.sdk.ksdk_minimum_version
                ksdk_configuration.kelvin_sdk.ksdk_latest_version = url_metadata.sdk.ksdk_latest_version
                self.global_ksdk_configuration = ksdk_configuration.commit_ksdk_configuration()
                return self.global_ksdk_configuration
        except ConnectionError:
            logger.debug("Could not retrieve metadata. Proceeding regardless..")
        return None

    def launch_ipython_client(self, args: Sequence[str]) -> None:
        """
        Launch an interactive IPython console with the pre-logged, already-built (kelvin.sdk.client) client.

        """
        import IPython
        from traitlets.config import Config

        if args:
            sys.argv[:] = args
            if args[0] == "-":
                args = ("", *args[1:])
        else:
            sys.argv[:] = [""]

        config = Config()
        config.TerminalInteractiveShell.banner1 = ""
        config.TerminalInteractiveShell.banner2 = """
            **************** Kelvin SDK Client *****************
            ************ Platform API access loaded ************
            *** type 'client' and tab to autocomplete ***
        """

        try:

            user_ns = {"client": self.login_client_on_current_url()}
            sys.exit(IPython.start_ipython(["--", *args], user_ns=user_ns, config=config))
        except Exception as exc:
            logger.exception(str(exc))

    # ? - Global KSDK Configurations
    def global_configurations_list(self, should_display: bool = False) -> OperationResponse:
        """
        List all available configurations for the Kelvin-SDK

        :param should_display: specifies whether or not the display should output data.

        :return: an OperationResponse object encapsulating the yielded Kelvin tool configurations.

        """
        try:
            global_ksdk_configuration = self.get_global_ksdk_configuration()
            descriptions = global_ksdk_configuration.kelvin_sdk.configurations.descriptions
            private_fields = global_ksdk_configuration.kelvin_sdk.configurations.private_fields

            data = [v for k, v in descriptions.items() if k not in private_fields]

            display_obj = display_data_entries(
                data=data,
                header_names=["Variable", "Description", "Current Value"],
                attributes=["env", "description", "current_value"],
                table_title=GeneralConfigs.table_title.format(title="Environment Variables"),
                should_display=should_display,
            )
            set_unset_command = success_colored_message("kelvin configuration set/unset")
            logger.info(f"See {set_unset_command} for more details on how to configure this tool.")
            return OperationResponse(success=True, data=display_obj.parsed_data)

        except Exception as exc:
            error_message = f"Error retrieving environment variable configurations: {str(exc)}"
            logger.exception(error_message)
            return OperationResponse(success=False, log=error_message)

    def global_configurations_set(self, configuration: str, value: str) -> OperationResponse:
        """
        Set the specified configuration on the platform system.

        :param configuration: the configuration to change.
        :param value: the value that corresponds to the provided configuration.

        :return: an OperationResponse object encapsulating the result the configuration set operation.

        """
        try:
            global_ksdk_configuration = self.get_global_ksdk_configuration()
            global_ksdk_configuration.set_configuration(configuration=configuration, value=value)
            success_message = f'Successfully set "{configuration}" to "{value}"'
            logger.relevant(success_message)
            return OperationResponse(success=True, log=success_message)
        except Exception as exc:
            error_message = f"Error setting configuration variable: {str(exc)}"
            logger.exception(error_message)
            return OperationResponse(success=False, log=error_message)

    def global_configurations_unset(self, configuration: str) -> OperationResponse:
        """
        Unset the specified configuration from the platform system

        :param configuration: the configuration to unset.

        :return: an OperationResponse object encapsulating the result the configuration unset operation.

        """
        try:
            global_ksdk_configuration = self.get_global_ksdk_configuration()
            global_ksdk_configuration.unset_configuration(configuration=configuration)
            success_message = f'Successfully unset "{configuration.lower()}"'
            logger.relevant(success_message)
            return OperationResponse(success=True, log=success_message)
        except Exception as exc:
            error_message = f"Error un-setting configuration variable: {str(exc)}"
            logger.exception(error_message)
            return OperationResponse(success=False, log=error_message)


session_manager = SessionManager()
