from stdserver import *

async def quick_send_private(msg:str, target:int|tuple[int]) -> dict:
    _d = quick_map(
        user_id = target,
        message = msg,
    )
    resp = await requests.post(NCURL + '/send_msg', json=_d)
    return resp

async def quick_send_group(msg:str, target:int|tuple[int], at:bool=False) -> dict:
    msg = f"[CQ:at,qq={target}] " if at else '' + msg
    _d = quick_map(
        group_id = target,
        message = msg,
    )
    resp = await requests.post(NCURL + '/send_msg', json=_d)
    return resp