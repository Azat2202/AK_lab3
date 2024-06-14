import json
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional


class Opcode(str, Enum):
    DUP = "dup"
    OVER = "over"
    POP = "pop"
    SWAP = "swap"
    LOAD = "load"
    SAVE = "save"
    INC = "inc"
    DEC = "dec"
    ADD = "add"
    SUB = "sub"
    DIV = "div"
    XOR = "xor"
    MUL = "mul"
    JUMP = "jump"
    JZ = "jz"
    PUSH = "push"
    WORD = "word"
    HALT = "halt"

    def __str__(self):
        return self.value

@dataclass
class Instruction:
    opcode: Opcode
    arg: Optional[int | str] = None

    def to_dict(self):
        # exclude None fields
        data = asdict(self)
        return {key: value for key, value in data.items() if value is not None}


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Instruction):
            return o.to_dict()
        if isinstance(o, Enum):
            return o.value
        return json.JSONEncoder.default(self, o)


def write_code(filename: str, code: dict) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        file.write(json.dumps(code, cls=CustomEncoder, indent=2))


def read_code(filename: str) -> dict[str, str]:
    return json.load(open(filename, encoding="utf-8"))
