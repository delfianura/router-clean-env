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

    def __init__(
        self,
        routes: list[Route] | None = None,
        cache_ttl: float | None = None,
        default_route: str | None = None,
    ) -> None:
        self._routes: list[Route] = routes or []
        self._cache_ttl = cache_ttl
        self._cache: dict[str, tuple[str | None, float]] = {}
        self._default_route = default_route

    def add_route(self, route: Route) -> None:
        self._routes.append(route)
        self._cache.clear()

    def remove_route(self, name: str) -> None:
        self._routes = [r for r in self._routes if r.name != name]
        self._cache.clear()

    def set_priority(self, name: str, priority: int) -> None:
        for r in self._routes:
            if r.name == name:
                r.priority = priority
        self._cache.clear()

    def clear_routes(self) -> None:
        self._routes = []
        self._cache.clear()

    _MISS = object()

    def route(self, text: str) -> str | None:
        cached = self._cache_get(text)
        if cached is not self._MISS:
            return cached

        result = self._best_match(text)
        self._cache_set(text, result)
        return result

    def _best_match(self, text: str) -> str | None:
        lowered = text.lower()
        matches = [r for r in self._routes if any(k.lower() in lowered for k in r.keywords)]
        if not matches:
            return self._default_route
        matches.sort(key=lambda r: r.priority, reverse=True)
        return matches[0].name

    def _cache_get(self, text: str):
        if self._cache_ttl is None:
            return self._MISS
        cached = self._cache.get(text)
        if cached is not None and time.monotonic() - cached[1] < self._cache_ttl:
            return cached[0]
        return self._MISS

    def _cache_set(self, text: str, result: str | None) -> None:
        if self._cache_ttl is not None:
            self._cache[text] = (result, time.monotonic())

    def route_many(self, texts: list[str]) -> list[str | None]:
        return [self.route(t) for t in texts]
