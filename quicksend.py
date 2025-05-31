from stdserver import *

def quick_map(**kwargs) -> dict:
    return kwargs

async def quick_send_private(msg:str, target:int|tuple[int]) -> dict:
    _d = quick_map(
        user_id = target,
        message = msg,
    )
    resp = await requests.post(NCURL + '/send_msg', json=_d)
    return resp

async def quick_send_group(msg:str, target:int|tuple[int], at:int=0) -> dict:
    msg = f"[CQ:at,qq={at}] " if at else '' + msg
    _d = quick_map(
        group_id = target,
        message = msg,
    )
    resp = await requests.post(NCURL + '/send_msg', json=_d)
    return resp