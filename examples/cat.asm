_start:
            PUSH    0x801       ; [0x801]
loop:
            DUP                 ; [0x801; 0x801]
            LOAD                ; [0x801; "char"]
            JZ      exit        ; [0x801; "char"]
            OVER                ; [0x801; "char"; 0x801]
            SAVE                ; [0x801]
            JMP     loop        ; [0x801]

exit:
            HALT
