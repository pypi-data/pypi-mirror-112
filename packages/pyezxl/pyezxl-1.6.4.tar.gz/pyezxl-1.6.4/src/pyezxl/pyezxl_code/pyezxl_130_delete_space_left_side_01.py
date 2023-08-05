#  -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

#왼쪽끝과 오른쪽 끝의 공백을 삭제하는 것
for x in range(x1, x2+1):
	for y in range(y1, y2+1):
		cell_value = excel.read_cell_value(sheet_name,[x, y])
		changed_data = str(cell_value).lstrip()
		if cell_value == changed_data or cell_value == None or type(cell_value)==type(123):
			pass
		else:
			excel.write_cell_value(sheet_name, [x, y], changed_data)
			excel.set_cell_color(sheet_name, [x, y], 16)
