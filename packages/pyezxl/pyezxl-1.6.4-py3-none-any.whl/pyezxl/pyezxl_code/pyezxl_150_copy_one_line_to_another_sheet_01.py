#  -*- coding: utf-8 -*-

# 다른시트에 현재 위치한 한줄을 특정 위치에 복사하기
# 이것은 사용자가 코드를 넣어서 사용하기위한 자료인 것이다

import pyezxl
excel = pyezxl.pyezxl("")
sheet_name = excel.read_activesheet_name()
activecell = excel.read_activecell_range()

# 자료를 옮길 시트가 기존에 있는지 확인한후
# 없다면 만드는 것이다
paste_sheet_name = "pyezxl_result_sheet"
all_sheet_name = excel.read_sheet_name()
excel.check_sheet_name(paste_sheet_name)

# 자료를 복사하는 코드
excel.copy_x_line(sheet_name, paste_sheet_name, activecell[0], 1)
