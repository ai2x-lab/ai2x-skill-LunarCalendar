"""Domain-specific exceptions."""

class CalendarEngineError(Exception):
    """Base exception for calendar engine errors."""


class CacheError(CalendarEngineError):
    """Raised when cache loading or validation fails."""


class RuleError(CalendarEngineError):
    """Raised when festival rules are malformed."""


class QueryError(CalendarEngineError):
    """Raised when query parameters are invalid."""

