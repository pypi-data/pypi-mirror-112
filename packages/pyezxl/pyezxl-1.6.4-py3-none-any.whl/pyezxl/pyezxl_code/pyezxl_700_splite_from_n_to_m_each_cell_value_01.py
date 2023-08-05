#  -*- coding: utf-8 -*-
import pyezxl

# 영역에서 각 셀의 일정부분의 자료만 갖고고기
# 시작점의 위치를 설정하세요
# 시작점에서부터 몇개를 읽어올지를 설정하세요

#선택된영역의 자료를 갖고옵니다
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

input = excel.read_messagebox_value("from 1 to 6 : ex) 1, 6")
input_new = input.split(",")

start = int(str(input_new[0]).strip())
end = int(str(input_new[1]).strip())

for x in range(x1, x2+1):
	for y in range(y1, y2+1):
		cell_value = str(excel.read_cell_value(sheet_name,[x, y]))
		print (cell_value)
		temp = cell_value[start:end]
		excel.write_cell_value(sheet_name, [x, y + 1], temp)
