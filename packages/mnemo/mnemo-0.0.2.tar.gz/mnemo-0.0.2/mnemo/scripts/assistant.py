"""
@author: Gabriele Girelli
@contact: gigi.ga90@gmail.com
"""

from bottle import run  # type: ignore
import click
import os
from tinydb import TinyDB  # type: ignore
from typing import Any, Dict

import mnemo
from mnemo.bottled.apps import get_base_app
from mnemo.bottled.routes import (
    add_file_route,
    add_get_route,
    add_post_route,
    add_templated_route,
)
from mnemo.const import CONTEXT_SETTINGS, DEFAULT_DB_PATH, DEFAULT_ROOT_PATH
from mnemo.session import Session


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--address",
    "-a",
    help="server address to access mnemo",
    type=click.STRING,
    default="localhost",
    show_default=True,
)
@click.option(
    "--port",
    "-p",
    help="server port to access mnemo",
    type=click.INT,
    default=8080,
    show_default=True,
)
@click.option(
    "--database",
    "-d",
    help="path to db.json file",
    type=click.STRING,
    default=DEFAULT_DB_PATH,
    show_default=True,
)
@click.option(
    "--auto-reload",
    "-r",
    help="activates auto-reload of the server upon code changes, mainly for developers",
    type=click.BOOL,
    default=False,
    is_flag=True,
)
@click.version_option(mnemo.__version__)
def __main(address: str, port: int, database: str, auto_reload: bool) -> None:
    app = get_base_app()
    db = TinyDB(DEFAULT_DB_PATH)

    app_data: Dict[str, Any] = {}
    app_data["root_path"] = DEFAULT_ROOT_PATH
    app_data["session"] = Session(db)

    add_file_route(app, os.path.join(mnemo.const.DEFAULT_ROOT_PATH, "js"), "js")
    add_file_route(app, os.path.join(mnemo.const.DEFAULT_ROOT_PATH, "css"), "css")

    add_templated_route(app, "/", "pages/home", app_data)
    add_templated_route(app, "/profile", "pages/profile", app_data)
    add_templated_route(app, "/journal", "pages/journal", app_data)
    add_templated_route(app, "/notes", "pages/notes", app_data)

    add_post_route(app, "/first_setup", "responses/first_setup_response", app_data)
    add_post_route(app, "/login", "responses/login_response", app_data)
    add_get_route(app, "/logout", "responses/logout_response", app_data)
    add_post_route(
        app, "/profile_edit_field", "responses/profile_edit_field_response", app_data
    )

    run(app, host=address, port=port, server="paste", reloader=auto_reload)
