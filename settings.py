#! -*- coding: utf-8 -*-

import base64


# FLASK SETTINGS
HOSTNAME = "localhost"
PORT = 5000

# DATABASE SETTINGS
DB_USERNAME = "lookies"
DB_PASSWORD = base64.b64decode(b'bG9va2llcw==').decode()

DB_HOSTNAME = "localhost"
DB_PORT = "5432"
DB_NAME = "hackatonrtf"
