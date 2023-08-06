"""The promethues monitor page"""

from prometheus_client import (  # type: ignore
    CONTENT_TYPE_LATEST,
    generate_latest
)

from bareasgi import bytes_writer

from baretypes import (
    Scope,
    Info,
    RouteMatches,
    Content,
    HttpResponse
)


async def prometheus_view(
        _scope: Scope,
        _info: Info,
        _matches: RouteMatches,
        _content: Content
) -> HttpResponse:
    """The endpoint for prometheus stats

    Args:
        _scope (Scope): The scope.
        _info (Info): The info.
        _matches (RouteMatches): The route matches
        _content (Content): The contents

    Returns:
        HttpResponse: The prometheus statistics
    """
    headers = [
        (b'content-type', CONTENT_TYPE_LATEST.encode('ascii'))
    ]
    body = generate_latest()
    return 200, headers, bytes_writer(body)
