from requests import RequestException


class MCPException(Exception):
    """Base exception for MCP server."""

    pass


class AuthenticationError(MCPException):
    """Raised when authentication fails."""

    pass


class ValidationError(MCPException):
    """Raised when input validation fails."""

    pass


class ServiceError(MCPException):
    """Raised when a service operation fails."""

    pass


class ExternalAPIError(RequestException):
    """Raised when an external API request fails."""

    pass
