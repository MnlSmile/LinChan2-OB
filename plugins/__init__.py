"""
"""

import traceback
import os
import importlib

def scan() -> list[str]:
    """
    扫描所有插件并返回插件路径组成的列表.
    插件以 plugins 包的子库或子包的形式存在.
    """
    fl = os.listdir('./plugins')
    if fl != []:
        for fn in ['doc.md', '.git', '.gitignore', '.vscode', 'plugintools.py', 'README.md', '__pycache__', '__init__.py', 'temp', 'disabled']:
            if fn in fl: fl.remove(fn)
        plugin_pymodule_names = []
        try:
            for p in fl:
                try:
                    plugin_pymodule_names.append(f"plugins.{p.split('.')[0]}")
                except Exception:
                    pass
        except Exception:
            pass
        return plugin_pymodule_names
    else:
        return []

def load_plugins() -> list:
    """
    加载所有插件.
    插件以 plugins 包的子库或子包的形式存在.
    """
    pl = scan()
    plugin_pymodules = []
    for p in pl:
        try:
            plugin_pymodules.append(importlib.import_module(p))
        except Exception as e:
            print(f"Aquaplugin {p} failed to load({e}).")
    return plugin_pymodules

async def a_load_plugins() -> list:
    """
    async
    加载所有插件.
    插件以 plugins 包的子库或子包的形式存在.
    """
    pl = scan()
    plugin_pymodules = []
    for p in pl:
        try:
            _module = importlib.import_module(p)
            plugin_pymodules.append(_module)
        except Exception as e:
            print(f"Aquaplugin {p} failed to load({e}).")
    return plugin_pymodules

plugin_modules = load_plugins()

def reg_all() -> None:
    """
    注册所有插件.
    插件以 plugins 包的子库或子包的形式存在.
    """
    for p in plugin_modules:
        try:
            p.reg()
        except Exception:
            print(f"插件 {p.__name__} 注册失败, 因为:")
            traceback.print_exc()
            print('\n')

async def a_reg_all() -> None:
    """
    async
    注册所有插件.
    插件以 plugins 包的子库或子包的形式存在.
    """
    for p in plugin_modules:
        try:
            ...
        except Exception:
            print(f"插件 {p.__name__} 注册失败, 因为:")
            traceback.print_exc()
            print('\n')

if __name__ == '__main__':
    print(scan())