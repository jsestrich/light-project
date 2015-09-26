all: bin/cube_sim bin/run_fcserver

clean:
	rm bin/*
	rm layout/*.json
	cd fadecandy/server && make clean
	cd openpixelcontrol && make clean

openpixelcontrol/bin/gl_server: force_look
	cd openpixelcontrol && make bin/gl_server

layout/cube.py.json: layout/cube.py layout/base.py
	cd layout && ./cube.py 12 8 60

bin/cube_sim: layout/cube.py.json openpixelcontrol/bin/gl_server
	mkdir -p bin
	echo '#!/bin/bash' > bin/cube_sim
	echo `pwd`/openpixelcontrol/bin/gl_server -l layout/cube.py.json -p 8888 >> bin/cube_sim
	chmod a+x bin/cube_sim

fadecandy/server/fcserver: force_look
	cd fadecandy/server && make

# TODO(jsestrich) Move fadecandy server config somewhere more reasonable
bin/run_fcserver: fadecandy/server/fcserver
	mkdir -p bin
	echo '#!/bin/bash' > bin/run_fcserver
	echo `pwd`/fadecandy/server/fcserver `pwd`/fadecandy/server/fcserver.json >> bin/run_fcserver
	chmod a+x bin/run_fcserver

force_look:
	true
