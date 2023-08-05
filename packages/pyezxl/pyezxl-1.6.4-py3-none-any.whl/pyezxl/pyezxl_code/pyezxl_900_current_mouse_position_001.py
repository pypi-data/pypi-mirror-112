#  -*- coding: utf-8 -*-

#위치찾기 : 현재 마우스의 위치를 돌려준다

import pyautogui
import pyezxl

position = pyautogui.position()
output_text = "x좌표 : " + str(position.x) + ", y좌표 : " + str(position.y)

excel = pyezxl.pyezxl("activeworkbook")
excel.show_messagebox_value(output_text)

