#  -*- coding: utf-8 -*-

import pyezxl
import random

excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

# 선택한 영역에 불규칙한 난수 발생하기
# 난수는 선택한 영역에서 하나씩만 나오며
# 영역이 더 크면, 다시 난수를 발생시켜서 추가로 입력한다
input_data = excel.read_messagebox_value("1~100까지 난수 지정시 입력예 : 1,100")
no_start, no_end = input_data.split(",")
no_start = int(no_start.strip())
no_end = int(no_end.strip())
basic_data= list(range(no_start,no_end+1))
random.shuffle(basic_data)
temp_no = 0

for x in range(x1, x2+1):
	for y in range(y1, y2+1):
		excel.write_cell_value("", [x, y], basic_data[temp_no])
		if temp_no >= no_end - no_start:
			random.shuffle(basic_data)
			temp_no=0
		else:
			temp_no = temp_no + 1
