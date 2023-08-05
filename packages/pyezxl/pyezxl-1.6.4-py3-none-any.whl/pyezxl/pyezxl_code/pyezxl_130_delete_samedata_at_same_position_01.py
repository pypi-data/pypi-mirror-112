#  -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl("")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

#선택한 영역안의 첫번째것은 냅두고 나머지부터 같은것은 삭제한다
py_dic={}
for x in range(x1, x2+1):
	for y in range(y1, y2+1):
		cell_value = excel.read_cell_value(sheet_name,[x, y])

		#사전안에 현재 자료가 있는지 확인하는것
		if cell_value in py_dic:
			excel.write_cell_value(sheet_name, [x, y], "")
		else:
			py_dic[cell_value]=""
