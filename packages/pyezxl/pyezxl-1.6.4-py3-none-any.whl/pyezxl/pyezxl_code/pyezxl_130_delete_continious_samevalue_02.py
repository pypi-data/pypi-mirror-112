#  -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

#선택한 영역중 연속된 같은자료 삭제
flag_same = 0
old_data=""

for y in range(y1, y2 + 1):
	for x in range(x1, x2+1):
		if flag_same == 0:
			cell_value = excel.read_cell_value(sheet_name,[x, y])
		cell_value_down = excel.read_cell_value(sheet_name,[x+1, y])

		if cell_value == cell_value_down:
			excel.write_cell_value(sheet_name, [x+1, y], "")
			flag_same = 1
		else:
			flag_same = 0
