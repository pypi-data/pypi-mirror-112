#  -*- coding: utf-8 -*-

"""
선택한 영역중 여러부분이 같을 때 그 열을 삭제하는것
입력값 : 1,3,4 (이 3개의 자료가 모두 같은것만 삭제하기)

코드 : 1과 3과 4의 값을 모두 특수문자를 사용하여 연결한후 이것을 사전의 키로 만들어서
      비교하여 선택한다
	  각개개는 틀리지만 합쳤을때 같아지는 형태가 있을수 있어 특수문자를 포함한다
	  예 : 123, 45 과 12, 345
"""
import pyezxl
import time
excel = pyezxl.pyezxl("activeworkbook")
rng_select = excel.read_select_address()
[x1, y1, x2, y2] = excel.read_select_address()

input_data = excel.read_messagebox_value("선택한 영역중 같은 값이 있다면 그 열을 삭제, 예) 1,3,4")
input_list = input_data.split(",")

data_dic={}
del_no = 0

for x in range(x1, x2+1):
	new_x= x - del_no
	one_data =""
	print (x, new_x)
	for a in input_list:
		new_y = y1 + int(a) -1
		one_data = one_data + str(excel.read_cell_value("", [new_x, new_y])) + "#!$@"
	if one_data in data_dic.keys():
		excel.delete_x_line("", new_x)
		del_no=del_no+1
		data_dic[one_data] = data_dic[one_data] + 1
	else:
		data_dic[one_data] = 1




