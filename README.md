# Лабораторная работа №3 по Архитектуре Компьютера
- Сиразетдинов Азат Ниязович, P3216
- ```asm | stack | neum | hw | tick -> instr | struct | trap -> stream | mem | cstr | prob1 | spi```
- Упрощенный вариант

## Язык программирования
``` ebnf
program ::= { line }

line ::= label [ comment ] "\n"
       | instr [ comment ] "\n"
       | [ comment ] "\n"

label ::= label_name ":"

instr ::= op0 
        | op1 data
        | op2 label_name

op0 ::= "DUP" 
      | "OVER"
      | "POP"
      | "SWAP"
      | "LOAD"
      | "SAVE"
      | "INC"
      | "DEC"
      | "ADD"
      | "SUB"
      | "DIV"
      | "MUL"

op1 ::= "PUSH"
      | "WORD"

op2 ::= "JZ" | "JUMP"

label_name ::= <any of "a-z A-Z _"> { <any of "a-z A-Z 0-9 _"> }

comment ::= ";" <any symbols except "\n">

data ::= string | number | label_name

string ::= "\"" <any symbols except "\n"> "\""

number ::= 0x <any of "0-9 ABCDEF">
```


