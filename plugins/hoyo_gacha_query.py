from stdserver import *

transer = register(__name__)

async def ent(a0:'Message') -> None:
    return await parse_ent(a0.fetch_one())

async def parse_ent(ev:BotPostEvent) -> None:
    ev = ev[0]
    if ev.post_type == 'message':
        await bussiness(ev)
    return 

def format_gacha_pool_message(pool:dict) -> str:
    result = f"{pool['version']} 祈愿活动\n"
    if pool['phase_1']['exist']:
        result += '    上半\n' + ' ' * 8
        result += ('\n' + ' ' * 8).join(pool['phase_1']['5_stars'] + pool['phase_1']['4_stars'])
        result += '\n'
    elif pool['phase_2']['exist']:
        result += '    下半\n' + ' ' * 8
        result += ('\n' + ' ' * 8).join(pool['phase_2']['5_stars'] + pool['phase_2']['4_stars'])
        result += '\n'
    elif pool['phase_unknown']['exist']:
        result += '    不详\n' + ' ' * 8
        result += ('\n' + ' ' * 8).join(pool['phase_unknown']['5_stars'] + pool['phase_unknown']['4_stars'])
        result += '\n'
    elif pool['chronicled']['exist']:
        result += '    集录\n' + ' ' * 8
        result += ('\n' + ' ' * 8).join(pool['chronicled']['5_stars'] + pool['chronicled']['4_stars'])
        result += '\n'
    result += '结果准确性把握 99%'
    return result

async def bussiness(ev:BotPostEvent) -> None:
    rmsg = ev.raw_message
    if not ev.post_type == 'message' and not ev.message_type == 'group':
        return
    fromgroup = ev.group_id
    match rmsg:
        case '/gacha query genshin':
            pool = await get_latest_genshin_gacha_pool()
            reply = format_gacha_pool_message(pool)
            await quick_send_group(reply, fromgroup)
        case '原神卡池':
            pool = await get_latest_genshin_gacha_pool()
            reply = format_gacha_pool_message(pool)
            await quick_send_group(reply, fromgroup)
        case '/gacha query starrail':
            pool = await get_latest_hsr_gacha_pool()
            reply = format_gacha_pool_message(pool)
            await quick_send_group(reply, fromgroup)
        case '崩坏星穹铁道卡池':
            pool = await get_latest_hsr_gacha_pool()
            reply = format_gacha_pool_message(pool)
            await quick_send_group(reply, fromgroup)
        case '/git pull':
            def _thread():
                os.system('git pull')
            threading.Thread(target=_thread).start()
    return

async def get_latest_genshin_gacha_pool() -> dict:
    resp = await requests.get('https://homdgcat.wiki/gi/banner.js')
    total_pool = json.loads(resp.text[34:resp.text.index('\nvar _icons = ')])
    _locals = json.loads(resp.text[resp.text.index('var _index = ') + len('var _index = '):])
    of_latest_known_version = total_pool[0]
    version = of_latest_known_version['V']
    o_pools = of_latest_known_version['P']

    result = {
        'version': version,
        'phase_1': {
            'exist': False,
            '5_stars': [],
            '4_stars': []
        },
        'phase_2': {
            'exist': False,
            '5_stars': [],
            '4_stars': []
        },
        'phase_unknown': {
            'exist': False,
            '5_stars': [],
            '4_stars': []
        },
        'chronicled': {
            'exist': False,
            '5_stars': [],
            '4_stars': []
        }
    }

    for pool in o_pools:
        _id = pool['_id']
        S_chars = pool['A']
        A_chars = pool['B']
        match _id:
            case 0:
                # 不知道哪半
                this_phase = result['phase_unknown']
                this_phase['exist'] = True  
                for char in S_chars:
                    en_name = char['N']
                    ch_name = 'unknown'
                    for k, v in  _locals.items():
                        if v == en_name:
                            ch_name = k
                            break
                    this_phase['5_stars'] += [ch_name]
                for char in A_chars:
                    en_name = char['N']
                    ch_name = 'unknown'
                    for k, v in  _locals.items():
                        if v == en_name:
                            ch_name = k
                            break
                    this_phase['4_stars'] += [ch_name]
            case 1:
                # 上半
                this_phase = result['phase_1']
                this_phase['exist'] = True  
                for char in S_chars:
                    en_name = char['N']
                    ch_name = 'unknown'
                    for k, v in  _locals.items():
                        if v == en_name:
                            ch_name = k
                            break
                    this_phase['5_stars'] += [ch_name]
                for char in A_chars:
                    en_name = char['N']
                    ch_name = 'unknown'
                    for k, v in  _locals.items():
                        if v == en_name:
                            ch_name = k
                            break
                    this_phase['4_stars'] += [ch_name]
            case 2:
                # 下半
                this_phase = result['phase_2']
                this_phase['exist'] = True  
                for char in S_chars:
                    en_name = char['N']
                    ch_name = 'unknown'
                    for k, v in  _locals.items():
                        if v == en_name:
                            ch_name = k
                            break
                    this_phase['5_stars'] += [ch_name]
                for char in A_chars:
                    en_name = char['N']
                    ch_name = 'unknown'
                    for k, v in  _locals.items():
                        if v == en_name:
                            ch_name = k
                            break
                    this_phase['4_stars'] += [ch_name]
            case 4:
                # 集录
                this_phase = result['chronicled']
                this_phase['exist'] = True  
                for char in S_chars:
                    en_name = char['N']
                    ch_name = 'unknown'
                    for k, v in  _locals.items():
                        if v == en_name:
                            ch_name = k
                            break
                    this_phase['5_stars'] += [ch_name]
                for char in A_chars:
                    en_name = char['N']
                    ch_name = 'unknown'
                    for k, v in  _locals.items():
                        if v == en_name:
                            ch_name = k
                            break
                    this_phase['4_stars'] += [ch_name]
    return result

