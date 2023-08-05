#  -*- coding: utf-8 -*-

import pyezxl

# 선택한 영역에서 각셀마다 왼쪽에서 N번째까지의글자삭제하기
excel = pyezxl.pyezxl("activeworkbook")
activesheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_range_select()

aaa = excel.read_messagebox_value("Please Input Number : ")

for x in range(x1, x2 + 1):
	for y in range(y1, y2 + 1):
		current_data = str(excel.read_cell_value(activesheet_name, [x, y]))
		print(current_data)
		if current_data == "" or current_data == None or current_data == "None":
			pass
		else:
			excel.write_cell_value(activesheet_name, [x, y], current_data[int(aaa):])
