from flask import Flask, request, send_from_directory, redirect
from flask_sockets import Sockets
import re, jinja2, json, random, os, sys, struct
from urllib import parse
from socket import *
app = Flask(__name__)
sockets = Sockets(app)

@app.route('/')
@app.route('/<int:port>')
def main_page(port=None) :
	dict_render = {
		'aileron_duplicate': 1,
		'elevator_duplicate': 1,
		'rudder_duplicate': 1,
		'throttle_duplicate': 5,
		'aileron_active': True,
		'elevator_active': True,
		'rudder_active': False,
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
			'port': port,
		})
	elif port is None:
		pass
	else:
		raise ValueError
	home_template = jinja2.Template(open(home_template_name).read())
	return home_template.render(**dict_render)

@app.route('/vector.js')
def vector_js() :
	return send_from_directory(DIR, 'vector.js')

@app.route('/proxy')
def proxy_udp() :
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
def favicon() :
	return ''

@app.errorhandler(404)
def page_not_found(error):
	return '404 (Not Found)'

DIR = os.path.dirname(os.path.realpath(__file__))
home_template_name = os.path.join(DIR, 'f.html')
home_template = jinja2.Template(open(home_template_name).read())

if __name__ == '__main__' :
	if len(sys.argv) > 1 :
		host = sys.argv[1]
	else :
		host = '127.0.0.1'
	if len(sys.argv) > 2 :
		port = int(sys.argv[2])
	else :
		port = 1234
	if not 'ws':
		from gevent import pywsgi
		from geventwebsocket.handler import WebSocketHandler
		server = pywsgi.WSGIServer(('', 23456), app,
									handler_class=WebSocketHandler,
									keyfile=os.path.join(DIR, 'ssl.key'),
									certfile=os.path.join(DIR, 'ssl.cert'))
		server.serve_forever()
	else:
		app.run(host=host, port=port, debug=True, threaded=True,
				ssl_context=(os.path.join(DIR, 'ssl.cert'),
							os.path.join(DIR, 'ssl.key')))
	# https://werkzeug.palletsprojects.com/en/1.0.x/serving/#generating-certificates
	# openssl genrsa 1024 > ssl.key
	# openssl req -new -x509 -nodes -sha1 -days 365 -key ssl.key > ssl.cert

