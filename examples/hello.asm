_start:
            PUSH    0x801       ; [0x801]
            PUSH    welcome     ; [0x801; welcome]
print_invitation:
            OVER                ; [0x801; welcome; 0x801]
            OVER                ; [0x801; welcome; 0x801; welcome]
            LOAD                ; [0x801; welcome; 0x801; "W"]
            PUSH    save_null   ; [0x801; welcome; 0x801; "W"; save_null]
            JZ                  ; [0x801; welcome; 0x801; "W"]
            SWAP                ; [0x801; welcome; "W"; 0x801]
            SAVE                ; [0x801; welcome]
            INC                 ; [0x801; welcome++]
            PUSH   print_invitation  ; [[0x801; welcome; print_invitation]
            JUMP                ; [0x801; welcome]

save_null:                      ; [0x801; welcome; 0x801; "\0"]
            SWAP                ; [0x801; welcome; "\0"; 0x801]
            SAVE                ; [0x801; welcome]
            POP                 ; [0x801]
            PUSH    data        ; [0x801; data]
read_input:
            OVER                ; [0x801; data; 0x801]
            LOAD                ; [0x801; data; "A"]
            PUSH   print_greeting  ; [0x801; data; "A"; print_greeting]
            JZ                  ; [0x801; data; "A"]
            OVER                ; [0x801; data; "A"; data]
            SAVE                ; [0x801; data]
            INC                 ; [0x801; data++]
            PUSH    read_input  ; [0x801; data; read_input]
            JUMP                ; [0x801; data]

print_greeting:                 ; [0x801; data; "\0"]
            POP                 ; [0x801; data]
            POP                 ; [0x801]
            PUSH    greeting    ; [0x801; greeting]
print_data:
            OVER                ; [0x801; greeting; 0x801]
            OVER                ; [0x801; greeting; 0x801; greeting]
            LOAD                ; [0x801; greeting; 0x801; "H"]
            PUSH    print_name  ; [0x801; greeting; 0x801; "H"; print_name]
            JZ                  ; [0x801; greeting; 0x801; "H"]
            SWAP                ; [0x801; greeting; "A"; 0x801]
            SAVE                ; [0x801; greeting]
            INC                 ; [0x801; greeting++]
            PUSH   print_data   ; [0x801; greeting; print_data]
            JUMP

print_name:                     ; [0x801; greeting; 0x801; "\0"]
            POP                 ; [0x801; greeting; 0x801]
            POP                 ; [0x801; greeting]
            POP                 ; [0x801]
            PUSH    data        ; [0x801; data]
print_data:
            OVER                ; [0x801; data; 0x801]
            OVER                ; [0x801; data; 0x801; data]
            LOAD                ; [0x801; data; 0x801; "A"]
            PUSH    exit        ; [0x801; data; 0x801; "A"; exit]
            JZ                  ; [0x801; data; 0x801; "A"]
            SWAP                ; [0x801; data; "A"; 0x801]
            SAVE                ; [0x801; data]
            INC                 ; [0x801; data++]
            PUSH    print_data
            JUMP

exit:
            HALT



welcome:
            WORD    "What`s your name?"
greeting:
            WORD    "Hello, "
data:
            WORD    0x0