#  -*- coding: utf-8 -*-

import pyezxl
import re
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

#괄호안의 모든 글자를 괄호를 포함하여 삭제하는것
input = excel.read_messagebox_value("Please input specific char : ex) a, b")
input_new = input.split(",")
#re_basic = "\\"+str(input_new[0]) + "[\^" + str(input_new[0]) +"]*\\" + str(input_new[1])

input_new[0] = str(input_new[0]).strip()
input_new[1] = str(input_new[1]).strip()

special_char = ".^$*+?{}[]\|()"
#특수문자는 역슬래시를 붙이도록
if input_new[0] in special_char : input_new[0]= "\\" + input_new[0]
if input_new[1] in special_char: input_new[1]= "\\" + input_new[1]

re_basic = str(input_new[0]) + ".*" + str(input_new[1])

excel.insert_y_line(sheet_name, y1 + 1)
for x in range(x1, x2+1):
	for y in range(y1, y2+1):
		cell_value = str(excel.read_cell_value(sheet_name,[x, y]))
		result_list = re.findall(re_basic, cell_value)
#		print("새로운값 ==>", new_value)
		if result_list == None or result_list == []:
			pass
		else:
			print("result_list ==>", result_list)
			excel.write_cell_value(sheet_name,[x, y+1], result_list[0])
