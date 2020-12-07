"""oastodcat package.

Modules:
    oas_dataservice
"""
try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from .oas_dataservice import create_id
from .oas_dataservice import NotSupportedOASError
from .oas_dataservice import NotValidOASError
from .oas_dataservice import OASDataService
from .oas_dataservice import RequiredFieldMissingError
