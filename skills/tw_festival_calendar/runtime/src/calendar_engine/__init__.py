"""Taiwan local-first festival calendar engine package."""

from .config import CREATOR_EMAIL, CREATOR_NAME, ENGINE_VERSION
from .services.lookup_service import LookupService

__version__ = ENGINE_VERSION
__creator_name__ = CREATOR_NAME
__creator_email__ = CREATOR_EMAIL

__all__ = [
    "LookupService",
    "__version__",
    "__creator_name__",
    "__creator_email__",
]

