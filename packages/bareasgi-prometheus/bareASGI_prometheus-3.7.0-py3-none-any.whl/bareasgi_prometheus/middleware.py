"""Prometheus middleware"""

from socket import gethostname
from typing import Optional, Type

from baretypes import (
    Scope,
    Info,
    RouteMatches,
    Content,
    HttpResponse,
    HttpChainedCallback
)

from jetblack_metrics import monitor

from .metrics import HttpRequestMetric, PrometheusHttpRequestMetric


class PrometheusMiddleware:
    """Prometheus Middleware"""

    def __init__(
            self,
            *,
            metric_type: Type[HttpRequestMetric] = None,
            host: Optional[str] = None,
            app_name: Optional[str] = None
    ):
        """Prometheus middleware

        Args:
            metric_type (Type[HttpRequestMetric], optional): The metric type.
                Defaults to None.
            host (Optional[str], optional): The host. Defaults to None.
            app_name (Optional[str], optional): The application name. Defaults
                to None.
        """
        self.metric_type = metric_type or PrometheusHttpRequestMetric
        self.host = host or gethostname()
        self.app_name = app_name or 'bareASGI'

    async def __call__(
            self,
            scope: Scope,
            info: Info,
            matches: RouteMatches,
            content: Content,
            handler: HttpChainedCallback
    ) -> HttpResponse:
        with monitor(self.metric_type(
                self.host,
                self.app_name,
                scope,
                info,
                matches
        )) as metric:
            status, headers, response_content, pushes = await handler(
                scope,
                info,
                matches,
                content
            )
            metric.status = status
            return status, headers, response_content, pushes
