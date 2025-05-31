from io import TextIOWrapper

def refer(*args, **kw) -> TextIOWrapper:
    """
    refer a file in temp dir instead of simply open().
    """
    _args = ('./plugins/temp/' + args[0],) + args[1:]
    return open(*_args, **kw)
