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

from itertools import chain, groupby
from operator import itemgetter
from typing import Dict, Generator, List, Optional, Tuple

from kelvin.sdk.lib.api.datatype import datatype_download, datatype_list, datatype_upload
from kelvin.sdk.lib.configs.internal.datatype_configs import DatatypeConfigs
from kelvin.sdk.lib.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.exceptions import DataTypeException
from kelvin.sdk.lib.models.apps.common import Version
from kelvin.sdk.lib.models.apps.kelvin_app import DataType
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import KelvinAppConfiguration
from kelvin.sdk.lib.models.apps.ksdk_app_setup import KelvinAppBuildingObject
from kelvin.sdk.lib.models.datatypes import ICDPayloadHelper
from kelvin.sdk.lib.models.factories.app_setup_configuration_objects_factory import get_project_building_object
from kelvin.sdk.lib.models.generic import KPath, NameWithVersion
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.models.types import EmbeddedFiles
from kelvin.sdk.lib.session.session_manager import session_manager
from kelvin.sdk.lib.templates.templates_manager import get_embedded_file
from kelvin.sdk.lib.utils.datatype_utils import (
    check_if_datatype_name_is_valid,
    check_if_datatype_name_with_version_is_valid,
)
from kelvin.sdk.lib.utils.display_utils import display_yes_or_no_question
from kelvin.sdk.lib.utils.general_utils import get_files_from_dir, unique_items
from kelvin.sdk.lib.utils.logger_utils import logger


# 1 - App Building
def setup_datatypes(kelvin_app_building_object: KelvinAppBuildingObject) -> Optional[KPath]:
    """
    Handle the datatypes, both the raw datatype folder and app configuration datatype specifications and copy them
    to the intended build dir folder for processing.

    :param kelvin_app_building_object: the KelvinAppBuildingObject used to configure the datatype interaction.

    :return: an optional string indicating the path to the build folder that will contain the models to be compiled.

    """
    logger.info("Processing application data types..")

    datatype_dir_path = kelvin_app_building_object.app_datatype_dir_path
    if datatype_dir_path is None:
        return None

    app_configuration_object: KelvinAppConfiguration = kelvin_app_building_object.app_config_model
    app_config_file_path: KPath = kelvin_app_building_object.app_config_file_path
    kelvin_app_configuration = app_configuration_object.app.app_type_configuration
    app_name = app_configuration_object.info.name
    if kelvin_app_configuration:
        # 1 - retrieves datatypes from the configuration (kelvin->app->data_types)
        datatypes_to_handle = [*(kelvin_app_configuration.data_types or [])]
        datatype_names = {str(x.name) for x in datatypes_to_handle}
        for io in chain(
            kelvin_app_configuration.inputs or [],
            kelvin_app_configuration.outputs or [],
        ):
            if io.data_type in datatype_names:
                continue
            version = (
                DatatypeConfigs.datatype_raw_version
                if io.data_type.startswith("raw.")
                else DatatypeConfigs.datatype_missing_version
            )
            datatype_names |= {str(io.data_type)}
            datatypes_to_handle += [DataType(**{"name": io.data_type, "version": version})]

        # 2 - reset the "build/datatype/" directory
        datatype_dir_path.delete_dir().create_dir()
        # 3 - Ensure the raw datamodel cache is preserved
        cached_datamodels_handled = _download_raw_datatypes_to_cache(target_datatypes_dir_path=datatype_dir_path)
        # 4 - handle the datatypes prior to the upload
        if datatypes_to_handle or cached_datamodels_handled.success:
            logger.info(f'Retrieving data types for "{app_name}"')

            versions: Dict[str, Version] = {}
            if any(x.version.root_value == DatatypeConfigs.datatype_missing_version for x in datatypes_to_handle):
                items = [
                    (x["name"], Version.parse_obj(x["version"]))
                    for x in datatype_list(all_datatypes=True, should_display=False).data
                ]
                key = itemgetter(0)
                groups = groupby(sorted(items, key=key), key=key)
                versions.update((name, max(str(version) for _, version in x)) for name, x in groups)  # type: ignore

            if kelvin_app_building_object.build_for_upload:
                datatypes_successfully_handled = _handle_upload_phase_datatypes(
                    datatypes_to_handle=datatypes_to_handle,
                    input_dir_path=KPath(datatype_dir_path.name),
                    ignore_warning=kelvin_app_building_object.upload_datatypes,
                )
                # 5 - update app's app.yaml by removing datatypes path field after upload
                remove_paths_from_datatypes = any([item.path for item in datatypes_to_handle])
                if datatypes_successfully_handled and remove_paths_from_datatypes:
                    # Commit the changes and proceed
                    datatypes = [datatype.dict(exclude={"path"}) for datatype in datatypes_to_handle]
                    raw_app_config = app_config_file_path.read_yaml()
                    raw_app_config["app"]["kelvin"]["data_types"] = datatypes
                    app_config_file_path.write_yaml(yaml_data=raw_app_config)

            for datatype in datatypes_to_handle:
                if datatype.path:  # local
                    datatype_path = app_config_file_path.parent.absolute() / KPath(datatype.path)
                    ICDPayloadHelper(**datatype_path.read_yaml())
                    datatype_path.clone_into(path=datatype_dir_path)
                else:  # remote
                    if datatype.version.root_value == DatatypeConfigs.datatype_missing_version:
                        try:
                            datatype.version = versions[str(datatype.name)]
                        except KeyError:
                            pass
                    datatype_name_with_version = f"{str(datatype.name)}:{str(datatype.version)}"
                    download_datatype(
                        datatype_name_with_version=datatype_name_with_version,
                        output_dir=datatype_dir_path,
                    )

            content = [content for content in datatype_dir_path.dir_content() if not content.startswith(".")]
            should_compile = bool(content)
            return datatype_dir_path if should_compile else None

    logger.info("No data types to process")
    return None


