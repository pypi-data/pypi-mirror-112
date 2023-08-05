#  -*- coding: utf-8 -*-
#먼저 키보드로 입출력을 받기위해 pynput을 설치해야 한다
# 엑셀의 시트 전체의 높이는 11.4, 넓이는 1.2정도로 만든다

from pynput import keyboard
import pyezxl
import time
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

isActive = True
position = {'x': 3, 'y': 15}
rotation = {"z":4}
block = {"type": "bar"}
def key_press(key):
	global position
	if key == key.up: rotation['z'] += 1
	if key == key.down: rotation['z'] += 1
	if key == key.left: position['y'] -= 1
	if key == key.right: position['y'] += 1
	if position['y'] < 3: position['y'] = 3
	if position['y'] > 23: position['y'] = 23
	if position['x'] < 1: position['x'] = 1
	if position['x'] > 30: position['x'] = 30

def key_release(key):
	if key == keyboard.Key.esc:
		global isActive
		isActive = False
		return False

listener = keyboard.Listener(on_press=key_press, on_release=key_release)
listener.start()


def block(block_type):
	if block_type =="i":
		result=[[-1, 0],[0, 0],[1, 0]]
	if block_type =="t":
		result= [[-1, -1],[-1, 0],[-1, 1],[0, 0],[1, 0]]
	if block_type =="z":
		result=[[-1, -1],[-1, 0],[0, 0],[1, 0],[1, 1]]
	if block_type =="rz":
		result=[[-1, 0],[-1, 1],[0, 0],[1, -1],[1, 0]]
	if block_type =="b":
		result=[[0, 0],[0, 1],[1, 0],[1, 1]]
	return result

def block_rotation(block_type, degree):
	if block_type =="i":
		if degree==0: result=[[0, 0],[0, 0],[0, 0]]
		if degree==1: result=[[1, -1],[0, 0],[-1, 1]]
		if degree==2: result=[[2, 0],[0, 0],[-2, 0]]
		if degree==3: result=[[1, 1],[0, 0],[-1, -1]]
	if block_type =="t":
		if degree==0: result=[[0, 0],[0, 0],[0, 0],[0, 0],[0, 0]]
		if degree==1: result=[[2, 0],[1, -1],[0, -2],[0, 0],[-1, 1]]
		if degree==2: result=[[2, 2],[2, 0],[2, -2],[0, 0],[-2, 0]]
		if degree==3: result=[[0, 2],[1, 1],[2, 0],[0, 0],[-1, -1]]
	if block_type =="z":
		if degree==0: result=[[0, 0],[0, 0],[0, 0],[0, 0],[0, 0]]
		if degree==1: result=[[2, 0],[1, -1],[0, 0],[-1, 1],[-2, 0]]
		if degree==2: result=[[0, 0],[0, 0],[0, 0],[0, 0],[0, 0]]
		if degree==3: result=[[2, 0],[1, -1],[0, 0],[-1, 1],[-2, 0]]
	if block_type =="rz":
		if degree==0: result=[[0, 0],[0, 0],[0, 0],[0, 0],[0, 0]]
		if degree==1: result=[[1, -1],[0, -2],[0, 0],[0, 2],[-1, 1]]
		if degree==2: result=[[0, 0],[0, 0],[0, 0],[0, 0],[0, 0]]
		if degree==3: result=[[1, -1],[0, -2],[0, 0],[0, 2],[-1, 1]]
	if block_type =="b":
		if degree==0: result=[[0, 0],[0, 0],[0, 0],[0, 0]]
		if degree==1: result=[[0, 0],[0, 0],[0, 0],[0, 0]]
		if degree==2: result=[[0, 0],[0, 0],[0, 0],[0, 0]]
		if degree==3: result=[[0, 0],[0, 0],[0, 0],[0, 0]]
	return result

while isActive:
	for block_type in ["t", "z", "rz", "i", "b"]:
		excel.set_range_nocolor("", [1, 1, 30, 30])
		block_result = block(block_type)
		for no in range(1, 30):
			if position['x'] < 30: position['x'] += 1
			excel.set_range_nocolor("", [1, 1, 30, 30])
			degree=rotation['z']%4
			block_rotation_result = block_rotation(block_type, degree)
			for one in range(len(block_result)):
				x=block_result[one][0] +block_rotation_result[one][0]+position['x']
				y=block_result[one][1] +block_rotation_result[one][1]+position['y']
				print(x,y)
				excel.set_cell_color("", [x,y], 4)
			time.sleep(0.3)
		position["x"] = 3
		position["y"] = 15
		excel.set_range_nocolor("", [1, 1, 50, 50])

del listener

