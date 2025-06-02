import ast

from typing import Callable, Any

def resolve_string(s:str) -> object:
    try:
        result = ast.literal_eval(s)
    except Exception:
        result = s
    return result

def get_type_from_string(s:str) -> type:
    return type(resolve_string(s))

class ConstStr(str): ...

class Parser:
    def __init__(self, s:str, compile:bool=True) -> None:
        self.raw = s
        self.compile() if compile else None
        def raiseerr(*args) -> None:
            raise ValueError(f'Unsigned command: {self.raw}')
        self.func = raiseerr
    def compile(self) -> None:
        self.raw_arr = self.raw.split()
        self.type_arr = [get_type_from_string(c) for c in self.raw_arr]
        self.data_arr = [resolve_string(c) for c in self.raw_arr]
        self.clauses = self.data_arr[1:]
        self.clause_types = self.type_arr[1:]
        self.command = self.data_arr[0][1:] if self.data_arr[0][0] in './\\' else self.data_arr[0]
    def resolve_overload_and_bind(self, overload_binds:dict[tuple[str, type|str]:Callable]) -> Callable|None:
        def is_matched(overload_preset_type:type|str|ConstStr, clause: Any) -> bool:
            if isinstance(overload_preset_type, ConstStr) and isinstance(clause, str):
                return clause == overload_preset_type  # 这时候后者不是个类型
            elif isinstance(clause, overload_preset_type):
                return True
            return False
        for overload, func in overload_binds.items():
            if overload[0].startswith('/'):
                overload = tuple([overload[0][1:]] + list(overload[1:]))  # 注册信息如果有杠就去杠
            if self.command != overload[0]:
                continue
            overload = overload[1:]  # 命令比较已通过, 接下来只需要比较从句
            if len(overload) != len(self.clauses):
                continue
            matching:int = 0
            for i in range(len(overload)):
                matching += is_matched(overload[i], self.clauses[i])
            if matching == len(overload):
                self.func = func
                return func
        return None  
    def execute(self) -> Any:
        return self.func(*self.clauses)
    async def aexecute(self) -> Any:
        return await self.func(*self.clauses)
    def __enter__(self) -> 'Parser':
        self.compile()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        # 只负责自动执行, 不处理异常
        if exc_type:
            return False
        self.execute()
        return True
    async def __aenter__(self) -> 'Parser':
        self.compile()
        return self
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        # 只负责自动执行, 不处理异常
        if exc_type:
            return False
        await self.aexecute()
        return True

if __name__ == '__main__':
    _d = {
        ('/aaa', int, int, int): lambda *x: print(0, *x),
        ('a', ConstStr('aaa'), int, int): print
    }
    a = Parser(input())
    a.compile()
    print(a.clauses)
    if a.resolve_overload_and_bind(_d):
        a.execute()
    with Parser('/aaa 1 1 1') as cmd:
        cmd.resolve_overload_and_bind(_d)