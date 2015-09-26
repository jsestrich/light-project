all: bin/cube_sim

clean:
	rm bin/*
	rm layout/*.json
	cd openpixelcontrol && make clean

openpixelcontrol/bin/gl_server:
	cd openpixelcontrol && make bin/gl_server

layout/cube.py.json: layout/cube.py layout/base.py
	cd layout && ./cube.py 12 8 60

bin/cube_sim: layout/cube.py.json openpixelcontrol/bin/gl_server
	mkdir -p bin
	echo '#/bin/bash'
	echo `pwd`/openpixelcontrol/bin/gl_server -l layout/cube.py.json 8888 >> bin/cube_sim
	chmod a+x bin/cube_sim
