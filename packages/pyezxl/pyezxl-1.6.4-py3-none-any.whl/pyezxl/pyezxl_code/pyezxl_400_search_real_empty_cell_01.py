#  -*- coding: utf-8 -*-				

# 빈셀처럼 보이는데 space문자가 들어가 있는것 찾기				
# 1. 선택한 영역의 셀을 하나씩 읽어와서 re모듈을 이용해서 공백만 있는지 확인한다				

import pyezxl

excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

import re

for x in range(x1, x2 + 1):
	for y in range(y1, y2 + 1):
		cell_value = excel.read_cell_value("", [x, y])
		com = re.compile("^\s+")
		if cell_value != None:
			if com.search(cell_value):
				excel.set_cell_color("", [x, y], 4)