# 2 - datatype creation
def create_datatype(datatype_name: str, output_dir: Optional[str] = None) -> OperationResponse:
    """
    Creates a data type from the specified parameters.

    Parameters
    ----------
    datatype_name: the name of the datatype to create.
    output_dir: the output directory where the data type will be created.

    Returns
    ----------
    an OperationResponse object encapsulating the result of the data type creation operation.

    """
    try:
        check_if_datatype_name_is_valid(datatype_name=datatype_name)

        # 1 - check if the current output directory is an app.
        datatype_output_dir: KPath = _evaluate_datatype_dir(datatype_dir=output_dir)

        # 2 - Validate the datatype name and determine its file path
        datatype_item = ICDPayloadHelper(
            name=datatype_name,
            version=DatatypeConfigs.datatype_default_version,
            description="",
            payload_fields=[],
            class_name="SomeClassName",  # this is not used
        )
        datatype_file_name = datatype_item.datatype_file_name

        logger.info(f'Creating spec for data type "{datatype_item.name}"')

        # 3 - Render the default ICD sample template
        default_icd_template = get_embedded_file(embedded_file=EmbeddedFiles.DEFAULT_DATATYPE_TEMPLATE)
        default_icd_template_rendered = default_icd_template.render(
            datatype_name=datatype_item.name, datatype_version=datatype_item.version
        )

        # 4 - Write it down on the target file
        template_output_file_path: KPath = datatype_output_dir / datatype_file_name
        template_output_file_path.write_content(content=default_icd_template_rendered)

        # 5 - Log the success message
        output_file: str = str(template_output_file_path.absolute())
        success_message = f'Data type "{datatype_name}" spec successfully created in "{output_file}"'
        logger.relevant(success_message)
        return OperationResponse(success=True, log=success_message)

    except Exception as exc:
        error_message = f"Error creating data type spec file: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


# 3 - datatype upload
def upload_datatypes(input_dir: Optional[str] = None, datatypes: Optional[List[str]] = None) -> OperationResponse:
    """
    Upload all the data types in the provided input directory.

    Parameters
    ----------
    input_dir: the directory to read the data types from.
    datatypes: the names of the data types to upload.

    Returns
    ----------
    an OperationResponse object encapsulating the result of the data type upload operation.

    """
    try:
        # auxiliary variable due to mypy issue with optional str
        datatypes_input_dir: KPath = _evaluate_datatype_dir(datatype_dir=input_dir)

        logger.info(f'Uploading data types from directory "{datatypes_input_dir}"')

        loaded_datatypes = _load_all_datatype_files(input_dir=datatypes_input_dir)
        if datatypes:
            loaded_datatypes = _filter_datatypes(loaded_datatypes=loaded_datatypes, datatype_names=datatypes)
        if loaded_datatypes:
            all_platform_datatypes = datatype_list(all_datatypes=True, should_display=False)
            all_datatypes = [DataType(**item) for item in all_platform_datatypes.data if all_platform_datatypes]
            dependency_tree = _build_datatype_upload_dependency_tree(loaded_datatypes=loaded_datatypes)
            upload_result = _process_datatype_upload_dependency_tree(
                all_platform_datatypes=all_datatypes,
                loaded_datatypes=loaded_datatypes,
                dependency_tree=dependency_tree,
            )
            success_message = "Data types successfully processed"
            logger.relevant(success_message)
            return OperationResponse(success=upload_result, log=success_message)
        else:
            error_message = "No data types to process matching your criteria"
            logger.error(error_message)
            return OperationResponse(success=False, log=error_message)
    except Exception as exc:
        error_message = f"Error uploading data types: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


