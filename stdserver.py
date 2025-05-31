"""
万能头
"""
import fastapi
import re
import time
import datetime
import asyncio
import os
import threading
import httpx
import json

from typing import *
from fastapi import APIRouter, Header
from fastapi.responses import RedirectResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from broadcasting import Transceiver, Message, register
from quicksend import quick_send_group, quick_send_private

class BotPostEvent(BaseModel):
    time:int
    post_type:str
    self_id:int
    class Config:
        extra = "allow"

NCURL = 'http://127.0.0.1:5801' 
requests = httpx.AsyncClient(verify=False)

def quick_map(**kwargs) -> dict:
    return kwargs