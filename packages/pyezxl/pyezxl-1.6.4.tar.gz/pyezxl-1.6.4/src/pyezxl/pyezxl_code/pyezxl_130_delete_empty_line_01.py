#  -*- coding: utf-8 -*-

#전체가 빈 가로열 삭제 

import pyezxl
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

for x in range(x2, x1-1, -1):
	#여기 위까지는 선택한 영역에서 가로열만 밑에서부터 순차적으로 실행하는것
	if excel.check_x_empty(sheet_name, x) ==0:
		excel.delete_x_line(sheet_name, x)