# 4 - datatype download
def download_datatype(datatype_name_with_version: str, output_dir: Optional[str] = None) -> OperationResponse:
    """
    Download the datatype corresponding to the provided data type id into the provided output dir.

    Parameters
    ----------
    datatype_name_with_version: the name with version of the data type to download.
    output_dir: the path into which the data types should be downloaded.

    Returns
    ----------
    an OperationResponse object encapsulating the result of the data type download operation.

    """
    check_if_datatype_name_with_version_is_valid(app_name_with_version=datatype_name_with_version)

    datatype_output_dir: KPath = _evaluate_datatype_dir(datatype_dir=output_dir)

    name_with_version = NameWithVersion(name=datatype_name_with_version)
    if name_with_version.version is None:
        raise DataTypeException('Please provide a valid datatype version. "datatype:version"')

    acquired_datatype: Optional[ICDPayloadHelper] = datatype_download(
        datatype_name=name_with_version.name,
        datatype_version=name_with_version.version,
        output_dir=datatype_output_dir,
    )
    if acquired_datatype:
        downloaded_datatype_fields = acquired_datatype.dependency_datatypes
        for dependency_datatype_name in downloaded_datatype_fields:
            download_datatype(datatype_name_with_version=dependency_datatype_name, output_dir=datatype_output_dir)

    if not acquired_datatype:
        raise DataTypeException("Error processing data type tree")

    return OperationResponse(success=True, log="datatype successfully downloaded.")


# Internal utils
def _load_all_datatype_files(input_dir: str) -> List[Tuple[str, ICDPayloadHelper]]:
    """
    Load all datatypes from the provided input directory.

    :param input_dir: the input directory to read the datatype files from.

    :return: a list of tuples containing the key and the respective ICDPayloadHelper
    """
    logger.info(f'Loading all data type files from directory "{input_dir}"')

    # 1 - get all datatypes
    yml_file_type: str = DatatypeConfigs.datatype_default_icd_extension
    datatype_files = get_files_from_dir(file_type=yml_file_type, input_dir=input_dir)
    datatype_file_paths = [KPath(input_dir) / file for file in datatype_files]

    # 2 - from the datatype files, load all datatype entries into a list of tuples (path + datatype ICD)
    loaded_datatypes: List = []
    for file in datatype_file_paths:
        yaml_content: Generator = file.read_yaml_all()
        for entry in yaml_content:
            loaded_datatypes.append((file, ICDPayloadHelper(**entry)))

    # 3 - report and return
    total = len(loaded_datatypes)
    logger.relevant(f'{total} data types loaded from directory "{input_dir}"')
    return loaded_datatypes


def _handle_upload_phase_datatypes(
    datatypes_to_handle: List[DataType], input_dir_path: KPath, ignore_warning: bool = False
) -> bool:
    """
    If a local datatype is provided during the appregistry upload phase, make sure to warn the user
    and, if ruled so, upload them.

    Parameters
    ----------
    datatypes_to_handle : the names of the datatypes to handle. Mainly for display purpose.
    input_dir_path : The input directory where the datatypes are hosted.
    ignore_warning: indicates whether the upload warning should be displayed.

    Returns
    -------
    a boolean indicating whether the datatypes have been successfully uploaded.

    """
    local_datatypes = [f"{model.name}:{model.version}" for model in datatypes_to_handle if model.path]

    if local_datatypes:
        local_datatypes_list = ", ".join(local_datatypes)
        local_datatypes_upload_warning: str = f"""

            The application you're trying to upload has references to local data types:

            > {local_datatypes_list}

            Do you wish to upload them to the platform before proceeding?

        """
        if not ignore_warning:
            ignore_warning = display_yes_or_no_question(question=local_datatypes_upload_warning)
        if ignore_warning:
            result = upload_datatypes(input_dir=input_dir_path, datatypes=None)
            if not result.success:
                raise DataTypeException(result.log)

    return True


