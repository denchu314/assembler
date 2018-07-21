	j main
hoge:
	arrival
	iAdd	ZERO	ZERO	ZERO	
	iAdd	ZERO	ZERO	ZERO	
	iAdd	ZERO	ZERO	ZERO	
	iAdd	ZERO	ZERO	ZERO	
	iAdd	ZERO	ZERO	ZERO	
	iAdd	ZERO	ZERO	ZERO	
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
