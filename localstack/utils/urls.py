from typing import Optional

from localstack import config, constants
from localstack.config import HostAndPort


def path_from_url(url: str) -> str:
    return f'/{url.partition("://")[2].partition("/")[2]}' if "://" in url else url


def hostname_from_url(url: str) -> str:
    return url.split("://")[-1].split("/")[0].split(":")[0]


def localstack_host(
    use_hostname_external: bool = False,
    use_localstack_hostname: bool = False,
    use_localhost_cloud: bool = False,
    custom_host: str | None = None,
    custom_port: Optional[int] = None,
) -> HostAndPort:
    """
    Determine the host and port to return to the user based on:
    - the user's configuration (e.g environment variable overrides)
    - the defaults of the system
    """
    port = config.EDGE_PORT
    if custom_port is not None:
        port = custom_port

    if config.USE_LOCALSTACK_HOST:
        host = config.LOCALSTACK_HOST
        if custom_port:
            host.port = port
        return host

    host = config.LOCALHOST
    if use_hostname_external:
        host = config.HOSTNAME_EXTERNAL
    elif use_localstack_hostname:
        host = config.LOCALSTACK_HOSTNAME
    elif use_localhost_cloud:
        host = constants.LOCALHOST_HOSTNAME
    elif custom_host:
        host = custom_host

    return HostAndPort(host=host, port=port)
