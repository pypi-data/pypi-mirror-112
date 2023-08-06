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

from types import MappingProxyType
from typing import List, Optional

from jinja2 import Environment, PackageLoader, Template

from kelvin.sdk.lib.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.models.apps.kelvin_app import ApplicationInterface, ApplicationLanguage
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import ProjectType
from kelvin.sdk.lib.models.apps.ksdk_app_setup import TemplateFile
from kelvin.sdk.lib.models.types import EmbeddedFiles, FileType


def get_project_templates(
    project_type: ProjectType,
    file_type: FileType,
    kelvin_app_lang: Optional[ApplicationLanguage] = None,
    kelvin_app_interface: Optional[ApplicationInterface] = None,
) -> List[TemplateFile]:
    """
    When provided with a programming language and file type, retrieve all of the respective templates.

    :param project_type: the project types of the desired templates.
    :param kelvin_app_lang: the programming app language of the desired templates.
    :param kelvin_app_interface: the programming app language of the desired templates.
    :param file_type: the type of templates to retrieve (either app templates or configuration templates).

    :return: a list of TemplateFiles.

    """

    if project_type == ProjectType.kelvin:
        templates = (
            _project_templates.get(project_type, {})
            .get(kelvin_app_lang, {})
            .get(kelvin_app_interface, {})
            .get(file_type, [])
        )
    else:  # Both ProjectType.docker and ModelServiceType.default are docker applications
        templates = _project_templates.get(project_type, {}).get(file_type, [])

    return [
        TemplateFile(
            name=item.get("name"),
            content=_retrieve_template(template_name=item.get("content", "")),
            options=item.get("options", {}),
        )
        for item in templates
    ]


def get_embedded_file(embedded_file: EmbeddedFiles) -> Template:
    """
    When provided with an embedded app type and file type, retrieve all of the respective templates.

    :param embedded_file: the type of the embedded app to retrieve the templates from.

    :return: a list of TemplateFiles.

    """
    template = _embedded_files.get(embedded_file, {})

    return _retrieve_template(template_name=template)


def _retrieve_template(template_name: str) -> Template:
    """
    Retrieve the Jinja2 Template with the specified template name (path).

    :param template_name: the name of the template to retrieve.

    :return: a Jinja2 template.

    """
    templates_package_loader = PackageLoader(package_name="kelvin.sdk.lib", package_path="templates")
    templates_environment = Environment(loader=templates_package_loader, trim_blocks=True, autoescape=True)
    return templates_environment.get_template(name=template_name)


class Templates:
    files_default_dockerignore: str = "files/default_dockerignore.jinja2"
    files_default_empty_file: str = "files/default_empty_file.jinja2"


