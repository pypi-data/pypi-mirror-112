# Handle setting
#
# Author: F. Mertens

import os

from libpipe.settings import BaseSettings


TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')


class Settings(BaseSettings):

    DEFAULT_SETTINGS = os.path.join(TEMPLATE_DIR, 'default_settings.toml')

    def __init__(self, file, d):
        BaseSettings.__init__(self, file, d)
