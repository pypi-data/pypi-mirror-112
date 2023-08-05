from pynput import keyboard
import pyezxl
import time
import random

excel = pyezxl.pyezxl("")
sheet_name = excel.read_activesheet_name()
color = excel.color()
excel.set_y_length("", [1,30],3)
excel.set_range_line("", [2,2,30,25])
excel.set_range_color("", [1,1,35,30], color[""])

for a in range(1, 3):
	excel.set_cell_color("", [3, random.randrange(2, 25)], color["black"])

excel.set_cell_color("", [28, 13], color["red"])
excel.set_range_select("", [28, 13, 28, 13])

arrow = "↑"
isActive = True
position = {'before':13, 'now':13, "shoot": "off"}
shoot_x = 28
shoot_y = 13
temp = "shoot"
shoot = "no"
def on_press(key):
	#키가 눌렀을때 실행 되는것
	global shoot_y
	global position
	global shoot

	if key == key.left:
		position['now'] -= 1
		if position['now'] < 2: position['now'] = 2
	if key == key.right:
		position['now'] += 1
		if position['now'] > 25: position['now'] = 25
	if key == key.up:
		if shoot == "yes":
			pass
		if shoot == "no":
			shoot = "yes"
			shoot_y = position['now']

def on_release(key):
	#키가 눌렀다 떼지면 실행 되는것
	if key == keyboard.Key.esc:  # esc 키가 입력되면 종료
		return False

# 키보드의 상태를 무한 루프 돌려서 받는 것이다
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

while isActive:
	if position['now'] < position['before']:
		#왼쪽을 누르면, 맨밑의 영역의 색을 다 지운후 한칸 왼쪽 옆에 색을 칠한다
		excel.set_range_color("", [28, 2, 28, 25], color[""])
		excel.set_cell_color("", [28, position['now']], color["pink_p"])
		position['before'] = position['now']
	if position['now'] > position['before']:
		#오른쪽을 누르면, 맨밑의 영역의 색을 다 지운후 한칸 오른쪽에 색을 칠한다
		excel.set_range_color("", [28, 2, 28, 25], color[""])
		excel.set_cell_color("", [28, position['now']], color["pink_p"])
		position['before'] = position['now']
	if shoot =="yes":
		# 화살이 한칸씩 위로 움직이는 것이다
		excel.write_cell_value("", [shoot_x, shoot_y], "")
		shoot_x -= 1
		excel.write_cell_value("", [shoot_x, shoot_y], arrow)

		# 화살이 맨위의 검정과 맞다으면 폭발하는 느낌으로 만들어서 색을 지우는 것
		if int(excel.read_cell_color("", [shoot_x, shoot_y])) == 0 :
			for a in range(3):
				excel.set_cell_color("", [shoot_x, shoot_y], color["indigo"])
				excel.set_cell_color("", [shoot_x+1, shoot_y+1], color["blue"])
				excel.set_cell_color("", [shoot_x, shoot_y+1], color["red"])
				excel.set_cell_color("", [shoot_x+1, shoot_y], color["yellow"])
				time.sleep(0.1)
				excel.set_cell_color("", [shoot_x, shoot_y], color[""])
				excel.set_cell_color("", [shoot_x+1, shoot_y+1], color[""])
				excel.set_cell_color("", [shoot_x, shoot_y+1], color[""])
				excel.set_cell_color("", [shoot_x+1, shoot_y], color[""])

			excel.write_cell_value("", [shoot_x, shoot_y], "")
			shoot = "no"
			shoot_x = 28

	if shoot =="no":
		# 만약 색이 지운것이 3개 이하이면 3개를 만드는 것이다
		aa=0
		for no in range(2, 25):
			color_no = excel.read_cell_color("", [3, no])
			if int(color_no) ==0:
				aa = aa +1
		if int(aa) < 3:
			for a in range(aa, 3):
				excel.set_cell_color("", [3, random.randrange(2, 25)], color["black"])

	if shoot_x == 2:
		# 화살표가 계속 올라가다가 2열에 만나면, 그만 올라가고
		# 새로운 화살이 나갈수 있도록 상태를 변경하는것이다
		excel.write_cell_value("", [shoot_x, shoot_y], "")
		shoot = "no"
		shoot_x = 28

	excel.set_range_select("", [28, position['now']])
