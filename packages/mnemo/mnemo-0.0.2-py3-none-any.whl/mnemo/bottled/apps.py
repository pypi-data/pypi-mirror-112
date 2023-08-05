"""
@author: Gabriele Girelli
@contact: gigi.ga90@gmail.com
"""

from bottle import Bottle  # type: ignore


def get_base_app() -> Bottle:
    return Bottle()
