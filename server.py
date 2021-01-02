#
# FGFSControllerWeb - Using an iOS Device to Control FGFS
# Copyright (C) 2020  lxylxy123456
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from flask import Flask, request, send_from_directory, redirect
from flask_sockets import Sockets
import re, jinja2, json, random, os, sys, struct, argparse
from urllib import parse
from socket import *
app = Flask(__name__)
sockets = Sockets(app)

@app.route('/')
@app.route('/<int:port>')
def main_page(port=None):
	dict_render = {
		'aileron_duplicate': 1,
		'elevator_duplicate': 1,
		'rudder_duplicate': 1,
		'throttle_duplicate': 5,
		'aileron_active': True,
		'elevator_active': True,
		'rudder_active': False,
		'aileron_factor': 1.0,
		'elevator_factor': 1.0,
		'rudder_factor': 1.5,
		'json': json,
		'port': 6789,
	}
	if port == 6789:
		dict_render.update({
			'rudder_duplicate': 0,
			'rudder_active': False,
			'port': port,
		})
	elif port == 6788:
		dict_render.update({
			'aileron_duplicate': 0,
			'rudder_duplicate': 0,
			'aileron_active': False,
			'rudder_active': False,
			'elevator_factor': 2.0,
			'port': port,
		})
	elif port is None:
		pass
	else:
		raise ValueError
	home_template = jinja2.Template(open(home_template_name).read())
	return home_template.render(**dict_render)

@app.route('/gateway')
def gateway():
	gate_template = jinja2.Template(open(gate_template_name).read())
	return gate_template.render()

@app.route('/vector.js')
def vector_js():
	return send_from_directory(DIR, 'vector.js')

@app.route('/proxy')
def proxy_udp():
	addr = request.args['addr']
	port = int(request.args['port'])
	data = json.loads(request.args['data'])
	payload = struct.pack('>' + 'f' * len(data), *data)
	s = socket(AF_INET, SOCK_DGRAM)
	s.sendto(payload, (addr, port))
	return payload

@sockets.route('/echo')
def echo_socket(ws):
	while not ws.closed:
		message = ws.receive()
		ws.send(message.upper())

@app.route('/favicon.ico')
def favicon():
	return ''

@app.errorhandler(404)
def page_not_found(error):
	return redirect("/gateway")

DIR = os.path.dirname(os.path.realpath(__file__))
home_template_name = os.path.join(DIR, 'f.html')
home_template = jinja2.Template(open(home_template_name).read())
gate_template_name = os.path.join(DIR, 'g.html')
gate_template = jinja2.Template(open(gate_template_name).read())

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--host', default='0.0.0.0')
	parser.add_argument('--port', type=int, default=23456)
	parser.add_argument('--ws', action='store_true')
	args = parser.parse_args()
	keyfile = os.path.join(DIR, 'ssl.key')
	certfile = os.path.join(DIR, 'ssl.cert')
	if args.ws:
		from gevent import pywsgi
		from geventwebsocket.handler import WebSocketHandler
		server = pywsgi.WSGIServer(('', args.port), app,
									handler_class=WebSocketHandler,
									keyfile=keyfile, certfile=certfile)
		server.serve_forever()
	else:
		app.run(host=args.host, port=args.port, debug=True, threaded=True,
				ssl_context=(certfile, keyfile))

# Generate certificates:
# https://werkzeug.palletsprojects.com/en/1.0.x/serving/#generating-certificates
# openssl genrsa 1024 > ssl.key
# openssl req -new -x509 -nodes -sha1 -days 365 -key ssl.key > ssl.cert

