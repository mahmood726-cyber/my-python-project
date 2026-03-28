"""Custom exceptions for IPDMA package."""


class IPDMAError(Exception):
    """Base exception for IPDMA package."""
    pass


class ConvergenceError(IPDMAError):
    """Raised when model fails to converge."""
    pass


class DataError(IPDMAError):
    """Raised when data validation fails."""
    pass


class SpecificationError(IPDMAError):
    """Raised when model specification is invalid."""
    pass


class NetworkError(IPDMAError):
    """Raised for network meta-analysis issues."""
    pass


class TransportError(IPDMAError):
    """Raised for transportability issues."""
    pass