"""
@author: Gabriele Girelli
@contact: gigi.ga90@gmail.com
"""

import os

import mnemo

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
DEFAULT_ROOT_PATH = os.path.join(mnemo.__path__[0], "bottled")
DEFAULT_DB_PATH = os.path.join(DEFAULT_ROOT_PATH, "db", "db.json")
DEFAULT_TEMPLATE_PATH = os.path.join(DEFAULT_ROOT_PATH, "templates")
