# isort: skip_file
"""Kelvin Application Framework."""

__all__ = [
    "Application",
    "ApplicationConfig",
    "AppStatus",
    "BaseApplication",
    "DataApplication",
    "DataStatus",
    "PollerApplication",
    "KelvinAppConfig",
    "MappingProxy",
]

from .application import AppStatus, BaseApplication, DataApplication, DataStatus, PollerApplication
from .config import ApplicationConfig, KelvinAppConfig
from .mapping_proxy import MappingProxy
from .version import version as __version__

Application = DataApplication
