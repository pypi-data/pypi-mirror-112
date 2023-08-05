#  -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

#새로운 가로열을 선택한 영역에 1개씩 추가하는것이다
step_n = excel.read_messagebox_value("Please Input how many lines will be inserted at each x-line")
if step_n =="" or step_n==None: step_n=1

for x in range(x2, x1, -1):
	for a in range(int(step_n)):
		excel.insert_x_line(sheet_name, x)