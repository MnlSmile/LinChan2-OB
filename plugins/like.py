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
    if not ev.post_type == 'message' and not ev.message_type == 'group':
        return
    fromgroup = ev.group_id
    match rmsg:
        case '/like':
            for i in range(20):
                await requests.get(NCURL + '/send_like', params=quick_map(user_id=ev.user_id))
                await asyncio.sleep(random.randint(1, 400))
    return

transer.set_receiving_parser(ent)