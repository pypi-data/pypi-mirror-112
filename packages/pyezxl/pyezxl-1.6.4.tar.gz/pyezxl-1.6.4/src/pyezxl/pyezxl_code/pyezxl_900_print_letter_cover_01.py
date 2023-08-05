#  -*- coding: utf-8 -*-

# 봉투인쇄
import pyezxl

excel = pyezxl.pyezxl("")

#기본적인 자료 설정
data_from = [["sheet1",[1,2]],["sheet1",[1,4]], ["sheet1",[1,6]],["sheet1",[1,8]]]
data_to = [["sheet2",[1,2]],["sheet2",[2,2]], ["sheet2",[3,2]],["sheet2",[2,3]]]

no_start = 1
no_end = 200
step = 5


# 실행되는 구간
for no in range(no_start, no_end):
	for one in range(len(data_from)):
		value = excel.read_cell_value(data_from[one][0], data_from[one][1])
		excel.write_cell_value(data_to[one][0], [data_to[one][1][0]+(step*no), data_to[one][1][1]] , value)
