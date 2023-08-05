#  -*- coding: utf-8 -*-

#자주 사용하는 형식변환을 만들어 놓는것이다
#링크없애고
#폰트크기 10
#폰트컬러는 검정색
#폰트는 Courier New


#한글폰트는 현재 않됨 확인해야함

import pyezxl
excel = pyezxl.pyezxl("activeworkbook")
sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()
select_range = [x1, y1, x2, y2]
excel.delete_range_link("", select_range)
excel.set_range_fontsize("", select_range, 10)
excel.set_range_font("", select_range, "Courier New")
excel.set_range_fontcolor("", select_range, 1)