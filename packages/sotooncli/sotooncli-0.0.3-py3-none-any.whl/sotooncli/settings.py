import os
from distutils.util import strtobool

APP_NAME = 'sotooncli'
SERVER_HOST = os.environ.get("SOTOON_SERVER_HOST", "https://gate.sotoon.ir/commander/")
USE_CACHE = bool(strtobool(os.environ.get("SOTOON_USE_CACHE", "True")))
