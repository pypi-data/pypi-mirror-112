#  -*- coding: utf-8 -*-

import pyezxl
excel = pyezxl.pyezxl("activeworkbook")
activesheet_name = excel.read_activesheet_name()

excel.write_cell_value("", [1,1], "SuJin")

#이것은 사용자 개발용 코드를 위한 테스트 용도입니다
#개발자의 이름_사용자용 분류번호(3자리)_설명_revision 번호.py (sujin_101_write_cell_value_001.py)
