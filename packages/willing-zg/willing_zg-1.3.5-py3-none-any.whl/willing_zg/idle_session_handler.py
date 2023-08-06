from zygoat.components import FileComponent
from zygoat.constants import FrontendUtils

from . import resources


class IdleSessionHandler(FileComponent):
    resource_pkg = resources
    base_path = FrontendUtils
    filename = "IdleSessionHandler.js"
    overwrite = True


idle_session_handler = IdleSessionHandler()
