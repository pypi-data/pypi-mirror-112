# -*- coding: utf-8 -*-

#입력받은 시간을 초로 만들어 주는것
import re

input_data_1 = "14:06:23"

re_compile = re.compile("\d+")
result = re_compile.findall(input_data_1)
total_sec =int(result[0])*3600 + int(result[1])*60 + int(result[2])

print(total_sec)


import pyezxl

# 영역의 이름을 짖고
# 모든 이름 돌려 받기
excel = pyezxl.pyezxl("")
me = excel.change_time_sec("14:06:23")
print(me)



#입력받은 초를 시간으로 만들어 주는것
import re

input_data_1 = 50783

step_1 = divmod(input_data_1,60)
step_2 = divmod(step_1[0],60)
final_result = [step_2[0], step_2[1], step_1[1]]
print(final_result)

me = excel.change_sec_time(50783)
print(me)
