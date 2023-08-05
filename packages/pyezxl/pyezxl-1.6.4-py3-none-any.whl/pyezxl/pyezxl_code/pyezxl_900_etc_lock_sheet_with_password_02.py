#  -*- coding: utf-8 -*-

import pyezxl
import itertools
import time
# 암호걸어 놓은 시트 풀기
excel = pyezxl.pyezxl("")
sheet_name = excel.read_activesheet_name()

#암호를 처음부터 하나하나씩 넣어가면서 비교검색한다
# 이것은 샘플용으로 시간이 많이 걸리지 않도록 숫자만하였으며 4개 단위의 묶음으로 하였다
source_letter = "1234567890"
repeat_no = 4

print(time.strftime('%c', time.localtime(time.time())))

# itertools.product는 문자열을 원하는 형태의 묶음으로 만들어 주는 모듈이다
# 아래의 에제와 같이 10개의 숫자중 4개씩만 대입을 전부다해 보면 약 30분의 시간이 걸린다
# 그러니 일반적인 컴퓨터로 8글자정도에 알파벳과 특수문자가 들어가 있다면 시간은 상상이상으로 걸리니
# 감안하시고 적용하시기를 바랍니다

count=0

time_start = excel.read_time_now()
for a in itertools.product(source_letter, repeat=repeat_no):
	print (a)
	count +=1
	print(count)
	temp_pwd = ("".join(map(str,a)))
	try:
		excel.set_sheet_unlock(sheet_name, temp_pwd)
		print("확인함==>", a)
	except:
		pass
	else:
		print("password is ==>", temp_pwd)
		break
print(time_start)
print (excel.read_time_now())
print(count)
