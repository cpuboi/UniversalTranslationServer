#!/usr/bin/env python3

"""
Fast Translation translation_server is a fastapi based webserver that translates text.

It uses several ML models, namely:
OPUS-MT
m2m100


TODO: Add a translation handler that rotates between all GPU's in a multithreaded manner (asyncio?)
"""

import sys
import logging
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from translation_server.core.config import Settings
from translation_server.api.router import api_router


Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(stream=sys.stdout,
                    format=Log_Format,
                    level=logging.INFO)
logger = logging.getLogger()


def include_router(app):
    app.include_router(api_router)


def start_application():
    app = FastAPI(title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION)
    include_router(app)
    return app

app = start_application()



