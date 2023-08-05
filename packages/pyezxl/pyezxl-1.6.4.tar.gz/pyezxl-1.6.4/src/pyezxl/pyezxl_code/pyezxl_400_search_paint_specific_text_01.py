#  -*- coding: utf-8 -*-
import pyezxl
excel = pyezxl.pyezxl("activeworkbook")

sheet_name = excel.read_activesheet_name()
x1, y1, x2, y2= excel.read_select_address()


#영역 안의 자료를 
selection_range=excel.read_select_address()
datas=list(excel.read_range_value("activesheet",selection_range ))

temp=[]
result=[]
min_value=[]

print (datas)

input_text = excel.read_messagebox_value()

for data_xx in datas:
	temp_list=[]
	temp_num=0
	for data_x in data_xx:
		if str(input_text) in str(data_x) and data_x != None:
			excel.set_range_color(sheet_name, [x1, y1+temp_num, x1, y1+temp_num], 6)
		temp_num= temp_num+1
	x1 = x1+1

