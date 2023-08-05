#  -*- coding: utf-8 -*-
import halmoney_pcell

#전체가 빈 가로열 삭제 
#두개의 시트에서 기준시트와 똑같은 열로 다른 시트를 옮기는것이름으로

#1. 현재의 시트 이름을 알아온다
#2. 옮길 시트이름을 얻는다
#3. 기준시트의 사용된영역중 첫번째 열의 모든 내용을 읽어온다
#4. 옮길시트의 사용된영역중 첫번째 열의 모든 내용을 읽어온다
#5.. 두개를 비교해서 몇번째로 이동을 할것인지 새로운 기준시트의 첫번째 열의 모든 내용을 읽어와서 하나씩 비교를 한다

import pyezxl
excel = pyezxl.pyezxl("activeworkbook")

sheet_name_1 = excel.read_activesheet_name()
sheet_name_2=excel.read_messagebox_value()

var_1 = excel.read_range_usedrange(sheet_name_1)[2]
var_2 = excel.read_range_usedrange(sheet_name_2)[2]
sheet_1_end_num = excel.change_address_type(var_1)[1][2]
sheet_2_end_num = excel.change_address_type(var_1)[1][2]

for y1 in range(1, sheet_1_end_num+1):
	var_3 = excel.read_cell_value(sheet_name_1,[1,y1])
	var_5=0
	for y2 in range(1, sheet_2_end_num):
		var_4 = excel.read_cell_value(sheet_name_2,[1,y2])
		if var_3==var_4 and var_5==0:
			excel.insert_range_sero(sheet_name_2, y1)
			excel.copy_range_sero(sheet_name_2, sheet_name_2, y2+1, y1)
			excel.delete_range_sero(sheet_name_2, y2+1)
			var_5=1
	if var_5==0:
		excel.insert_range_sero(sheet_name_2, y1)
		sheet_2_end_num=sheet_2_end_num+1
		

