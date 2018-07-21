hoge:
	iAddi	S0	S1	0x12
	iAddi	S0	S1	0x12
	iAddi	S0	S1	0x12
	iAddi	S0	S1	0x12
	iAddi	S0	S1	0x12
	iAddi	S0	S1	0x12
	return
main:
	iAdd	S0	S1	ZERO
	iAdd	S0	S1	ZERO
	iAdd	S0	S1	ZERO
	iAdd	S0	S1	ZERO
	call	hoge	ZERO	ZERO	ZERO	ZERO
	iAdd	S0	S1	ZERO
	iAdd	S0	S1	ZERO
	iAdd	S0	S1	ZERO
	iAdd	S0	S1	ZERO
	iAdd	S0	S1	ZERO
