all: bin/cube_sim bin/run_fcserver clients/cpp clients/python

clean:
	-rm -r bin
	-rm config/*.json
	-rm clients/python/opc.py*
	cd fadecandy/server && make clean
	cd openpixelcontrol && make clean
	cd clients/cpp && make clean
	cd clients/python && make clean

openpixelcontrol/bin/gl_server: force_look
	cd openpixelcontrol && make bin/gl_server

fadecandy/server/fcserver: force_look
	cd fadecandy/server && make

clients/cpp: force_look
	cd clients/cpp && make

clients/python: clients/python/opc.py force_look
	cd clients/python && make

clients/python/opc.py: fadecandy/examples/python/opc.py
	ln -s `pwd`/$^ $@

config/cube.py.json: config/cube.py config/base.py
	cd config && ./cube.py

bin/cube_sim: config/cube.py.json openpixelcontrol/bin/gl_server
	mkdir -p bin
	echo '#!/bin/bash' > bin/cube_sim
	echo `pwd`/openpixelcontrol/bin/gl_server -l config/cube.py.json -p 8888 >> bin/cube_sim
	chmod a+x bin/cube_sim

config/server_config.py.json: config/server_config.py
	cd config && ./server_config.py

# TODO(jsestrich) Move fadecandy server config somewhere more reasonable
bin/run_fcserver: fadecandy/server/fcserver config/server_config.py.json

	mkdir -p bin
	echo '#!/bin/bash' > bin/run_fcserver
	echo `pwd`/fadecandy/server/fcserver `pwd`/config/server_config.py.json >> bin/run_fcserver
	chmod a+x bin/run_fcserver

force_look:
	true
