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
    async def echo(_s:str) -> None:
        await quick_send_group(_s, target=fromgroup)
    try:
        async with MCLikeCommandParser.Parser(rmsg) as cmd:
            cmd.resolve_overload_and_bind(
                {
                    ('echo', str): echo
                }
            )
    except ValueError:
        pass
    return

transer.set_receiving_parser(ent)