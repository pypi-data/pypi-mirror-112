from kelvin.sdk.lib.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.legacy.models.ksdk_app import KelvinAppConfiguration
from kelvin.sdk.lib.models.generic import KPath


def get_legacy_app_object(app_dir: str) -> KelvinAppConfiguration:
    app_dir_path: KPath = KPath(app_dir)
    app_config_file_path: KPath = app_dir_path / GeneralConfigs.default_app_config_file

    return KelvinAppConfiguration(**app_config_file_path.read_yaml())
