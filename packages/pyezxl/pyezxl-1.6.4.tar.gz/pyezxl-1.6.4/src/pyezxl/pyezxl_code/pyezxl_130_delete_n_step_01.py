#  -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
rng_select = excel.read_select_address()
rng_used = excel.read_usedrange_address()
x1, y1, x2, y2 = excel.intersect_range1_range2(rng_select, rng_used)

#삭제 : 선택자료중 n번째 가로열의 자료를 삭제하는것

step_no=excel.read_messagebox_value("몇번째의 모든 가로값을 지울까요?")

for x in range(x1, x2 + 1):
	for y in range(y1, y2+1):
		if (x-x1+1)%int(step_no)==0:
			excel.write_cell_value(sheet_name, [x, y], "")



