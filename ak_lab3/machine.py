import logging
import sys
from collections import deque
from enum import StrEnum, auto
from queue import Queue
from typing import Callable, Optional

from ak_lab3.isa import read_code, Instruction, Opcode


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
    def __init__(
        self,
        alu: ALU,
        data_memory_size: int,
        stack_size: int,
        program: list[Instruction],
        mmio: dict[int, IO],
        start: int,
    ):
        self.memory_size = data_memory_size
        self.memory = program + [0] * (data_memory_size - len(program))
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

    def signal_read_memory(self) -> dict | int:
        if self.ar in self.mmio:
            return self.mmio[self.ar].read_byte()
        return self.memory[self.ar]

    def signal_write_memory(self, value: int):
        if self.ar in self.mmio:
            self.mmio[self.ar].write_byte(value)
        self.memory[self.ar] = value

    def signal_latch_ar(self, value: int):
        self.ar = value

    def perform_alu_operation(
        self, alu_operation: AluOperation, left: AluInputMux, right: AluInputMux
    ) -> int:
        left_input = 0 if left == AluInputMux.ZERO else self._get_first()
        right_input = 0 if right == AluInputMux.ZERO else self._get_second()
        return self.alu.perform(left_input, right_input, alu_operation)

    def _get_first(self):
        return self.stack[-1]

    def _get_second(self):
        return self.stack[-2]


class ControlUnit:
    _tick: int

    def __init__(self, data_path: DataPath):
        self.data_path = data_path
        self._tick = 0
        self.executors: dict[str, Callable[[dict], None]] = {
            Opcode.PUSH: self.execute_push
        }


    def tick(self):
        self._tick += 1

    def current_tick(self) -> int:
        return self._tick

    def decode_and_execute_instruction(self):
        instruction = self.data_path.signal_read_memory()
        assert isinstance(instruction, dict), "FAULT: Executing data!"
        self.tick()
        self.data_path.signal_latch_ar(self.data_path.ar + 1)
        self.tick()
        opcode: str = instruction["opcode"]
        self.executors[Opcode[opcode]](instruction)

    def execute_push(self, instruction: dict):

        print("Pushed!")







STACK_SIZE = 254
MEMORY_SIZE = 1024


def simulation(code: dict, input_tokens, data_memory_size, stack_size, limit) -> tuple[str, int, int]:
    alu = ALU()
    io = IO(input_tokens)
    ios = {801: io}
    data_path = DataPath(alu, data_memory_size, stack_size, code["code"], ios, code["start"])
    control_unit = ControlUnit(data_path)
    instr_counter = 0
    logging.debug("%s", control_unit)
    try:
        while instr_counter < limit:
            control_unit.decode_and_execute_instruction()
            instr_counter += 1
            logging.debug("%s", control_unit)
    except EOFError:
        logging.warning("Input buffer is empty!")
    except StopIteration:
        pass

    if instr_counter >= limit:
        logging.warning("Limit exceeded!")
    logging.info("output buffer: %s", io.output)
    return io.output, instr_counter, control_unit.current_tick()


def main(code_file: str, input_file: str):
    code = read_code(code_file)
    with open(input_file, encoding="utf-8") as file:
        input_text = file.read()
        input_token = []
        for char in input_text:
            input_token.append(char)
    output, instr_counter, ticks = simulation(
        code, input_token, data_memory_size=100, stack_size=100, limit=1000
    )
    print("".join(output))
    print("instr_counter: ", instr_counter, "ticks:", ticks)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    assert len(sys.argv) == 3, "Wrong arguments: machine.py <code_file> <input_file>"
    _, code_file, input_file = sys.argv
    main(code_file, input_file)
