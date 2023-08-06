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

from typing import Optional

from typeguard import typechecked

from kelvin.sdk.lib.models.operation import OperationResponse


@typechecked
def schema_validate(
    file_path: str, schema_file_path: Optional[str], full_schema_errors: bool = False
) -> OperationResponse:
    """
    Validate a file against a schema.

    Parameters
    ----------
    file_path: The path to the file to validate.
    schema_file_path: The path to the schema file to validate the file against.
    full_schema_errors: The path to the schema file to validate the file against.

    Returns
    -------
    an OperationResponse object encapsulating the result of the file schema validation.

    """
    from kelvin.sdk.lib.schema.schema_manager import validate_schema as _validate_schema

    return _validate_schema(
        file_path=file_path, schema_file_path=schema_file_path, full_schema_errors=full_schema_errors
    )
