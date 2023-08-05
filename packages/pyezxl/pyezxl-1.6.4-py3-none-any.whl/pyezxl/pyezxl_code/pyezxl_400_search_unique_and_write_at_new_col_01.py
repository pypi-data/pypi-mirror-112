#  -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

#선택한 영역에서 고유한값을 만들어서
#열 하나를 선택한후 나열하도록 한다

py_dic={}
for x in range(x1, x2+1):
	for y in range(y1, y2+1):
		cell_value = excel.read_cell_value(sheet_name,[x, y])

		#사전안에 현재 자료가 있는지 확인하는것
		if not(cell_value in py_dic) and not(cell_value==""): py_dic[cell_value]=""

excel.insert_y_line("", 1)
list_dic = list(py_dic.keys())
for no in range(len(list_dic)):
	excel.write_cell_value(sheet_name, [no+1, 1], list_dic[no])