def _filter_datatypes(
    loaded_datatypes: List[Tuple[str, ICDPayloadHelper]], datatype_names: List[str]
) -> List[Tuple[str, ICDPayloadHelper]]:
    """
    Filter the loaded datatypes list

    :param loaded_datatypes: the list of datatypes to process.
    :param datatype_names: the list of datatypes to filter.

    :return: a list of filtered datatypes tuples
    """

    filtered_datatypes: List[Tuple[str, ICDPayloadHelper]] = []
    filtered_datatypes_names: List[str] = []

    for datatype in loaded_datatypes:
        file, icd = datatype
        if icd.full_datatype_name in datatype_names:
            filtered_datatypes.append(datatype)
            filtered_datatypes_names.append(icd.full_datatype_name)

    # check for not found datatypes
    for datatype_name in datatype_names:
        if datatype_name not in filtered_datatypes_names:
            logger.warn(f'No data type found matching your criteria: "{datatype_name}"')

    total = len(filtered_datatypes)
    if total:
        logger.relevant(f"A total of {total} data types loaded match your criteria: {filtered_datatypes_names}")

    return filtered_datatypes


def _build_datatype_upload_dependency_tree(
    loaded_datatypes: List[Tuple[str, ICDPayloadHelper]]
) -> Tuple[List[str], List[str]]:
    """
    Process the loaded datatypes and retrieve the dependency tree with the correct upload structure.

    :param loaded_datatypes: the list of datatypes to process.

    :return: the organized list datatype names with version, ready to operate.
    """
    logger.info("Processing the data type dependency tree.")
    requires_processing: Dict[str, List[str]] = {}
    prepare_for_upload: List[str] = []

    # 1 - Load the datatypes
    for _, datatype in loaded_datatypes:
        datatype_name_with_version = f"{datatype.name}:{datatype.version}"
        datatype_fields = datatype.payload_fields or []
        has_dependencies: bool = False
        requires_processing[datatype_name_with_version] = []  # Register the datatype in the dependency tree
        for field in datatype_fields:
            # 2 - Custom datatypes must have a semver tag. If not, its a raw sub type and its not processed (go to #4)
            has_dependencies = has_dependencies or bool(field.type and ":" in field.type)
            if has_dependencies and field.type and field.type not in requires_processing[datatype_name_with_version]:
                # 3 - Register each sub datatype reference
                requires_processing[datatype_name_with_version].append(field.type)
        # 4 - if the datatype has no custom datatype in its fields, skip any processing and mark it for upload.
        if not has_dependencies:
            prepare_for_upload.append(datatype_name_with_version)

    verify_on_the_platform = []
    while requires_processing:
        keys = requires_processing.keys()
        items = list(requires_processing.items())
        for key, value in items:
            for item in value:
                if item in keys:
                    prepare_for_upload.append(item)
                else:
                    verify_on_the_platform.append(item)
                prepare_for_upload.append(key)
            del requires_processing[key]

    prepare_for_upload = unique_items(items=prepare_for_upload)
    verify_on_the_platform = unique_items(items=verify_on_the_platform)
    verify_on_the_platform = [item for item in verify_on_the_platform if item not in prepare_for_upload]
    return prepare_for_upload, verify_on_the_platform


def _process_datatype_upload_dependency_tree(
    all_platform_datatypes: List[DataType],
    loaded_datatypes: List[Tuple[str, ICDPayloadHelper]],
    dependency_tree: Tuple[List[str], List[str]],
) -> bool:
    """
    Process the datatype dependency tree and uploaded what is necessary to the platform.

    :param all_platform_datatypes: a list of all platform datatypes.
    :param loaded_datatypes: a list containing all the loaded datatypes.
    :param dependency_tree: the dependency tree composed by the ordered name of datatypes to upload.

    :return: a bool indicating the datatypes were successfully processed.
    """
    logger.info("Initializing the data type upload operation.")

    # 1 - get a list of datatypes as strings
    all_platform_datatypes_names: List[str] = [f"{model.name}:{model.version}" for model in all_platform_datatypes]

    datatypes_to_upload, datatypes_to_check_on_the_platform = dependency_tree
    for datatype in datatypes_to_check_on_the_platform:
        # 2 - if the datatype is not present in the platform nor the local definition, raise an exception
        if datatype not in all_platform_datatypes_names:
            raise DataTypeException(message=f'Invalid data type "{datatype}". Please check the platform')
        else:  # 3 - If the datatype already exists, inform the user
            logger.warn(f'Data type "{datatype}" already present in the system. Skipping.')

    for datatype_name_with_version in datatypes_to_upload:
        if datatype_name_with_version not in all_platform_datatypes_names:
            name, version = datatype_name_with_version.split(":")
            clean = [(file, icd) for (file, icd) in loaded_datatypes if icd.name == name and icd.version == version]
            file, icd = next(iter(clean))
            if icd:
                datatype_uploaded = datatype_upload(datatype_content=icd.dict(), source=str(file))
                if not datatype_uploaded.success:
                    raise DataTypeException("Error processing data type tree")
        else:
            logger.warn(f'Data type "{datatype_name_with_version}" already present in the system. Skipping.')

    return True


