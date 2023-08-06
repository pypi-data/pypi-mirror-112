"""An HTTP Request metric"""

from baretypes import (
    Scope,
    Info,
    RouteMatches
)

from jetblack_metrics import TimedMetric


class HttpRequestMetric(TimedMetric):
    """A metric which holds HTTP information."""

    def __init__(
            self,
            host: str,
            app_name: str,
            scope: Scope,
            info: Info,
            matches: RouteMatches
    ) -> None:
        """Create an HTTP request metric

        Args:
            host (str): The host
            app_name (str): The name of the application
            scope (Scope): The ASGI scope
            info (Info): The application defined info
            matches (RouteMatches): The route matches
        """
        super().__init__()
        self.host = host
        self.app_name = app_name
        self.scope = scope
        self.info = info
        self.matches = matches
        self.status = 500
