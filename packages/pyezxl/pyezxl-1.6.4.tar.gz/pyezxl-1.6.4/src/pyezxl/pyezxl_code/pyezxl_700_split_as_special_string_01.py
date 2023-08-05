#  -*- coding: utf-8 -*-

# 선택한 1줄의 영역에서 원하는 문자나 글자를 기준으로 분리할때
# 2개의 세로행을 추가해서 결과값을 쓴다

import pyezxl
import re

excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

aaa = excel.read_messagebox_value("Please Input Split String")

excel.insert_y_line("", y1 + 1)
excel.insert_y_line("", y1 + 1)
result=[]
length=2

for x in range(x1, x2 + 1):
	for y in range(y1, y2 + 1):
		cell_value = str(excel.read_cell_value(sheet_name, [x, y]))
		list_data = cell_value.split(aaa)
		result.append(list_data)

for x_no in range(len(result)):
		if len(result[x_no]) > length:
			for a in range(len(result[x_no])-length):
				excel.insert_y_line("", y1 + length)
			length= len(result[x_no])
		for y_no in range(len(result[x_no])):
			excel.write_cell_value(sheet_name, [x1+x_no, y1 + y_no+1], result[x_no][y_no])
