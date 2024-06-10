import json
from dataclasses import dataclass
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


class ArgType(str, Enum):
    IMPL = "implicit"
    ADDR = "address"


@dataclass
class Instruction:
    opcode: Opcode
    arg: Optional[int | str] = None
    arg_type: Optional[ArgType] = None


def write_code(filename: str, code: list[Opcode]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        buf = []
        for instr in code:
            buf.append(json.dumps(instr))
        file.write("[" + ",\n ".join(buf) + "]")


def read_code(filename: str) -> dict[str, str]:
    raise NotImplementedError()
