message:
            WORD 	'hello, world!'
_start:
            PUSH 	message     ; [message_addr]
loop:
            DUP                 ; [message_addr; message_addr]
            LOAD		        ; [message_addr, "h"]
            PUSH    exit        ; [message_addr, "h"; exit]
	        JZ   	    	    ; [message_addr, "h"]
	        PUSH    0x801       ; [message_addr, "h", 0x801]
	        SAVE        	    ; [message_addr]
	        INC		            ; [message_addr++ ]
	        PUSH    loop        ; [message_addr; loop]
	        JUMP
exit:
	        HALT
