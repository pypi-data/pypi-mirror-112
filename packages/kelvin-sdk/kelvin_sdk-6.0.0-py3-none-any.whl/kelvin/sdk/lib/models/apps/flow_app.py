from pydantic import Extra

from kelvin.sdk.lib.models.generic import KSDKModel


class FlowAppType(KSDKModel):
    class Config:
        extra = Extra.allow
