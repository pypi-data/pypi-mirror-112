from typing import Any, Dict, List, Optional

from pydantic import Field
from pydantic.types import constr

from kelvin.sdk.lib.configs.internal.datatype_configs import DatatypeConfigs
from kelvin.sdk.lib.exceptions import DataTypeException
from kelvin.sdk.lib.models.generic import KSDKModel


class DottedIdentifierWithVersion(KSDKModel):
    __root__: constr(regex=r"^([a-z][a-z0-9_]+\.)+[a-z][a-z0-9_]+:[^:]+$")  # type: ignore # noqa


class DottedIdentifierWithOptionalVersion(KSDKModel):
    __root__: constr(regex=r"^([a-z][a-z0-9_]+\.)+[a-z][a-z0-9_]+:?[^:]+$")  # type: ignore # noqa


class ICDField(KSDKModel):
    description: str
    name: str
    type: str
    array: Optional[bool]


class ICDPayloadHelper(KSDKModel):
    name: constr(regex=DatatypeConfigs.datatype_name_acceptance_regex)  # type: ignore # noqa
    class_name: constr(regex=DatatypeConfigs.datatype_class_name_acceptance_regex)  # type: ignore # noqa
    description: str
    payload_fields: List[ICDField] = Field(..., alias="fields")
    version: str

    class Config:
        allow_population_by_field_name: bool = True

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return super().dict(by_alias=True, *args, **kwargs)

    @property
    def datatype_file_name(self) -> str:
        """
        Based on the data type name and its version, get the project specific file name.

        :return: the name of the file that will be created to host the new Datatype

        """

        if not self.name or not self.version:
            raise DataTypeException("Datatype requires both a name and a version")

        name: str = self.name.replace(".", "_")
        version: str = self.version.replace(".", "-")

        return f"{name}__{version}{DatatypeConfigs.datatype_default_icd_extension}"

    @property
    def full_datatype_name(self) -> str:
        return f"{self.name}:{self.version}"

    @property
    def dependency_datatypes(self) -> List[str]:
        return_obj = []
        for item in self.payload_fields:
            if item.type and item.type.count(":") == 1:
                return_obj.append(item.type)
        return list(set(return_obj))
