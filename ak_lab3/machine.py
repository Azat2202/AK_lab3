import logging
import sys
from collections import deque
from enum import StrEnum, auto
from typing import Callable, Union

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

DATA_MEMORY_SIZE = 100
STACK_SIZE = 100


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
        return self._z_flag


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
    pc: int = 0
    ar: int = 0

    def __init__(
        self,
        alu: ALU,
        program: list[Instruction],
        mmio: dict[int, IO]
    ):
        self.memory = program + [0] * (DATA_MEMORY_SIZE - len(program))
        self.stack: list[int] = []
        self.mmio = mmio
        self.alu = alu

    def signal_pop(self):
        self.stack.pop()

    def signal_push(self, value: int):
        assert len(self.stack) <= STACK_SIZE, "Stack overflow"
        self.stack.append(value)

    def signal_write_second(self, value: int):
        self.stack[-2] = value

    def signal_write_first(self, value: int):
        self.stack[-1] = value

    def signal_read_memory(self) -> Instruction | int:
        if self.ar in self.mmio:
            return self.mmio[self.ar].read_byte()
        if self.memory[self.ar].opcode == Opcode.WORD:
            return self.memory[self.ar].arg
        return self.memory[self.ar]

    def signal_write_memory(self, value: int):
        if self.ar in self.mmio:
            self.mmio[self.ar].write_byte(value)
        self.memory[self.ar] = value

    def signal_latch_ar(self, value: int):
        self.ar = value

    def signal_latch_pc(self, value: int):
        self.pc = value

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

    def tick(self):
        self._tick += 1

    def current_tick(self) -> int:
        return self._tick

    def decode_and_execute_instruction(self):
        self.data_path.signal_latch_ar(self.data_path.pc)
        self.tick()
        instruction = self.data_path.signal_read_memory()
        assert isinstance(instruction, Instruction), "FAULT: Executing data!"
        self.tick()
        self.data_path.signal_latch_pc(self.data_path.pc + 1)
        self.tick()
        if instruction.opcode == Opcode.DUP:
            self.execute_dup()
        elif instruction.opcode == Opcode.OVER:
            self.execute_over()
        elif instruction.opcode == Opcode.POP:
            self.execute_pop()
        elif instruction.opcode == Opcode.SWAP:
            self.execute_swap()
        elif instruction.opcode == Opcode.LOAD:
            self.execute_load()
        elif instruction.opcode == Opcode.SAVE:
            self.execute_save()
        elif instruction.opcode in [Opcode.INC, Opcode.DEC]:
            self.execute_single_operand_alu_operation(instruction)
        elif instruction.opcode in [Opcode.ADD, Opcode.SUB, Opcode.DIV, Opcode.XOR, Opcode.MUL]:
            self.execute_double_operand_alu_operation(instruction)
        elif instruction.opcode == Opcode.JUMP:
            self.execute_jump()
        elif instruction.opcode == Opcode.JZ:
            self.execute_jz()
        elif instruction.opcode == Opcode.PUSH:
            self.execute_push(instruction)
        elif instruction.opcode == Opcode.HALT:
            self.execute_halt()
        else:
            raise NotImplementedError


    def execute_dup(self):
        self.data_path.signal_push(
            self.data_path.perform_alu_operation(
                AluOperation.ADD, AluInputMux.TOS, AluInputMux.ZERO
            )
        )
        self.tick()

    def execute_over(self):
        self.data_path.signal_push(
            self.data_path.perform_alu_operation(
                AluOperation.ADD, AluInputMux.ZERO, AluInputMux.TOS
            )
        )
        self.tick()

    def execute_pop(self):
        self.data_path.signal_pop()
        self.tick()

    def execute_swap(self):
        self.data_path.signal_write_first(
            self.data_path.perform_alu_operation(
                AluOperation.XOR, AluInputMux.TOS, AluInputMux.TOS
            )
        )
        self.tick()
        self.data_path.signal_write_second(
            self.data_path.perform_alu_operation(
                AluOperation.XOR, AluInputMux.TOS, AluInputMux.TOS
            )
        )
        self.tick()
        self.data_path.signal_write_first(
            self.data_path.perform_alu_operation(
                AluOperation.XOR, AluInputMux.TOS, AluInputMux.TOS
            )
        )
        self.tick()

    def execute_load(self):
        self.data_path.signal_latch_ar(
            self.data_path.perform_alu_operation(
                AluOperation.ADD, AluInputMux.TOS, AluInputMux.ZERO
            )
        )
        self.tick()
        self.data_path.signal_write_first(
            self.data_path.signal_read_memory()
        )
        self.tick()

    def execute_save(self):
        self.data_path.signal_latch_ar(
            self.data_path.perform_alu_operation(
                AluOperation.ADD, AluInputMux.TOS, AluInputMux.ZERO
            )
        )
        self.tick()
        self.data_path.signal_pop()
        self.tick()
        self.data_path.signal_write_memory(
            self.data_path.perform_alu_operation(
                AluOperation.ADD, AluInputMux.TOS, AluInputMux.ZERO
            )
        )
        self.tick()
        self.data_path.signal_pop()
        self.tick()

    def execute_single_operand_alu_operation(self, instruction: Instruction):
        assert instruction.opcode in AluOperation
        self.data_path.signal_write_second(
            self.data_path.perform_alu_operation(
                AluOperation[instruction.opcode], AluInputMux.TOS, AluInputMux.ZERO
            )
        )
        self.tick()
        self.data_path.signal_pop()
        self.tick()

    def execute_double_operand_alu_operation(self, instruction: Instruction):
        assert instruction.opcode in AluOperation
        self.data_path.signal_write_second(
            self.data_path.perform_alu_operation(
                AluOperation[instruction.opcode], AluInputMux.TOS, AluInputMux.TOS
            )
        )
        self.tick()
        self.data_path.signal_pop()
        self.tick()

    def execute_jump(self):
        self.data_path.signal_latch_pc(
            self.data_path.perform_alu_operation(
                AluOperation.ADD, AluInputMux.TOS, AluInputMux.ZERO
            )
        )
        self.tick()
        self.data_path.signal_pop()
        self.tick()

    def execute_jz(self):
        if self.data_path.alu.z_flag:
            self.execute_jump()

    def execute_push(self, instruction: Instruction):
        assert instruction.arg is not None and isinstance(instruction.arg, int)
        self.data_path.signal_push(instruction.arg)
        self.tick()

    def execute_halt(self):
        raise StopIteration

    def __repr__(self):
        state_repr = (f"TICK: {self.current_tick():4} "
                      f"PC: {self.data_path.pc:4} "
                      f"AR: {self.data_path.ar:4} "
                      f"Z_FLAG: {self.data_path.alu.z_flag:1} ")
        stack_repr = f"DATA_STACK: {self.data_path.stack}"
        instr_repr = str(self.data_path.memory[self.data_path.pc])

        return f"{state_repr} \t{stack_repr} \t{instr_repr}"



def simulation(
    code_raw: dict, input_tokens, limit
) -> tuple[str, int, int]:
    alu = ALU()
    io = IO(input_tokens)
    ios = {801: io}
    code = list(map(Instruction.from_dict, code_raw["code"]))
    data_path = DataPath(
        alu, code, ios
    )
    data_path.signal_latch_pc(code_raw["start"])
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


def main(code_filename: str, input_filename: str):
    code = read_code(code_filename)
    with open(input_filename, encoding="utf-8") as file:
        input_text = file.read()
        input_token = []
        for char in input_text:
            input_token.append(char)
    output, instr_counter, ticks = simulation(
        code, input_token, limit=1000
    )
    print("".join(output))
    print("instr_counter: ", instr_counter, "ticks: ", ticks)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    assert len(sys.argv) == 3, "Wrong arguments: machine.py <code_file> <input_file>"
    _, code_file, input_file = sys.argv
    main(code_file, input_file)
