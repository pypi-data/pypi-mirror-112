#  -*- coding: utf-8 -*-

import pyezxl

# 영역의 이름을 짖고
# 모든 이름 돌려 받기
excel = pyezxl.pyezxl("")
activesheet_name = excel.read_activesheet_name()
select_area = excel.read_select_address()
[x1, y1, x2, y2] = select_area


input_text = excel.read_messagebox_value("영역의 이름을 넣어주세요")
print(input_text)


excel.set_range_rangename("", select_area, input_text)
bbb = excel.set_range_rangename()
print(bbb)
