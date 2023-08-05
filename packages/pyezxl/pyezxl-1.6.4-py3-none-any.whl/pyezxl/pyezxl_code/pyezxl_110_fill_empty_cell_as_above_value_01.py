#  -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2]= excel.read_select_address()

#빈셀을 발견하면 바로위의 자료로 넣기
#채우기 : 빈셀 바로위의 것으로 채우기
old_data=""
for y in range(y1, y2+1):
	for x in range(x1, x2+1):
		cell_value = excel.read_cell_value(sheet_name,[x, y])
		if x == x1:
			#만약 자료가 제일 처음이라면
			old_data=cell_value
		else: 
			if cell_value == None:
				excel.write_cell_value(sheet_name,[x, y],old_data)
			else:
				old_data=cell_value
