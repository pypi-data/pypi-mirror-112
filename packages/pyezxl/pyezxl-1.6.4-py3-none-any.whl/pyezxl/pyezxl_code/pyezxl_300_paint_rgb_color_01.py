#  -*- coding: utf-8 -*-

import pyezxl

excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()
my_range = [x1, y1, x2, y2]

# RGB값을 색칠하는 방법
input_data=excel.read_messagebox_value("Type : 234, 234, 234")
red_no, green_no, blue_no = input_data.split(",")
rgb_list = [int(red_no), int(green_no), int(blue_no)]
excel.set_range_rgbcolor(sheet_name, my_range, rgb_list)