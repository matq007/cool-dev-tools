from __future__ import absolute_import
import os

# ENVIRONMENT
__version__ = '1.0.0'

# GLOBAL VARIABLES
EXTENSION = '.tgz'
TMP_FOLDER = '/tmp/'
URL = 'http://cool-dev-tools.net16.net/server.json'

ROOT = os.path.dirname(os.getcwd())
TOOLS_DIR = os.path.expanduser(os.path.join(ROOT, 'src'))
PACKAGE_FOLDER = os.path.expanduser(os.path.join(TOOLS_DIR, 'packages'))
PACKAGE_JSON = os.path.expanduser(os.path.join(TOOLS_DIR, 'packages/packages.json'))

# ASCII ART
INTRO = " ____  ____  ____  _       ____  _____ _       _____  ____  ____  _     ____    \n" \
        "/   _\/  _ \/  _ \/ \     /  _ \/  __// \ |\  /__ __\/  _ \/  _ \/ \   / ___\   \n" \
        "|  /  | / \|| / \|| |     | | \||  \  | | //    / \  | / \|| / \|| |   |    \   \n" \
        "|  \__| \_/|| \_/|| |_/\  | |_/||  /_ | \//     | |  | \_/|| \_/|| |_/\\\\___ | \n" \
        "\____/\____/\____/\____/  \____/\____\\\\__/      \_/  \____/\____/\____/\____/ \n"
