#  -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl("")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

#선택한 영역에서 2번이상 반복된것만 색칠하기
py_dic = {}
for x in range(x1, x2+1):
	for y in range(y1, y2+1):
		cell_value = excel.read_cell_value(sheet_name,[x, y])
		if cell_value != "" and  cell_value != None:
			if not py_dic[cell_value]:
				py_dic[cell_value] = 1
			else:
				py_dic[cell_value] = py_dic[cell_value] +1

			if py_dic[cell_value] >= 2:
				excel.set_cell_color(sheet_name, [x, y], 4)
