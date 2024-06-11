from enum import StrEnum, auto

from ak_lab3.isa import Opcode


class AluOperation(StrEnum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    XOR = auto()
    NOT = auto()
    INC = auto()
    DEC = auto()


class ALU:
    z_flag = None

    def __init__(self):
        self.z_flag = False

    def perform(self, left: int, right: int, operation: AluOperation) -> int:
        match operation:
            case AluOperation.ADD:
                return left + right
            case AluOperation.SUB:
                return left - right
            case AluOperation.MUL:
                return left * right
            case AluOperation.DIV:
                return left // right
            case AluOperation.XOR:
                return left ^ right
            case AluOperation.NOT:
                return not left
            case AluOperation.INC:
                return left + 1
            case AluOperation.DEC:
                return left - 1
            case _:
                raise NotImplementedError()