def _evaluate_datatype_dir(datatype_dir: Optional[str] = None) -> KPath:
    """
    Check if the provided dir is valid for two conditions:
        1 - Is a valid app directory
        2 - If The output_dir is none, the current dir will be used and must be a valid app directory


    :param datatype_dir: optional output dir

    :return: a resolved and validated KPath
    """
    try:
        # if output dir is an app dir, create the datatype inside the app's datatype folder
        # otherwise create the datatype in the app's root
        if not datatype_dir:
            datatype_dir = ""

        base_build_object = get_project_building_object(app_dir=datatype_dir)
        datatype_output_dir = base_build_object.app_dir_path / GeneralConfigs.default_datatype_dir
    except Exception:
        if not datatype_dir:
            raise DataTypeException("Please provide a valid application directory or specify a directory")
        else:
            datatype_output_dir = KPath(datatype_dir)

    datatype_output_dir = datatype_output_dir.expanduser().resolve()
    return datatype_output_dir


def _download_raw_datatypes_to_cache(
    raw_datatypes_dir_path: Optional[KPath] = None, target_datatypes_dir_path: Optional[KPath] = None
) -> OperationResponse:
    """
    Verifies whether raw datatypes are already cached in the system and ready for building.
    If not, download them into the "raw_datatypes_dir_path".
    Once done, copy them over to the "target_datatypes_dir_path"

    Parameters
    ----------
    raw_datatypes_dir_path : the directory where all raw datatypes are downloaded into & cached.
    target_datatypes_dir_path : the target directory into which datatypes will be copied.

    Returns
    -------
    An operation response objective with result of the download operation
    """
    try:
        # 1 - Retrieve the raw datatypes object
        raw_datatypes = [
            DataType(
                **{
                    "name": name,
                    "version": DatatypeConfigs.datatype_raw_version,
                    "path": DatatypeConfigs.datatype_raw_path,
                }
            )
            for name in DatatypeConfigs.raw_datatype_list
        ]
        # 2 - If no raw datatype dir is provided, assume the default datatype cache dir
        if not raw_datatypes_dir_path:
            raw_datatypes_dir_path = session_manager.get_global_ksdk_configuration().ksdk_datatype_dir_path
        # 3 - Make sure it exists
        raw_datatypes_dir_path.create_dir()
        # 4 - Attempt to load all cached datatypes.
        all_cached_datatypes = _load_all_datatype_files(input_dir=raw_datatypes_dir_path)
        # 5 - Retrieve the unique names of each cached datatype
        cached_datatype_names = [payload_helper.full_datatype_name for _, payload_helper in all_cached_datatypes]
        # 6 - Verify which raw datatypes are yet to be downloaded
        datatypes_to_download = [
            entry for entry in raw_datatypes if entry.name_with_version not in cached_datatype_names
        ]
        # 7 - Download all the missing data types and move forward
        for datatype in datatypes_to_download:
            download_datatype(datatype_name_with_version=datatype.name_with_version, output_dir=raw_datatypes_dir_path)
        # 8 - Clone the datamodels to be built
        if target_datatypes_dir_path:
            raw_datatypes_dir_path.clone_dir_into(path=target_datatypes_dir_path)
    except KeyboardInterrupt:
        raise
    except Exception:
        session_manager.get_global_ksdk_configuration().ksdk_datatype_dir_path.delete_dir()
        raise DataTypeException("Error retrieving raw datatypes.")

    success_message = "Datatypes successfully retrieved from cache."
    return OperationResponse(success=True, log=success_message)
