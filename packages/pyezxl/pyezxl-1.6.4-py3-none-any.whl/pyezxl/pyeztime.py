# -*- coding: utf-8 -*-

import time
import string

class eztime:
	def __init__(self):
		self.web_site = "www.halmoney.com"
		pass

	def change_sec_time(self, input_data=""):
		# input_data = 123456
		# 입력받은 초를 시간으로 바꾸는 것
		step_1 = divmod(int(input_data), 60)
		step_2 = divmod(step_1[0], 60)
		final_result = [step_2[0], step_2[1], step_1[1]]
		return final_result

	def change_time_sec(self, input_data=""):
		# input_data = "14:06:23"
		# 입력받은 시간을 모두 초로 바꾸는것
		re_compile = re.compile("\d+")
		result = re_compile.findall(input_data)
		total_sec = int(result[0]) * 3600 + int(result[1]) * 60 + int(result[2])
		return total_sec

	def read_time_day(self, time_char=time.localtime(time.time())):
		#일 -----> ['05', '095']
		return [time.strftime('%d',time_char),time.strftime('%j',time_char)]

	def read_time_hour(self, time_char=time.localtime(time.time())):
		#시 -----> ['10', '22', 'PM']
		return [time.strftime('%I',time_char),time.strftime('%H',time_char),time.strftime('%P',time_char)]

	def read_time_minute(self, time_char=time.localtime(time.time())):
		#분 -----> ['07']
		return [time.strftime('%M',time_char)]

	def read_time_month(self, time_char=time.localtime(time.time())):
		#월 -----> ['04', 'Apr', 'April']
		return [time.strftime('%m',time_char),time.strftime('%b',time_char),time.strftime('%B', time_char)]

	def read_time_second(self, time_char=time.localtime(time.time())):
		#초 -----> ['48']
		return [time.strftime('%S',time_char)]

	def read_time_today(self, time_char=time.localtime(time.time())):
		#종합 -----> ['2002-04-05', '04/05/02', '22:07:48', '04/05/02 22:07:48']
		aaa = string.split(time.strftime('%c',time_char))
		total_dash = time.strftime('%Y', time_char)+"-"+time.strftime('%m',time_char)+"-"+time.strftime('%d',time_char)
		return [total_dash, aaa[0], aaa[1], time.strftime('%c',time_char)]

	def read_time_yearweek(self, time_char=time.localtime(time.time())):
		#주 -----> ['5', '13', 'Fri', 'Friday']
		return [time.strftime('%w',time_char),time.strftime('%W',time_char),time.strftime('%a',time_char),time.strftime('%A',time_char)]

	def read_time_week(self, time_char=time.localtime(time.time())):
		#주 -----> ['5', '13', 'Fri', 'Friday']
		return [time.strftime('%w',time_char),time.strftime('%W',time_char),time.strftime('%a',time_char),time.strftime('%A',time_char)]

	def read_time_year(self, time_char=time.localtime(time.time())):
		#년 -----> ['02', '2002']
		return [time.strftime('%y', time_char), time.strftime('%Y', time_char)]

