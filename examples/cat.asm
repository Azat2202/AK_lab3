_start:
            PUSH    0x801       ; [0x801]
loop:
            DUP                 ; [0x801; 0x801]
            LOAD                ; [0x801; "char"]
            PUSH    exit        ; [0x801; "char"; exit]
            JZ                  ; [0x801; "char"]
            OVER                ; [0x801; "char"; 0x801]
            SAVE                ; [0x801]
            PUSH    loop        ; [0x801; loop]
            JMP                 ; [0x801]

exit:
            HALT
