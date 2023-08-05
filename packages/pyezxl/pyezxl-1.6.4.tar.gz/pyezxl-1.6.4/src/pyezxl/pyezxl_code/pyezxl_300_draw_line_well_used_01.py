#  -*- coding: utf-8 -*-


import pyezxl
excel = pyezxl.pyezxl("")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

# 자주 사용하는 테두리선을 지정해 놓고 사용을 하는것
# 안쪽의 선들지정
# [선의위치, 라인스타일, 굵기, 색깔]
# 선의위치 (5-대각선 오른쪽, 6-왼쪽대각선, 7:왼쪽, 8;위쪽, 9:아래쪽, 10:오른쪽, 11:안쪽세로, 12:안쪽가로)
line_left = 7
line_top=8
line_right=10
line_bottom=9
line_inner_col=11
line_inner_row=12
# 라인스타일 (1-실선, 2-점선, 3-가는점선, 6-굵은실선,
line_style_line = 1
line_style_dot = -4118
line_style_dashdot = 4
line_style_dashdotdot = 5
line_style_dash = -4115
line_style_thick_dot = 6
line_style_double = -4119
line_style_none = -4142
line_style_slantdashdot = 13

# 굵기 (0-이중, 1-얇게, 2-굵게)
line_weight_hairline = 1
line_weight_medium = -4138
line_weight_thin = 2
line_weight_thick = 4
# 색깔 (0-검정, 1-검정, 3-빨강),
line_colorindex_black=1
line_colorindex_white=2
line_colorindex_red=3
line_colorindex_green=4
line_colorindex_blue=5
line_colorindex_yellow=6
line_colorindex_brown=9
line_colorindex_gray=17

line_list_head = [[line_left, line_style_line, line_weight_medium, line_colorindex_black],
				 [line_top, line_style_line, line_weight_medium, line_colorindex_black],
				 [line_right, line_style_line, line_weight_medium, line_colorindex_black],
			    [line_inner_col, line_style_line, line_weight_hairline, line_colorindex_black]]

line_list_body = [[line_left, line_style_line, line_weight_medium, line_colorindex_black],
			 [line_top, line_style_line, line_weight_hairline, line_colorindex_black],
			 [line_right, line_style_line, line_weight_medium, line_colorindex_black],
			 [line_bottom, line_style_line, line_weight_hairline, line_colorindex_black],
			 [line_inner_row, line_style_dot, line_weight_hairline, line_colorindex_red],
			 [line_inner_col, line_style_dot, line_weight_hairline, line_colorindex_blue]]

line_list_tail = [[line_left, line_style_line, line_weight_medium, line_colorindex_black],
			 [line_top, line_style_line, line_weight_hairline, line_colorindex_black],
			 [line_right, line_style_line, line_weight_medium, line_colorindex_black],
			 [line_bottom, line_style_line, line_weight_medium, line_colorindex_black],
			[line_inner_col, line_style_line, line_weight_hairline, line_colorindex_black]]



range_head = [x1, y1, x1, y2]
range_body = [x1+1, y1, x2-1, y2]
range_tail = [x2, y1, x2, y2]


for one in line_list_head:
	excel.set_range_line("", range_head, line_list_head)

for one in line_list_head:
	excel.set_range_line("", range_body, line_list_body)

for one in line_list_head:
	excel.set_range_line("", range_tail, line_list_tail)
