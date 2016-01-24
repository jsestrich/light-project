all: bin/colorfill bin/colorsphere

clean:
	rm -rf bin
	rm -rf lib

bin:
	mkdir -p bin

obj:
	mkdir -p lib

obj/opc_client.o: opc_client.c
	gcc -c -o $@ $^

bin/colorfill: bin colorfill.c opc_client.o
	gcc -o $@ colorfill.c opc_client.o

bin/colorsphere: bin colorsphere.c opc_client.o
	gcc -o $@ colorsphere.c opc_client.o
