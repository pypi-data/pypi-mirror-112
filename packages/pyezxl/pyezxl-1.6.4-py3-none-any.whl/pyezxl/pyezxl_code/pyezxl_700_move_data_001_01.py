#  -*- coding: utf-8 -*-

# 어지선가 갖고온 자료중 제목과 내용이연속적으로 된 자료중 제목을 왼쪽이나 오른쪽의 자료에다가 옮길려고 한다
# 1. 원하는 영역을 선택한다
# 2. 제목 부분이나 옮기고 싶은것이 몇번째인지 알아낸다
# 3. 현재 옮기고 싶은 자료의 위치를 기준으로 옮길곳을 +-로 나타낸다
# 입력값, 4-12 : 매 4번째의 값을 왼쪽으로 1칸 아래쪽으로 2칸의 위치에 입력한다


import pyezxl

excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()
select_range = [x1, y1, x2, y2]

bbb = excel.read_messagebox_value("Please input : step, down[+], right[+] : 4,1,2")
aaa = bbb.split(",")

for y in range(y1, y2 + 1):
	temp_int = 1
	for x in range(x1, x2 + 1):
		if temp_int % int(aaa[0]) == 0:
			cell_value = str(excel.read_cell_value(sheet_name, [x, y]))
			excel.write_cell_value(sheet_name, [x, y], "")
			excel.write_cell_value(sheet_name, [x + int(aaa[1]), y + int(aaa[2])], cell_value)
		temp_int = temp_int + 1