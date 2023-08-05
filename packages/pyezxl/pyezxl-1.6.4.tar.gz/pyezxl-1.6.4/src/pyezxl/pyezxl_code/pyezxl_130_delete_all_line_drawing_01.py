#  -*- coding: utf-8 -*-

#모든 선의 줄을 없애는것
# 어디에선가 갖고온 자료를 복사해서 넣으면 휜색선으로되서
# 기보선의 형태가 없어지는것이 보기 흉해서
# 흰색의 배경색만 없애기

import pyezxl
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
xyxy = excel.read_select_address()
[x1, y1, x2, y2] = xyxy

excel.delete_range_line("", xyxy)