#  -*- coding: utf-8 -*-

import pyezxl
import numpy
excel = pyezxl.pyezxl("activeworkbook")
"""
선택한 영역의 값의 행렬을 바꿔서 새로운 시트를 만들어 [1,1]에 쓰기
"""

address_select = excel.read_range_select()
values_d = excel.read_range_value("",address_select)

#튜플로 되어있는 값을 리스트로 바꾸기
values_l=[]
for one_data in values_d:
	values_l.append(list(one_data))

#리스트의 행과 열을 바꾸기
values_l = numpy.transpose(values_d)
print(values_l)

excel.insert_workbook_sheet()
excel.write_range_list("", [1,1], values_l)




