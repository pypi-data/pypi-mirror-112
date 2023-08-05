# -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl("")
sheet_name = excel.read_activesheet_name()
select_area = excel.read_select_address()
[x1, y1, x2, y2] = select_area

color_dic = excel.enum_color_dic()
color_list = excel.enum_color_list()
line_dic = excel.enum_cell_line()

#------------------------------------여기까지 기본자료를 불러오는것이다

range_names = excel.delete_workbook_rangenames()
print(range_names)