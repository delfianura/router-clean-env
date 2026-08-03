"""Minimal semantic router used to simulate real PR-sized changes."""

import time
from dataclasses import dataclass


@dataclass
class Route:
    name: str
    keywords: list[str]
    priority: int = 0


class Router:
    """Routes an incoming query to the highest-priority matching route."""

    def __init__(self, routes: list[Route] | None = None, cache_ttl: float | None = None) -> None:
        self._routes: list[Route] = routes or []
        self._cache_ttl = cache_ttl
        self._cache: dict[str, tuple[str | None, float]] = {}

    def add_route(self, route: Route) -> None:
        self._routes.append(route)

    def route(self, query: str) -> str | None:
        if self._cache_ttl is not None:
            cached = self._cache.get(query)
            if cached is not None and time.monotonic() - cached[1] < self._cache_ttl:
                return cached[0]

        matches = [r for r in self._routes if any(k in query for k in r.keywords)]
        result = None
        if matches:
            matches.sort(key=lambda r: r.priority, reverse=True)
            result = matches[0].name

        if self._cache_ttl is not None:
            self._cache[query] = (result, time.monotonic())

        return result
