# 0.5초이내에 화살표를 누르면 시간이 연장이 되고
# 누르지 않으면 셀에 색이 입혀지고 오른쪽으로 한칸 이동하는 샘플이다

from pynput import keyboard
import pyezxl
import time

excel = pyezxl.pyezxl("")
sheet_name = excel.read_activesheet_name()
color = excel.color()
excel.set_y_length("", [1,30],3)
excel.set_range_line("", [2,2,30,25])
duration = 0
excel.set_cell_select("", [5,5])

def on_press(key):
	#키가 눌렀을때 실행 되는것
	global duration

	if key == key.left:
		duration = 0
	if key == key.right:
		duration = 0
	if key == key.up:
		duration = 0
	if key == key.down:
		duration = 0


def on_release(key):
	#키가 눌렀다 떼지면 실행 되는것
	if key == keyboard.Key.esc:  # esc 키가 입력되면 종료
		return False

# 키보드의 상태를 무한 루프 돌려서 받는 것이다
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

while True:
		if duration > 0.5:
			xyxy = excel.read_activecell_address()
			print(xyxy)
			excel.set_cell_color("", [xyxy[0], xyxy[1]+1], color["indigo"])
			excel.set_cell_select("", [xyxy[0], xyxy[1]+1])
			duration=0
		else:
			duration = duration + 0.1
			time.sleep(0.1)