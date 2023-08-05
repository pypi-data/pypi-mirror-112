"""
@author: Gabriele Girelli
@contact: gigi.ga90@gmail.com
"""

from mnemo import const, session
from typing import List

from importlib.metadata import version

try:
    __version__ = version(__name__)
except Exception as e:
    raise e

__all__ = ["bottle", "const", "session"]
__path__: List[str]
