# Лабораторная работа №3 по Архитектуре Компьютера
- Сиразетдинов Азат Ниязович, P3216
- ```asm | stack | neum | hw | tick -> instr | struct | trap -> stream | mem | cstr | prob1 | spi```
- Упрощенный вариант

## Язык программирования
### Синтаксис
``` ebnf
program ::= { line }

line ::= label [ comment ] "\n"
       | instr [ comment ] "\n"
       | [ comment ] "\n"

label ::= label_name ":"

instr ::= op0 
        | op1 variable
        | "WORD" word_data

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
      | "XOR"
      | "JUMP"
      | "JZ"
      | "HALT"

op1 ::= "PUSH"

label_name ::= <any of "a-z A-Z _"> { <any of "a-z A-Z 0-9 _"> }

comment ::= ";" <any symbols except "\n">

word_data ::= variable | string

variable ::= number | label_name

string ::= "\"" <any symbols except "\n"> "\""

number ::= 0x <any of "0-9 ABCDEF">
```

Поддерживаются однострочные комментарии, начинающиеся с ;

  - ```DUP``` - продублировать вершину стека данных ```[a] -> [a, a]```
  - ```OVER``` - дублировать второй элемент на стеке данных через первый ```[a, b] -> [a, b, a]```
  - ```POP``` - удалить значение с вершины стека данных ```[a] -> []```
  - ```SWAP``` - поменять местами два значения на вершине стека данных ```[a, b] -> [b, a]```
  - ```LOAD``` - загрузить из памяти значение по адресу с вершины стека ```[address] -> [value_from_memory]```
  - ```SAVE``` - взять адрес с вершины стека данных и записать в память значение, следующее после вершины стека данных ```[value, address] -> []```
  - ```INC``` - увеличить значения на вершине стека данных на 1 ```[a] -> [a + 1]```
  - ```DEC``` - уменьшить значения на вершине стека данных на 1 ```[a] -> [a - 1]```
  - ```ADD``` - сумма двух значений на вершине стека данных ```[a, b] -> [b + a]```
  - ```SUB``` - разность двух значений на вершине стека данных (первое вычитается из второго) ```[a, b] -> [a - b]```
  - ```DIV``` - целочисленное деление двух значений на вершине стека данных (второе делится на первое) ```[a, b] -> [a // b]```
  - ```XOR``` - побитовая операция исключающего ИЛИ ```[a, b] -> [a ^ b]```
  - ```MUL``` - произведение двух значений на вершине стека данных ```[a, b] -> [b * a]```
  - ```JUMP``` - безусловный переход на адрес с вершины стека ```[a] -> []```
  - ```JZ``` - переход на адрес с вершины стека, если второй элемент равен 0 ```[a, b] -> [a] ```
  - ```PUSH number``` - положить число на стек ```[] -> [2]```
  - ```PUSH label``` - положить адрес метки на стек ```[] -> [0x801]```
  - ```HALT``` - остановка программы

### Семантика
  - Язык предполагает последовательное исполнение
  - Глобальная область видимости меток
  - В программе не может быть дублирующихся меток, определенных в разных местах с одним именем. 
  - В программе должна быть определена метка ```_start``` указывающая на адрес первой исполняемой команды
  - Метки для переходов определяются на отдельных строчках:
    ``` asm
    label: 
        INC
    ```
    И в другом месте (неважно, до или после определения) сослаться на эту метку:
    ``` asm 
    jmp label   ; --> `jmp 123`, где 123 - номер инструкции после объявления метки
    ```

## Транслятор


## Модель процессора

### DataPath

