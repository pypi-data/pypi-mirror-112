#  -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

# 새로운 세로행을 만든후 그곳에 두열을 서로 하나씩 포개어서 값넣기
# a 1   ==> a
# b 2       1
#           b
#           2

new_x=1

excel.insert_y_line("", 1)
for x in range(x1, x2+1):
	for y in range(y1, y2+1):
		cell_value = str(excel.read_cell_value(sheet_name,[x, y+1]))
		excel.write_cell_value(sheet_name,[new_x, 1], cell_value)
		new_x = new_x+1
