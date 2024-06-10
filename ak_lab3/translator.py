import sys
from typing import AnyStr

from ak_lab3.isa import Instruction, Opcode


def remove_comment(line: str) -> str:
    return line.split(";", 1)[0].strip()


def parse_opcode(code: str) -> Opcode:
    return Opcode[code]


def parse_word_data(data: str) -> list[Instruction]:
    if data.startswith("0x"):
        return [Instruction(Opcode.WORD, data[2:])]
    return [Instruction(Opcode.WORD, ord(ch)) for ch in data.strip('"')]


def preprocess(input_data: AnyStr):
    """Remove comments, replace tabs with spaces, only one space"""
    return "\n".join(
        [
            " ".join(remove_comment(str(line_raw)).replace("\t", " ").split())
            for line_raw in input_data.splitlines()
        ]
    )


def translate_stage_1(input_data: str) -> tuple[list[Instruction], dict[str, int]]:
    """Remove all commits and split into terms, without links"""
    code: list[Instruction] = []
    labels: dict[str, int] = {}
    for line_raw in input_data.splitlines():
        line = remove_comment(str(line_raw))
        if line[-1] == ":":
            assert line.count(" ") == 0, "Label and text must be on different lines"
            labels.update({line: len(code) - 1})
        elif line.count(" ") == 0:
            code.append(Instruction(parse_opcode(line), arg=None))
        elif line.startswith("PUSH"):
            op, label_name = line.split(" ", 2)
            code.append(Instruction(parse_opcode(op), label_name))
        elif line.startswith("WORD"):
            _, data = line.split(" ", 1)
            code += parse_word_data(data)
    return code, labels


def translate(input_data: AnyStr):
    input_str = preprocess(input_data)
    code, labels = translate_stage_1(input_str)

    print(*code, sep="\n")
    print(labels)


def main():
    assert (
        len(sys.argv) == 3
    ), "Wrong arguments: translator.py <input_file> <output_file>"
    _, source, _ = sys.argv
    with open(source, "r", encoding="utf-8") as file:
        input_data = file.read()

    translate(input_data)
    # print(code)


if __name__ == "__main__":
    main()
