from stdserver import *

transer = register(__name__)

async def ent(a0:'Message') -> None:
    return await parse_ent(a0.fetch_one())

async def parse_ent(ev:BotPostEvent) -> None:
    ev = ev[0]
    if ev.post_type == 'message':
        await bussiness(ev)
    return 

async def bussiness(ev:BotPostEvent) -> None:
    rmsg = ev.raw_message
    fromqq = ev.user_id
    match rmsg:
        case 'aaaa':
            await quick_send_group()
    return

transer.set_receiving_parser(ent)