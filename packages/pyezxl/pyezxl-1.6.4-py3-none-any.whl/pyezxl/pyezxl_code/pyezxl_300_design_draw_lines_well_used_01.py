# -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl("")
sheet_name = excel.read_activesheet_name()
select_area = excel.read_select_address()
[x1, y1, x2, y2] = select_area

color_dic = excel.ezcolor() #색깔에 대한것을 pink++의 형태로 사용
color_list = excel.ezcolor_list() #색깔에 대한것을 pink[0][0]의 형태로 사용
line_dic = excel.ezline()
#ezre = excel.ezre("입력할자료")

#input_text = excel.read_messagebox_value("입력형태 : 바꾸고싶은단어 or 정규식, 바꿀단어")
#input_data = input_text.split(",")
#print(input_data)
#------------------------------------여기까지 기본자료를 불러오는것이다


# 내가 자주사용하는 형태의 라인
# [선의위치, 라인스타일, 굵기, 색깔]
line_list_head = [
	 [line_dic["left"], line_dic["basic"], line_dic["t2"], color_dic["black"]],
	 [line_dic["top"], line_dic["basic"], line_dic["t2"], color_dic["black"]],
	 [line_dic["right"], line_dic["basic"], line_dic["t2"], color_dic["black"]],
	 [line_dic["bottom"], line_dic["basic"], line_dic["t2"], color_dic["black"]],
	 [line_dic["inside-h"], line_dic["basic"], line_dic["t1"], color_dic["black"]],
	 [line_dic["inside-v"], line_dic["basic"], line_dic["t1"], color_dic["black"]],
]

line_list_body = [
	 [line_dic["left"], line_dic["basic"], line_dic["t2"], color_dic["black"]],
	 [line_dic["top"], line_dic["basic"], line_dic["t2"], color_dic["black"]],
	 [line_dic["right"], line_dic["basic"], line_dic["t2"], color_dic["black"]],
	 [line_dic["bottom"], line_dic["="], line_dic["t2"], color_dic["black"]],
	 [line_dic["inside-h"], line_dic["basic"], line_dic["t1"], color_dic["black"]],
	 [line_dic["inside-v"], line_dic["basic"], line_dic["t1"], color_dic["black"]],
]

line_list_tail = [
	 [line_dic["left"], line_dic["basic"], line_dic["t2"], color_dic["black"]],
	 [line_dic["top"], line_dic["basic"], line_dic["t2"], color_dic["black"]],
	 [line_dic["right"], line_dic["basic"], line_dic["t2"], color_dic["black"]],
	 [line_dic["bottom"], line_dic["basic"], line_dic["t2"], color_dic["black"]],
	 [line_dic["inside-h"], line_dic["basic"], line_dic["t1"], color_dic["black"]],
	 [line_dic["inside-v"], line_dic["basic"], line_dic["t1"], color_dic["black"]],
]

print(line_list_head)
range_head = [x1, y1, x1, y2]
range_body = [x1+1, y1, x2-1, y2]
range_tail = [x2, y1, x2, y2]

for one in line_list_head:
	excel.set_range_line("", range_head, one)

for one in line_list_body:
	excel.set_range_line("", range_body, one)

for one in line_list_tail:
	excel.set_range_line("", range_tail, one)
