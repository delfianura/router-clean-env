"""Minimal semantic router used to simulate real PR-sized changes."""

from dataclasses import dataclass, field


@dataclass
class Route:
    name: str
    keywords: list[str]
    priority: int = 0


class Router:
    """Routes an incoming query to the highest-priority matching route."""

    def __init__(self, routes: list[Route] | None = None) -> None:
        self._routes: list[Route] = routes or []

    def add_route(self, route: Route) -> None:
        self._routes.append(route)

    def route(self, query: str) -> str | None:
        matches = [r for r in self._routes if any(k in query for k in r.keywords)]
        if not matches:
            return None
        matches.sort(key=lambda r: r.priority, reverse=True)
        return matches[0].name