_project_templates: MappingProxyType = MappingProxyType(
    {
        ProjectType.kelvin: {
            ApplicationLanguage.python: {
                ApplicationInterface.client: {
                    FileType.APP: [
                        {
                            "name": GeneralConfigs.default_python_init_file,
                            "content": "apps/kelvin/python/python_app_init_file.jinja2",
                        },
                        {
                            "name": "{app_file_system_name}{app_lang_extension}",
                            "content": "apps/kelvin/python/python_app_file.jinja2",
                        },
                    ],
                    FileType.CONFIGURATION: [
                        {
                            "name": GeneralConfigs.default_python_setup_file,
                            "content": "apps/kelvin/python/python_app_setup_file.jinja2",
                        },
                        {
                            "name": GeneralConfigs.default_requirements_file,
                            "content": "apps/kelvin/python/python_app_requirements_file.jinja2",
                        },
                        {
                            "name": GeneralConfigs.default_git_ignore_file,
                            "content": "apps/kelvin/python/python_app_gitignore_file.jinja2",
                        },
                        {
                            "name": GeneralConfigs.default_dockerignore_file,
                            "content": Templates.files_default_dockerignore,
                        },
                    ],
                    FileType.BUILD: [],
                    FileType.DATA: [
                        {
                            "name": GeneralConfigs.default_git_keep_file,
                            "content": Templates.files_default_empty_file,
                        },
                    ],
                    FileType.DATATYPE: [
                        {
                            "name": GeneralConfigs.default_git_keep_file,
                            "content": Templates.files_default_empty_file,
                        },
                    ],
                    FileType.DOCS: [
                        {
                            "name": GeneralConfigs.default_git_keep_file,
                            "content": Templates.files_default_empty_file,
                        },
                    ],
                    FileType.TESTS: [
                        {
                            "name": GeneralConfigs.default_python_test_file,
                            "content": "apps/kelvin/python/python_app_tests_file.jinja2",
                        },
                    ],
                    FileType.WHEELS: [
                        {
                            "name": GeneralConfigs.default_git_keep_file,
                            "content": Templates.files_default_empty_file,
                        },
                    ],
                },
            },
            ApplicationLanguage.cpp: {
                ApplicationInterface.data: {
                    FileType.APP: [
                        {
                            "name": "{app_file_system_name}{app_lang_extension}",
                            "content": "apps/kelvin/cpp/cpp_app_implementation.jinja2",
                        },
                        {
                            "name": "{app_file_system_name}{cpp_app_header_extension}",
                            "content": "apps/kelvin/cpp/cpp_app_header.jinja2",
                        },
                        {
                            "name": GeneralConfigs.default_cmakelists_file,
                            "content": "apps/kelvin/cpp/cpp_app_make_build.jinja2",
                        },
                    ],
                    FileType.CONFIGURATION: [
                        {
                            "name": GeneralConfigs.default_git_ignore_file,
                            "content": "apps/kelvin/cpp/cpp_app_gitignore.jinja2",
                        },
                        {
                            "name": GeneralConfigs.default_dockerignore_file,
                            "content": Templates.files_default_dockerignore,
                        },
                    ],
                    FileType.BUILD: [],
                    FileType.DATA: [
                        {
                            "name": GeneralConfigs.default_git_keep_file,
                            "content": Templates.files_default_empty_file,
                        },
                    ],
                    FileType.DATATYPE: [
                        {
                            "name": GeneralConfigs.default_git_keep_file,
                            "content": Templates.files_default_empty_file,
                        },
                    ],
                    FileType.DOCS: [
                        {
                            "name": GeneralConfigs.default_git_keep_file,
                            "content": Templates.files_default_empty_file,
                        },
                    ],
                    FileType.TESTS: [
                        {
                            "name": GeneralConfigs.default_git_keep_file,
                            "content": Templates.files_default_empty_file,
                        },
                    ],
                },
            },
        },
        ProjectType.docker: {
            FileType.CONFIGURATION: [
                {
                    "name": GeneralConfigs.default_dockerignore_file,
                    "content": Templates.files_default_dockerignore,
                },
                {
                    "name": GeneralConfigs.default_dockerfile,
                    "content": Templates.files_default_empty_file,
                },
            ],
        },
        ProjectType.model_service: {
            FileType.ARTIFACTS: [],
            FileType.APP: [
                {
                    "name": GeneralConfigs.default_python_init_file,
                    "content": Templates.files_default_empty_file,
                },
                {
                    "name": GeneralConfigs.default_model_service_io_file,
                    "content": "model_services/model_service_io_file.jinja2",
                },
                {
                    "name": GeneralConfigs.default_model_service_model_file,
                    "content": "model_services/model_service_model_file.jinja2",
                },
            ],
            FileType.APP_MODULE: [
                {
                    "name": GeneralConfigs.default_python_init_file,
                    "content": Templates.files_default_empty_file,
                },
                {
                    "name": GeneralConfigs.default_model_service_application_file,
                    "content": "model_services/server/model_service_application_file.jinja2",
                },
                {
                    "name": GeneralConfigs.default_model_service_config_file,
                    "content": "model_services/server/model_service_config_file.jinja2",
                },
                {
                    "name": GeneralConfigs.default_model_service_errors_file,
                    "content": "model_services/server/model_service_errors_file.jinja2",
                },
                {
                    "name": GeneralConfigs.default_model_service_io_file,
                    "content": "model_services/server/model_service_io_file.jinja2",
                },
                {
                    "name": GeneralConfigs.default_model_service_predict_file,
                    "content": "model_services/server/model_service_predict_file.jinja2",
                },
                {
                    "name": GeneralConfigs.default_model_service_service_file,
                    "content": "model_services/server/model_service_service_file.jinja2",
                },
            ],
            FileType.TESTS: [
                {
                    "name": GeneralConfigs.default_python_init_file,
                    "content": Templates.files_default_empty_file,
                },
                {
                    "name": GeneralConfigs.default_model_service_test_file,
                    "content": "model_services/model_service_tests_file.jinja2",
                },
            ],
            FileType.CONFIGURATION: [
                {
                    "name": GeneralConfigs.default_dockerignore_file,
                    "content": Templates.files_default_dockerignore,
                },
                {
                    "name": GeneralConfigs.default_readme_file,
                    "content": "model_services/model_service_readme_file.jinja2",
                },
                {
                    "name": GeneralConfigs.default_dockerfile,
                    "content": "model_services/model_service_dockerfile.jinja2",
                },
                {
                    "name": GeneralConfigs.default_requirements_file,
                    "content": "files/default_requirements_file.jinja2",
                },
                {
                    "name": GeneralConfigs.default_requirements_tests_file,
                    "content": "model_services/model_service_requirements_tests_file.jinja2",
                },
                {
                    "name": GeneralConfigs.default_model_service_yaml_file,
                    "content": "model_services/model_service_yaml_file.jinja2",
                },
            ],
        },
    },
)

_embedded_files: MappingProxyType = MappingProxyType(
    {
        EmbeddedFiles.EMPTY_FILE: Templates.files_default_empty_file,
        EmbeddedFiles.DOCKERIGNORE: Templates.files_default_dockerignore,
        EmbeddedFiles.DEFAULT_DATATYPE_TEMPLATE: "files/default_datatype_icd.jinja2",
        EmbeddedFiles.PYTHON_APP_GITIGNORE: "apps/kelvin/python/python_app_gitignore_file.jinja2",
        EmbeddedFiles.PYTHON_APP_DOCKERFILE: "apps/kelvin/python/python_app_dockerfile.jinja2",
        EmbeddedFiles.CPP_APP_DOCKERFILE: "apps/kelvin/cpp/cpp_app_dockerfile.jinja2",
    }
)
