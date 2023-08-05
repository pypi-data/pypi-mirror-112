#  -*- coding: utf-8 -*-

# 선택한 영역의 각셀에 아래의 글자가 모두 들어있는 셀에 초록색으로 배는경색 칠하기
# 1. 원하자료를 inputbox를 이용하여,를 사용하여 받는다					
# 2. split함수를 이용하여 리스트로 만들어					
# 3. 전부 만족한것을 for문으로 만들어 확인한후 색칠을 한다

import pyezxl
import re

excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

bbb = excel.read_messagebox_value("Please input text : in, to, his, with")


basic_list=[]
for one_data in bbb.split(","):
	basic_list.append(one_data.strip())
total_no = len(basic_list)

for x in range(x1, x2 + 1):
	for y in range(y1, y2 + 1):
		cell_value = str(excel.read_cell_value(sheet_name, [x, y]))
		temp_int = 0
		for one_word in basic_list:
			if re.match('(.*)' + one_word + '(.*)', cell_value):
				temp_int = temp_int + 1
		if temp_int == total_no:
			excel.set_cell_color(sheet_name, [x, y], 4)