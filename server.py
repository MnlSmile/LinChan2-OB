import fastapi
import sys

import plugins
from broadcasting import Transceiver, Message, register
from stdserver import *

from colorama import Fore, init
init(autoreset=True)
def colored_print(s, color:str='RESET') -> None:
    print(getattr(Fore, color) + str(s) + '\n')

transer = register(__name__)

app = fastapi.FastAPI()

plugins.load_plugins()

class BotPostEvent(BaseModel):
    time:int
    post_type:str
    self_id:int
    class Config:
        extra = "allow"

@app.post('/LinChan2API')
async def parse_post_message(event:BotPostEvent) -> JSONResponse:
    transer << event
    return 200

def handle_global_exception(exc_type, exc_value, exc_traceback):
    print(exc_traceback)

sys.excepthook = handle_global_exception