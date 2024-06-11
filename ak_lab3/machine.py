from enum import StrEnum, auto


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

    def __init__(self):
        self._z_flag = False

    def perform(self, left: int, right: int, operation: AluOperation) -> int:
        output_value: int
        match operation:
            case AluOperation.ADD:
                output_value = left + right
            case AluOperation.SUB:
                output_value = left - right
            case AluOperation.MUL:
                output_value = left * right
            case AluOperation.DIV:
                output_value = left // right
            case AluOperation.XOR:
                output_value = left ^ right
            case AluOperation.NOT:
                output_value = not left
            case AluOperation.INC:
                output_value = left + 1
            case AluOperation.DEC:
                output_value = left - 1
            case _:
                raise NotImplementedError()
        self._z_flag = output_value == 0
        return output_value

    @property
    def z_flag(self) -> bool:
        return self.z_flag
