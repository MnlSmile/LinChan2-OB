from stdserver import *

import MCLikeCommandParser

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
    async def like() -> None:
        for i in range(20):
            await requests.get(NCURL + '/send_like', params=quick_map(user_id=ev.qq_id))
            await asyncio.sleep(random.randint(1, 400) * 0.001)
    async def like_int(qqid:int) -> None:
        for i in range(20):
            await requests.get(NCURL + '/send_like', params=quick_map(user_id=qqid))
            await asyncio.sleep(random.randint(1, 400) * 0.001)
    try:
        async with MCLikeCommandParser.Parser(rmsg) as cmd:
            cmd.resolve_overload_and_bind(
                {
                    ('like'): like,
                    ('like', int): like_int
                }
            )
    except ValueError:
        pass
    return

transer.set_receiving_parser(ent)