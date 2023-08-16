CC=i686-w64-mingw32-gcc
CFLAGS=-g -c -Wall -masm=intel
LFLAGS=-shared -v -O0

TARGET=game_controller.dll
SOURCES=game_controller.c
OBJECTS=$(SOURCES:.c=.o)

$(TARGET): $(OBJECTS)
	$(CC) $(LFLAGS) $(OBJECTS) -o $@


test: $(TARGET)
	wine python -m unittest

all: $(TARGET) test
