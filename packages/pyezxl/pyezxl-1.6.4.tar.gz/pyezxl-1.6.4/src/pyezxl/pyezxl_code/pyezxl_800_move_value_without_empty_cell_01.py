#  -*- coding: utf-8 -*-

import pyezxl

#선택한 영역에서 세로의 값중에서 빈셀을 만나면
#아래의 값중 있는것을 위로 올리기

excel = pyezxl.pyezxl('activeworkbook')
[x1, y1, x2, y2] = excel.read_select_address()

for y in range(y1, y2 + 1):
	for x in range(x1, x2 + 1):
		current_value = excel.read_cell_value("", [x,y])
		if current_value == "" or current_value == None:
			for x_new in range(x+1, x2+1):
				temp_value = excel.read_cell_value("", [x_new, y])
				if temp_value:
					excel.write_cell_value("", [x, y],temp_value )
					excel.write_cell_value("", [x_new, y],"")
					break
