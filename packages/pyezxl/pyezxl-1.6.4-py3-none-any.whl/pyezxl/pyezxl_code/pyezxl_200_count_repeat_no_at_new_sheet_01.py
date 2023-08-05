#  -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

"""
선택한 영역의 반복되는 갯수를 구한다
1. 선택한 영역에서 값을 읽어온다
2. 사전으로 읽어온 값을 넣는다
3. 열을 2개를 추가해서 하나는 값을 다른하나는 반복된 숫자를 넣는다
"""

all_data=excel.read_range_value("", [x1, y1, x2, y2])
py_dic={}
#읽어온 값을 하나씩 대입한다

for line_data in all_data:
	for one_data in line_data:
		#키가와 값을 확인
		if one_data in py_dic:
			py_dic[one_data]=py_dic[one_data] +1
		else:
			py_dic[one_data] = 1

print(py_dic)
excel.insert_y_line(sheet_name, 1)
excel.insert_y_line(sheet_name, 1)
dic_list = list(py_dic.keys())
for no in range(len(dic_list)):
	excel.write_cell_value("", [no+1,1], dic_list[no])
	excel.write_cell_value("", [no+1,2], py_dic[dic_list[no]])