[//]: # (https://asciiflow.com/#/share/eJzFVstKw0AU%2FZUwK7UtfWwK3YkrwVJQAy6CZWhHW0yTkk6xtVSk%2BAkh%2BhGuupR%2BTb7ESTNJk3nkMVl4Ccm9meQ87syEbIAFZwj0rKVp1oEJ18gBPbAxwMoAvXar1akbYE3STrdLMoxWmBQG0Gj47qHIoSmEYVgJlsQAgz1fLiaVcMcQQ56Fi7I%2BOZ4FhqMXgX57Hgwik%2BeTFNm9kVanW300s521GirV7f2KZpbV7H990sccBMc8R6meBnmf91S5T0Gup9SWm%2BqUz1dn6iAh8%2F3gLsxzmbQHkSkFn5SNB2L4mUGFVX7WOleZT%2FY%2Bp4WcrweZjo%2F3E4NRHShKhQg7p5u%2Bd6AncS3HVumh4D1ho7gdwPLHavfsc4QJ23Of7t9dXw9W2i7GCOvT6ligkW2NMzl4LSc3ru9%2B%2BO7PEYsk39Xc5DVSttcFBLluZLheqr0FcAstBSGb1Gzp%2FtHL5W30djS9JsSjyRA6MadBIpk1w6JZzqO3L%2BqRIYzo3oZPJnyW8jF5rZ3AfW%2FUmheP4QKPwC9v9BC38L7kCLMmI2WLiGm0U8a4BmaRaHQHiqCTAHkGinAVMyQAY0LKEX6B4q9QNvL%2FHqW%2BLtJIN0jSrkJ4Ai3RD5dQY0UuQV0d8cq2sGObGvfDUVWpbk2xULkinrRWwCux5HKYwBZs%2FwD5cyhO&#41;)
```
        +-----------+                                                    
        |           +----push                                            
        |   data    |                            +----------+            
        |   stack   +----pop   sel               |          |            
        |           |           |                |  Memory  |            
        |           |         +-v-+              |          |<-- read    
        +-----------+         | M |              |          |            
        |           |         | U |<---------+---+          |<-- wrire   
        |    TOS  | |<--------+ X |          |   |          |            
        |         | |         |   |<---+     |   +----------+            
    (0) ++--------+-+         +---+    |     |   |   IO     |            
      |  |        |  |(0)              |     |   |          |            
      v  v        v  v                 |     |   +----------+            
     +----+      +----+                |     |          ^                
top->|MUX |      |MUX |<--second       |     |          |                
     +--+-+      +-+--+                |     |          +------+         
        |          |                   |     |          |      |         
        v          v                   |     |    +-----+----+ |         
      -------    ------                |     |    |    AR    |<+-latch_ar
      \      \  /      /               |     |    +----^-----+ |         
       \      \/      /z_flag          |     |         |       +1        
~-+/*^->\    ALU     /-----------+     |     |      +--+--+    |         
 +1 -1   \          /            |     |     |      | MUX |    |         
          --+-------             |     |     |      +-----+    |         
            |                    |     |     |        ^ ^      |         
            +--------------------+-----+-----+--------+ +------+         
                                 |           |                           
                           +-----v-------+   |                           
                           |             |   |                           
                           |   Control   |<--+                           
                           |    Unit     |                               
                           |             |                               
                           +-------------+                               
```

### Control Unit

[//]: # (https://asciiflow.com/#/share/eJytkk0KwjAQha9SZt2VC63d1o07QdwFJNSohZpIO4K1dOcRpN5FPI0nMdoq9DepNmSRGfK9N5NJDJzuGNjgCI6B8I0F9xBM8GnEApmOCRwJ2GNrZBKI5GlgDeUJ2RFlQMBoWY%2FLvesmhCsUq5k6RmGU3nOlObK9UqkSOOLAkQUdKa2qtVvQfb2qeTFbYLoaaim21dNGTXmIwcFFT3AF1VzehLlilU3qfet61u3pq6zVx2f1Rf06hQbFgrX8%2FTWEkqr1ySnvNap3EHobTv0wJ07LtU83%2FflUqLQr1f%2FbZocJRVpupZ4q7%2FSWATOKWw2Fpit6zN%2B9QwLJE2RWRN4%3D&#41;)
```
                            +---------------+
                            |               |
                 +--------->|    Step       |
                 |          |    Counter    |
                 |          |               |
                 |          +--------+------+
                 |                   |       
          +------+-------+           |       
          |              |           |       
          |  Instruction |           |       
   +------+  Decoder     |<----------+       
   |      |              |                   
   |      |              |                   
   |      +---+----------+                   
   |          |      ^                       
   |          |      |                       
instr     signals    |z_flag                 
   |          |      |                       
   |          v      |                       
   |      +----------+---+                   
   |      |   Data       |                   
   +----->|   Path       |                   
          |              |                   
          +--------------+                   
```
