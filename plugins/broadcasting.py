"""
Usage:
>>>  from broadcasting import Transceiver, Message, register
>>> import types
>>>
>>> transer = register(__name__)
>>>
>>> async def parse(self, a0:'Message') -> None:
>>>     print('hello World')
>>>     return
>>>
>>> transer.on_message_received = types.MethodType(parse, transer)
"""

import asyncio

import typing
from typing import Any

class BroadcastingInsiderMessage:
    def __init__(self, sender, *contents) -> None:
        self._sender = sender
        self._contents = contents
    def contents(self) -> list[Any]:
        return self._contents
    def sender(self) -> 'Transceiver':
        return self._sender
    def fetch_one(self) -> Any:
        return self._contents[0]

class ReceivingMessage(BroadcastingInsiderMessage): pass

# 别名
class InnerMsg(BroadcastingInsiderMessage): pass

class SkipError(Exception):
    pass

class Transceiver:
    _instances:'list[Transceiver]' = []
    #@staticmethod
    async def send_to(self, target:'Transceiver', a0:BroadcastingInsiderMessage) -> None:
        await target._receive(a0)
    def __init__(self, _main_:str) -> None:
        self._source = _main_
        self._on_message_received = lambda a0: None
        Transceiver._instances += [self]
        return
    def __del__(self) -> None:
        Transceiver._instances.remove(self)
    def source(self) -> str:
        return self._source
    def set_receiving_parser(self, func) -> None:
        self._on_message_received = func
    async def _receive(self, a0:ReceivingMessage) -> None:
        await self._on_message_received(a0)
        return 
    async def broadcast(self, *contents) -> None:
        return await self.shout(*contents)
    async def shout(self, *contents) -> None:
        l = len(contents)
        for target in Transceiver._instances[:]:
            if target is self or target == self or target.source() == __name__:
                #print('skipped self')
                continue
            else:
                await self.send_to(target, BroadcastingInsiderMessage(self, *contents))
        rcotentsstr = str(contents)
        if len(rcotentsstr) <= 32:
            print(contents, '->', f"{len(Transceiver._instances)} transceivers")
        else:
            print('...', '->', f"{len(Transceiver._instances)} transceivers")
        #print(*contents)
    def prepare_message(self, contents:list[Any]=[]) -> 'Message':
        return Message(self, contents)
    # 别名
    def message(self, contents:list[Any]=[]) -> 'Message':
        return self.prepare_message(contents)
    def msg(self, contents:list[Any]=[]) -> 'Message':
        return self.prepare_message(contents)
    
    # 运算符重载块
    # <<
    def __lshift__(self, p2: 'typing.Union[str, dict, Message, Any]') -> None:
        with self.msg() as msg:
            msg << p2
        return 
    
    # 类型转换重载块
    def __repr__(self) -> str:
        return f"Transceiver('{self._source}')"

class SendingMessage:
    def __init__(self, transer:Transceiver=None, contents:list[Any]=[]):
        self._is_in_contents_manager = False
        self._transer = transer
        self._contents = contents[:]  # 防共享
        self._dictdata = None
        return
    def set_contentss(self, contents:Any) -> None:
        self._contents = contents
        return
    def contents(self) -> Any:
        return self._contents
    def append(self, content:Any) -> None:
        self._contents += [content]
        return
    def fetch_one(self) -> Any:
        return self._contents[0]
    # 操作符重载块
    # +
    def __add__(self, p2: 'typing.Union[Message, Any]') -> 'Message':
        T = type(p2)
        if T == Message:
            self._contents += p2._contents
        else:
            self._contents += [p2]
        return self
    # +=
    def __iadd__(self, p2: 'typing.Union[Message, Any]') -> None:
        T = type(p2)
        if T == Message:
            self._contents += p2._contents
        else:
            self._contents += [p2]
        return 
    # <<
    def __lshift__(self, p2: 'typing.Union[Message, Any]') -> 'Message':
        T = type(p2)
        if T == Message:
            self._contents += p2._contents
        else:
            self._contents += [p2]
        return self
    # >>
    def __rshift__(self, p2:Transceiver) -> None:
        asyncio.create_task(p2.shout(*self._contents))
        if self._is_in_contents_manager:
            raise SkipError('Positively shouted')
    
    # 类型转换重载
    def __repr__(self) -> str:
        return f"Message(transceiver={self._transer}, content='{self._contents}')"
    def __str__(self) -> str:
        return str(self._contents)
    def __enter__(self) -> None:
        self._is_in_contents_manager = True
        if not self._transer:
            raise TypeError('Missing transceiver')
        return self
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            return True
        asyncio.create_task(self._transer.shout(self._contents))
        return False
    async def __aenter__(self) -> None:
        self._is_in_contents_manager = True
        if not self._transer:
            raise TypeError('Missing transceiver')
        return self
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            return True
        await self._transer.shout(self._contents)
        return False

# 别名
class Message(SendingMessage): pass

def register(_name_:str) -> Transceiver:
    for inst in Transceiver._instances:
        if inst.source() == _name_:
            return inst
    return Transceiver(_name_)
'''
async def main():
    transer = register(__name__)

    msg = transer.msg()
    msg << 'bbbbb'
    msg >> transer
    with transer.msg() as msg:
        msg:Message
        msg << {'a': 1}
        print(msg.content())
        msg >> transer

if __name__ == '__main__':
    asyncio.run(main())'''