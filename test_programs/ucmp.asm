iAddi 	T0 ZERO 0x0
iAddi 	ZERO ZERO 0x994c
Lsfti	T0 T0 0x10
iAddi 	T0 T0 0x19
iAddi 	ZERO ZERO 0x994c
iAddi 	T1 ZERO 0x0
Lsfti	T1 T1 0x10
iAddi 	T1 T1 0x18
ucmp  	T2 T0 T1
j 0
ori 0x100
