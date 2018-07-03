TARGET = modasm
OBJS = main.o 
Z_TOOLS = ../z_tools

CC = gcc
CFLAGS += -Wall

.PHONY: all
all :
	make $(TARGET)

#instruction.o : instruction.c
#	$(CC) -c $(CFLAGS) instruction.c
#emulator.o : emulator.c
#	$(CC) -c $(CFLAGS) emulator.c
#main.o : main.c
#	$(CC) -c $(CFLAGS) main.c
#$(TARGET) : main.o instruction.o emulator.o
#	$(CC) -o $(TARGET) $(CFLAGS) main.o instruction.o emulator.o
%.o : %.c Makefile
	$(CC) $(CFLAGS) -c $<

$(TARGET) : $(OBJS) Makefile
	$(CC) -o $@ $(OBJS)
clean :
	rm *.o
	rm $(TARGET)

