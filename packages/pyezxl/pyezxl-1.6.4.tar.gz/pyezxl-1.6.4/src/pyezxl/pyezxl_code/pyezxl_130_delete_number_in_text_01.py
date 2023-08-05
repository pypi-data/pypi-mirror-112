# -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl("")
sheet_name = excel.read_activesheet_name()
select_area = excel.read_select_address()
[x1, y1, x2, y2] = select_area

color_dic = excel.ezcolor()
color_list = excel.ezcolor_list()
line_dic = excel.ezline()
#ezre = excel.ezre("입력할자료")

input_text = excel.read_messagebox_value("입력형태 : 바꾸고싶은단어 or 정규식, 바꿀단어")
input_data = input_text.split(",")
print(input_data)
#------------------------------------여기까지 기본자료를 불러오는것이다

import re

for x in range(x1, x2+1):
	for y in range(y1, y2+1):
		cell_value = excel.read_cell_value(sheet_name,[x, y])
		#여기까지 코드가 션택한 각 셀의 값을 갖고오는 것이다
		# 가지고온 값을 변형한후 다시 원위치에 놓을것인지 아니면 다른 위치에 넣을것인지는 설정이 필요
		re_result_2 = re.sub(input_data[0], input_data[1], cell_value)
		print(re_result_2)

