from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .interface import (
    acp,
    app,
    appregistry,
    asset,
    asset_types,
    authentication,
    configuration,
    datatype,
    emulation,
    label,
    report,
    secrets,
    workload,
)

kelvin_server = FastAPI()
kelvin_server.include_router(acp.router)
kelvin_server.include_router(app.router)
kelvin_server.include_router(appregistry.router)
kelvin_server.include_router(asset.router)
kelvin_server.include_router(asset_types.router)
kelvin_server.include_router(authentication.router)
kelvin_server.include_router(configuration.router)
kelvin_server.include_router(datatype.router)
kelvin_server.include_router(emulation.router)
kelvin_server.include_router(label.router)
kelvin_server.include_router(report.router)
kelvin_server.include_router(secrets.router)
kelvin_server.include_router(workload.router)


@kelvin_server.get("/", response_class=HTMLResponse)
async def root() -> str:
    from kelvin.sdk.cli.version import version as _version

    return f"""
    <html>
        <head>
            <title>Kelvin Server</title>
        </head>
        <body>
            <h2>Welcome to Kelvin Server</h1>
            <h2> Kelvin-SDK version: {_version}:
            <h2>Access the API <a href=/docs>documentation page</a></h2>
        </body>
    </html>
    """


@kelvin_server.get("/info")
async def info() -> dict:
    from kelvin.sdk.cli.version import version as _version
    from kelvin.sdk.lib.configs.internal.general_configs import KSDKHelpMessages
    from kelvin.sdk.lib.session.session_manager import session_manager
    from kelvin.sdk.lib.utils.general_utils import get_system_information

    system_information = get_system_information()
    ksdk_configuration = session_manager.get_global_ksdk_configuration()
    current_url = ksdk_configuration.kelvin_sdk.current_url or KSDKHelpMessages.current_session_login
    return {"current_url": current_url, "version": _version, **system_information}


@kelvin_server.get("/version")
async def version() -> dict:
    from kelvin.sdk.cli.version import version as _version

    return {"version": _version}
