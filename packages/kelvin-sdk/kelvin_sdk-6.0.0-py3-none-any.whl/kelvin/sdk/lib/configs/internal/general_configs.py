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
from typing import List

NANO_SECONDS_OFFSET: float = 10 ** 9


class KSDKHelpMessages:
    # welcome message
    ksdk_welcome_message: str = """    Kelvin SDK:  The complete tool to interact with the Kelvin Ecosystem."""
    # ksdk help
    verbose: str = "Display all executed steps to the screen."
    yes: str = "If specified, will ignore the destructive warning of the operation and proceed."
    docs: str = "Open the kelvin-sdk documentation webpage."
    tree_title: str = """
        Kelvin Command Overview.
    """
    tree_help: str = "Display all available commands in a tree structure."
    current_system_info: str = "Provide system information and the currently logged platform."
    current_session_login: str = "No current session available."
    # login
    login_username: str = "The username used to login on the platform."
    login_password: str = "The password corresponding to the provided user."
    login_totp: str = "The time-based one-time password (TOTP) corresponding to the provided user."
    reset: str = "If specified will reset all local configuration files required by this tool."
    token_full: str = "Return the full authentication token, not just the access authentication token field."
    token_margin: str = """
        Minimum time to expiry (in seconds) for authentication token (new authentication_token retrieved if previous authentication token expires within margin).
        \b
        Set to 0 to retrieve a new authentication_token.
    """
    # applications
    app_description: str = "A simple description for the new app."
    app_type: str = """
        Specify the application type. \n
        Default: "kelvin"
    """
    kelvin_app_lang: str = """
        The programming language of the application.
        Applicable only to applications of type "kelvin". \n
        Default: "python"
    """
    app_dir: str = "The path to the application's directory. Assumes the current directory if not specified."
    status_source: str = """
        The source of data to read from.
        Retrieve from 'cache' or force a 'live' update. \n
        Default: 'cache'.
    """
    # apps
    appregistry_download_override_local_tag: str = "If specified, overrides the local image tag."
    appregistry_upload_datatypes_upload: str = "If specified, will upload locally defined data types."
    # workload list
    workload_list_acp_name: str = "The acp name used to filter the workloads."
    workload_list_app_name: str = "The app name, with version, used to filter the workloads."
    workload_list_enabled: str = "Allows the filtering of workloads by their status."
    # workload deploy
    workload_deploy_acp_name: str = "The acp to associate to the new workload."
    workload_deploy_app_name: str = "The app to associate to the new workload."
    workload_deploy_workload_name: str = "The name of the workload."
    workload_deploy_workload_title: str = "The title of the workload."
    workload_deploy_app_config: str = "The configuration file used to set up the workload."
    # workload bulk-deploy
    workload_deploy_bulk_file_type: str = "Type of the workload file."
    workload_deploy_bulk_ignore_failures: str = "Ignore deployment failures and automatically continue."
    workload_deploy_bulk_skip_successes: str = "Skip deployments already marked as successful."
    workload_deploy_bulk_dry_run: str = "Dry-run to validate inputs only."
    # workload update
    workload_update_app_version: str = "The app version to update the workload with."
    workload_update_workload_title: str = "The new title of the workload."
    workload_update_app_config: str = "The new configuration to be set on the existing workload."
    # workload logs
    workload_logs_tail_lines: str = "The number of lines to display."
    workload_logs_output_file: str = "The output file to write the logs into."
    workload_logs_follow: str = "If specified, follows the logs."
    # datatype list
    datatype_list_all: str = "If specified, will list all data types and its respective versions."
    # datatype create
    datatype_create_input_dir: str = "The directory to read the data types from."
    datatype_create_output_dir: str = "The directory where the new data type will be created."
    # datatype upload
    datatype_upload_input_dir: str = "The directory to read the data types from."
    datatype_upload_names: str = "The data type names to filter the upload operation."
    # datatype download
    datatype_download_output_dir: str = "The directory where the downloaded data type will be put."
    # emulation
    fresh: str = "If specified will remove any cache and rebuild the application from scratch."
    show_logs: str = "Log the application's output once started."
    emulation_logs_tail_lines: str = "Tails the container logs."
    emulation_logs_follow_lines: str = "Follows the container logs stream"
    emulation_app_config: str = "The app configuration file to be used on the emulation."
    emulation_acp_name: str = "The ACP name provided to the runtime."
    emulation_workload_name: str = "The workload name provided to the runtime."
    # report
    report_app_config_file: str = "The path fo the app configuration file to be reported."
    # server
    kelvin_server_port: str = "Specifies the kelvin server port."
    kelvin_server_working_dir: str = """
    Specifies the kelvin server context directory where temporary files will be handled.
    """
    # schema
    schema_file: str = "The path to the schema file to validate the file against."
    schema_errors: str = "Show the full schema validation logs"
    # studio
    studio_schema_file: str = "The schema file used to power the Kelvin Studio's interface."
    studio_input_file: str = "The input file to modify based on the schema file."
    studio_port: str = "Specifies the studio server port."
    # secrets
    secret_create_value: str = "The value corresponding to the secret."
    secret_list_filter: str = "The query to filter the secrets by."
    # assets
    asset_type_name: str = "The asset type name to associate to the asset."
    asset_title: str = "The title to associate to the asset."
    # labels
    label_list_filter: str = "The query to filter the labels by."
    # completion
    autocomplete_message: str = """\
        Generate command-completion configuration for KSDK commands.
        \b

        To configure your shell to complete KSDK commands:

        \b
            Bash:

                $ kelvin configuration autocomplete --shell bash > ~/.bashrc.ksdk
                $ echo "source ~/.bashrc.ksdk" >> ~/.bashrc

        \b
            ZSH:

                $ kelvin configuration autocomplete --shell zsh > ~/.zshrc.ksdk
                $ echo "source ~/.zshrc.ksdk" >> ~/.zshrc"""
    shell: str = "Name of the shell to generate completion configuration, e.g. bash, zsh, fish"
    # injector
    data_injector_app_name: str = "The app to inject data into."
    data_injector_endpoint: str = "The endpoint to publish."
    data_injector_poller_period: str = "The rate at which data will be polled from the application."
    data_injector_repeat: str = "Repeat data injection forever."
    data_injector_ignore_timestamps: str = "Ignore timestamps in data"
    # extractor
    data_extractor_output_dir: str = "The directory into which data will be output"
    data_extractor_batch: str = "The extractor batch write frequency."
    # model service
    model_service_dir: str = (
        "The path to the model service's directory. Assumes the current directory if not specified."
    )
    model_service_config: str = "The model service configuration file to be used when running the service."


