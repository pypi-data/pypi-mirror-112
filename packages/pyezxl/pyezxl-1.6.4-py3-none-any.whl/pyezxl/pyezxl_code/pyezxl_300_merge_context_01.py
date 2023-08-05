#  -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl("activeworkbook")

activesheet_name = excel.read_activesheet_name()
y_start, x_start, y_end, x_end= excel.read_range_select_v01()[2]

temp_result=""
result=""

for y in range(y_start, y_end+1):
	for x in range(x_start, x_end+1):
		temp_result = excel.read_cell_value(activesheet_name,[x, y])
		if y==y_end and x==x_end:
			result=result + str(temp_result)
		else:
			result=result + str(temp_result) + "\n"
excel.write_range_merge(activesheet_name, [x_start, y_start, x_end, y_end] )
excel.write_cell_value(activesheet_name,[x_start, y_start], result)

