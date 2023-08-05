#  -*- coding: cp949 -*-

import pyezxl
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

# 바꾸기
# 한번에 여러단어 바꾸기
# 이것은 메세지로 입력받기는 어려워 실제 코드에 바꿀 문자들을 입력바랍니다

words=[
["가나","다라"],
["짜장면","자장면"],
["효꽈","효과"],
]

for x in range(x1, x2+1):
	for y in range(y1, y2+1):
		cell_value = str(excel.read_cell_value(sheet_name,[x, y]))
		for one_list in words:
			cell_value = cell_value.replace(one_list[0], one_list[1])
		excel.write_cell_value(sheet_name,[x, y+1], cell_value)