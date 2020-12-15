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

'''
	Simulate a receiver for UDP packets
'''

from socket import *
import struct, threading

import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import random, pygame, time
from pygame.locals import *
from math import floor, ceil, sqrt

WINSIZE = [800, 600]
X = [1, 0]
Y = [0, 1]
FPS = 12

aileron = None
elevator = None
rudder = None
throttle = None

def v_add(a, b):
	return [a[0] + b[0], a[1] + b[1]]

def v_mult(c, v):
	return [c * v[0], c * v[1]]

def draw_triangle(val, color, x0, dx, y0, dy, ax_base, ax_var):
#def draw_triangle(val=0.5, color=[255, 0, 0], x0=50, dx=0, y0=150+300, dy=-300, 
#, ax_base=[1, 0], ax_var=[0, 1]):
	x = x0 + int(val * dx)
	y = y0 + int(val * dy)
	p1 = v_add(v_add(v_mult(8, ax_base), v_mult(10, ax_var)), [x, y])
	p2 = v_add(v_add(v_mult(8, ax_base), v_mult(-10, ax_var)), [x, y])
	p3 = v_add(v_mult(38, ax_base), [x, y])
	pygame.draw.polygon(screen, color, [p1, p2, p3], 5)

def update_triangle(name, val, color, x0, dx, y0, dy, ax_base, ax_var, prev={}):
	if name in prev:
		draw_triangle(prev[name], [0, 0, 0], x0, dx, y0, dy, ax_base, ax_var)
	if val is None:
		return
	draw_triangle(val, color, x0, dx, y0, dy, ax_base, ax_var)
	prev[name] = val

def update_all():
	update_triangle(
		'aileron', aileron, [0, 255, 0], 450, 100, 175, 0, [0, 1], [1, 0])
	update_triangle(
		'elevator', elevator, [0, 255, 0], 200, 0, 300, -100, [1, 0], [0, 1])
	update_triangle(
		'rudder', rudder, [0, 255, 0], 450, 100, 425, 0, [0, -1], [1, 0])
	update_triangle(
		'throttle', throttle, [0, 255, 0], 50, 0, 450, -300, [1, 0], [0, 1])

def receiver0(s):
	global aileron, elevator, rudder, throttle
	while True:
		a = s.recv(1000)
		vals = struct.unpack('>' + 'f' * (len(a) // 4), a)
		a, e, r, t = vals[:4]
		aileron = min(max(a, -1), 1)
		elevator = min(max(e, -1), 1)
		rudder = min(max(r, -1), 1)
		throttle = min(max(t, 0), 1)

def receiver1(s):
	global aileron, elevator, throttle
	while True:
		a = s.recv(1000)
		vals = struct.unpack('>' + 'f' * (len(a) // 4), a)
		a, e, t = vals[:3]
		aileron = min(max(a, -1), 1)
		elevator = min(max(e, -1), 1)
		throttle = min(max(t, 0), 1)

def receiver2(s):
	global rudder
	while True:
		a = s.recv(1000)
		vals = struct.unpack('>' + 'f' * (len(a) // 4), a)
		t = vals[0]
		rudder = min(max(t, -1), 1)

if __name__ == '__main__':
	clock = pygame.time.Clock()
	pygame.init()
	screen = pygame.display.set_mode(WINSIZE)
	pygame.display.set_caption('FGFS Controller Receiver')
	pygame.draw.rect(screen, [0, 255, 0], pygame.Rect(50, 150, 5, 300))
	pygame.draw.rect(screen, [0, 255, 0], pygame.Rect(200, 200, 5, 200))
	pygame.draw.rect(screen, [0, 255, 0], pygame.Rect(350, 175, 200, 5))
	pygame.draw.rect(screen, [0, 255, 0], pygame.Rect(350, 425, 200, 5))
	pygame.display.update()

	if '--split' in sys.argv[1:]:
		s1 = socket(AF_INET, SOCK_DGRAM)
		s2 = socket(AF_INET, SOCK_DGRAM)
		s1.bind(('0.0.0.0', 6789))
		s2.bind(('0.0.0.0', 6788))
		threading.Thread(target=receiver1, args=(s1,), daemon=True).start()
		threading.Thread(target=receiver2, args=(s2,), daemon=True).start()
	else:
		s = socket(AF_INET, SOCK_DGRAM)
		s.bind(('0.0.0.0', 6789))
		threading.Thread(target=receiver0, args=(s,), daemon=True).start()

	while True:
		update_all()
		pygame.display.update()
		clock.tick(FPS)

