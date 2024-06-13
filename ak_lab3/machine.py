from collections import deque
from enum import StrEnum, auto
from queue import Queue


class AluOperation(StrEnum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    XOR = auto()
    NOT = auto()
    INC = auto()
    DEC = auto()

class AluInputMux(StrEnum):
    ZERO = auto()
    TOS = auto()

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


class IO:
    def __init__(self, input_buffer: list[int]):
        self.output = ""
        self.input_buffer = deque(input_buffer)

    def write_byte(self, b: int):
        self.output += chr(b)

    def read_byte(self) -> int:
        if len(self.input_buffer) == 0:
            raise EOFError("Input is over")
        return self.input_buffer.pop()

    def __repr__(self) -> str:
        return f"{map(chr, self.input_buffer)}, {self.output}"



class DataPath:
    def __init__(self, alu: ALU, data_memory_size: int, stack_size: int, input_buffer: list[int], mmio: dict[int, IO], start: int):
        self.input_buffer = input_buffer
        self.memory_size = data_memory_size
        self.memory = [0] * data_memory_size
        self.stack_size = stack_size
        self.stack = [0] * stack_size
        self.mmio = mmio
        self.alu = alu
        self.ar = start

    def signal_stack_pop(self):
        self.stack.pop()

    def signal_push(self, value: int):
        self.stack.append(value)

    def signal_write_second(self, value: int):
        self.stack[-2] = value

    def signal_read_memory(self) -> int:
        if self.ar in self.mmio:
            return self.mmio[self.ar].read_byte()
        return self.memory[self.ar]

    def signal_write_memory(self, value: int):
        if self.ar in self.mmio:
            self.mmio[self.ar].write_byte(value)
        self.memory[self.ar] = value

    def latch_ar(self, value: int):
        self.ar = value

    def perform_alu_operation(self, alu_operation: AluOperation, left: AluInputMux, right: AluInputMux) -> int:
        left_input = 0 if left == AluInputMux.ZERO else self._get_first()
        right_input = 0 if right == AluInputMux.ZERO else self._get_second()
        return self.alu.perform(left_input, right_input, alu_operation)

    def _get_first(self):
        return self.stack[-1]

    def _get_second(self):
        return self.stack[-2]



