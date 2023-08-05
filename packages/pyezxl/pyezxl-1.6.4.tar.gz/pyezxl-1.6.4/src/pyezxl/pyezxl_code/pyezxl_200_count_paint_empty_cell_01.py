#  -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

temp_result = 0
#빈셀의 갯수를 계산한다
for x in range(x1, x2+1):
	for y in range(y1, y2+1):
		cell_value = excel.read_cell_value(sheet_name,[x, y])
		if cell_value == None :
			excel.set_cell_color("activesheet", [x, y], 16)
			temp_result = temp_result +1
excel.show_messagebox_value("Empty Cells : " + str(temp_result))
