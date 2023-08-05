#  -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl('activeworkbook')

#선택한 영역에서 각 세로행의 자료가 입삭제할것들을 입력받은 빈칸이상이 있으면 당겨오는 것이다
#이것은 여러곳에서 갖고온 자료들중 삭제한후에 값들을 당겨서 하기에 손이 많이 가는것을 코드로 만든 것이다

[x1, y1, x2, y2] = excel.read_range_select()
#0칸일때 빈 공간이 없는것이다
step_line = int(excel.read_messagebox_value("0 : 빈칸이 없는것입니다"))+1

for y in range(y1, y2 + 1):
	temp_data=[]
	flag = 0
	for x in range(x1, x2 + 1):
		temp_value = excel.read_cell_value("", [x,y])
		print(x, "번째 ====>", temp_value)
		if temp_value == "" or temp_value == None:
			flag = flag +1
		else:
			flag =0
		if flag >= step_line:
				pass
		else:
				temp_data.append([temp_value])
				excel.write_cell_value("", [x,y], "")
	print(temp_data)
	excel.dump_range_value("", [1,y], temp_data)