async def get_latest_hsr_gacha_pool() -> dict:
    resp = await requests.get('https://homdgcat.wiki/data/banner.js')
    total_pool = json.loads(resp.text[34:resp.text.index('\nvar _index = ')])
    _locals = json.loads(resp.text[resp.text.index('var _index = ') + len('var _index = '):])
    of_latest_known_version = total_pool[0]
    version = of_latest_known_version['V']
    o_pools = of_latest_known_version['P']

    result = {
        'version': version,
        'phase_1': {
            'exist': False,
            '5_stars': [],
            '4_stars': []
        },
        'phase_2': {
            'exist': False,
            '5_stars': [],
            '4_stars': []
        },
        'phase_unknown': {
            'exist': False,
            '5_stars': [],
            '4_stars': []
        },
        'chronicled': {
            'exist': False,
            '5_stars': [],
            '4_stars': []
        }
    }

    for pool in o_pools:
        _id = pool['I']
        S_chars = pool['A']
        A_chars = pool['B']
        match _id:
            case 0:
                # 不知道哪半
                this_phase = result['phase_unknown']
                this_phase['exist'] = True  
                for char in S_chars:
                    en_name = char['N']
                    ch_name = 'unknown'
                    for k, v in  _locals.items():
                        if v == en_name:
                            ch_name = k
                            break
                    this_phase['5_stars'] += [ch_name]
                for char in A_chars:
                    en_name = char['N']
                    ch_name = 'unknown'
                    for k, v in  _locals.items():
                        if v == en_name:
                            ch_name = k
                            break
                    this_phase['4_stars'] += [ch_name]
            case 1:
                # 上半
                this_phase = result['phase_1']
                this_phase['exist'] = True  
                for char in S_chars:
                    en_name = char['N']
                    ch_name = 'unknown'
                    for k, v in  _locals.items():
                        if v == en_name:
                            ch_name = k
                            break
                    this_phase['5_stars'] += [ch_name]
                for char in A_chars:
                    en_name = char['N']
                    ch_name = 'unknown'
                    for k, v in  _locals.items():
                        if v == en_name:
                            ch_name = k
                            break
                    this_phase['4_stars'] += [ch_name]
            case 2:
                # 下半
                this_phase = result['phase_2']
                this_phase['exist'] = True  
                for char in S_chars:
                    en_name = char['N']
                    ch_name = 'unknown'
                    for k, v in  _locals.items():
                        if v == en_name:
                            ch_name = k
                            break
                    this_phase['5_stars'] += [ch_name]
                for char in A_chars:
                    en_name = char['N']
                    ch_name = 'unknown'
                    for k, v in  _locals.items():
                        if v == en_name:
                            ch_name = k
                            break
                    this_phase['4_stars'] += [ch_name]
            case 4:
                # 集录
                this_phase = result['chronicled']
                this_phase['exist'] = True  
                for char in S_chars:
                    en_name = char['N']
                    ch_name = 'unknown'
                    for k, v in  _locals.items():
                        if v == en_name:
                            ch_name = k
                            break
                    this_phase['5_stars'] += [ch_name]
                for char in A_chars:
                    en_name = char['N']
                    ch_name = 'unknown'
                    for k, v in  _locals.items():
                        if v == en_name:
                            ch_name = k
                            break
                    this_phase['4_stars'] += [ch_name]
    return result

transer.set_receiving_parser(ent)