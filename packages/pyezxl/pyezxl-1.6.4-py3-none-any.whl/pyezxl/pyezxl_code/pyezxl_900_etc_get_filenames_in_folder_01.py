#  -*- coding: utf-8 -*-

import pyezxl
import os
import sys


excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()

"""
디렉토리안에 있는 화일들을 갖고온다
새로운 시트를 만들어서 그곳에 값을 입력한다
"""
input_data=excel.read_messagebox_value("if you want Full Code Names, Type : pyezxl")
if input_data =="pyezxl":
	path_head = os.path.dirname(sys.executable)
	path_body ="\Lib\site-packages\pyezxl\pyezxl_code\\"
elif len(input_data) > 3:
	path_head = input_data
	path_body=""
else:
	path_head = 'C:\\'
	path_body=""

file_names = os.listdir(path_head + path_body)
print(len(file_names))
excel.insert_workbook_sheet()
for one_no in range(len(file_names)):
	excel.write_cell_value("", [one_no+1,1], file_names[one_no])