class GeneralConfigs:
    # documentation link
    docs_url: str = "https://docs.kelvininc.com"
    # configuration files
    default_report_file: str = "kelvin_report.txt"
    default_ksdk_configuration_dir: str = "~/.config/kelvin/"
    default_ksdk_temp_dir: str = "temp"
    default_ksdk_schema_storage_dir: str = "schemas"
    default_ksdk_datatype_storage_dir: str = "datatypes"
    default_ksdk_history_file: str = "ksdk_history.log"
    default_ksdk_configuration_file: str = "ksdk.yaml"
    default_kelvin_sdk_client_configuration_file: str = "client.yaml"
    # default app names
    default_app_description: str = "Default description."
    default_app_version: str = "1.0.0"
    # dirs
    default_app_dir: str = "app"
    default_server_dir: str = "server"
    default_artifacts_dir: str = "artifacts"
    default_build_dir: str = "build"
    default_data_dir: str = "data"
    default_datatype_dir: str = "datatype"
    default_docs_dir: str = "docs"
    default_tests_dir: str = "tests"
    default_wheels_dir: str = "wheels"
    # files
    default_python_init_file: str = "__init__.py"
    default_python_main_file: str = "__main__.py"
    default_python_setup_file: str = "setup.py"
    default_python_config_file: str = "config.py"
    default_python_test_file: str = "test_application.py"
    default_app_config_file: str = "app.yaml"
    default_migrated_app_config_file: str = "app.yaml"
    default_git_keep_file: str = ".keep"
    default_git_ignore_file: str = ".gitignore"
    default_dockerignore_file: str = ".dockerignore"
    default_requirements_file: str = "requirements.txt"
    default_requirements_tests_file: str = "requirements.tests.txt"
    default_system_packages_file: str = "sys_requirements.txt"
    default_dockerfile: str = "Dockerfile"
    default_build_logs_file: str = "build.log"
    default_executable: str = "run_app"
    default_readme_file: str = "README.md"
    default_mqtt_config_file: str = "/mosquitto/config/mosquitto.conf"
    # cpp
    default_cmakelists_file: str = "CMakeLists.txt"
    default_makefile: str = "Makefile"
    # data images
    table_title: str = "*************************** {title} ***************************"
    # date visualization
    default_datetime_visualization_format: str = "%Y-%m-%d %H:%M:%S %z"
    default_datetime_and_elapsed_display: str = "{base_date}  ({now_minus_base_date})"
    # default env creation
    default_kelvin_app_dependency: str = "kelvin-app[data]==6.0.0"
    default_kelvin_app_dependency_simple: str = "kelvin-app[data]"
    # model service
    default_model_service_test_file: str = "test_service.py"
    default_model_service_application_file: str = "application.py"
    default_model_service_config_file: str = "config.py"
    default_model_service_io_file: str = "io.py"
    default_model_service_model_file: str = "model.py"
    default_model_service_predict_file: str = "predict.py"
    default_model_service_errors_file: str = "errors.py"
    default_model_service_service_file: str = "service.py"
    default_model_service_yaml_file: str = "model_service.yaml"
    default_model_service_module: str = "app.server.service:app"
    default_model_service_dependencies: List[str] = [
        "PyYAML==5.4.1",
    ]


class GeneralMessages:
    invalid_name: str = "The provided name is not valid. \nErrors:\n{reason}"
    invalid_name_with_version: str = "Please provide a valid name with a version: e.g. 'app:1.0.0'"
    no_data_yielded: str = "No data yielded."
    no_data_available: str = "No data yielded."
    are_you_sure_question: str = "\t    Are you sure? {prompt}"
    provide_a_valid_response: str = "Please provide a valid response. ['yes','y','no','n']\n"
    invalid_file_or_directory: str = "Please provide a valid file type and/or directory."
