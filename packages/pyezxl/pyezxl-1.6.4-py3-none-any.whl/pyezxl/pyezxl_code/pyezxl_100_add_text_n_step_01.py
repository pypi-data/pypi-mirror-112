#  -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

# 선택한 셀에서 n번째마다 셀에 값을 넣기
# 현재 셀이 있는 곳부터 입력을 시작하면서 계산함
input_text=excel.read_messagebox_value("from 1 to 500, 3 steps, text is value => ex) 1, 500, 3, value")
basic_list=[]
for one_data in input_text.split(","):
	basic_list.append(one_data.strip())

for x in range(int(basic_list[0]), int(basic_list[1])+1, int(basic_list[2])):
	for y in range(y1, y2+1):
		excel.write_cell_value(sheet_name,[x, y],basic_list[3])
