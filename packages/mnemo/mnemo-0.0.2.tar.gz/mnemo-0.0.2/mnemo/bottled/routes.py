"""
@author: Gabriele Girelli
@contact: gigi.ga90@gmail.com
"""

import bottle  # type: ignore
from typing import Any, Dict

from mnemo.const import DEFAULT_TEMPLATE_PATH

bottle.TEMPLATES.clear()
bottle.TEMPLATE_PATH.append(DEFAULT_TEMPLATE_PATH)


def add_templated_route(
    app: bottle.Bottle,
    location: str,
    template_key: str,
    template_data: Dict[str, Any] = {},
) -> None:
    @app.route(location)
    def routefun():
        return bottle.template(template_key, **template_data)


def add_text_route(app: bottle.Bottle, location: str, text: str) -> None:
    @app.route(location)
    def routefun():
        return text


def add_file_route(app: bottle.Bottle, path: str, extension: str) -> None:
    @app.route(f"/{extension}/<name:re:[a-z0-9\\.-]+\\.{extension}(\\.map)?>")
    def routefun(name):
        print((path, name))
        return bottle.static_file(name, root=path)


def add_post_route(
    app: bottle.Bottle,
    location: str,
    template_key: str,
    template_data: Dict[str, Any] = {},
) -> None:
    @app.post(location)
    def routefun():
        bottle.response.content_type = "application/json"
        return bottle.template(template_key, request=bottle.request, **template_data)


def add_get_route(
    app: bottle.Bottle,
    location: str,
    template_key: str,
    template_data: Dict[str, Any] = {},
) -> None:
    @app.get(location)
    def routefun():
        bottle.response.content_type = "application/json"
        return bottle.template(template_key, request=bottle.request, **template_data)
