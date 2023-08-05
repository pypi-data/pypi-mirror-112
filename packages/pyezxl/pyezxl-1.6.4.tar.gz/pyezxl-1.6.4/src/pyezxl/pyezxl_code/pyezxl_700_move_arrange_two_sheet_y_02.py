#  -*- coding: utf-8 -*-

# 두개의 시트에서 하나를 기준으로 다른 하나의 시트 내용을 정렬하는것
# 첫번째 시트의 제일 윗줄을 기준으로 두번째 시트를 정렬 하는것
import pyezxl
excel = pyezxl.pyezxl("")

input_list=[]

# 기준시트와 옮길시트의 이름을 갖고온다
input_data = excel.read_messagebox_value("Please input specific char : ex) sheet_a, sheet_b")
sheet_names = input_data.split(",")

#sheet_names=["aaa", "bbb"]

# 사용한 범위를 갖고온다
range_1 = excel.read_usedrange_address(sheet_names[0])
range_2 = excel.read_usedrange_address(sheet_names[1])

no_title2 =range_2[2]

# 기준 시트의 제목을 읽어와서 저장한다
title_1 = excel.read_range_value(sheet_names[0], [1, range_1[1], 1, range_1[3]])
title_1_list=[]
for no in range(1, len(title_1[0])+1):
	title_1_list.append([no, title_1[0][no-1]])


# 하나씩 옮길시트의 값을 읽어와서 비교한후 맞게 정렬한다
for y1 in range(len(title_1_list)):
	found = 0
	basic_title = title_1_list[y1][1]
	print("기준자료 ==>", basic_title)
	# 기준자료의 제목이 비어잇으면 새로이 한칸을 추가한다
	if basic_title == None or basic_title == "":
		excel.insert_y_line(sheet_names[1], y1 + 1)
		no_title2 = no_title2 +1
	else:
		#만약 기준시트의 제목보다 더 넘어가면 그냥 넘긴다
		if y1 > no_title2:
			pass
		else:
			for y2 in range(y1, no_title2+1):
				move_title = excel.read_cell_value(sheet_names[1], [1, y2+1])
				if found == 0 and move_title == basic_title:
					print("발견자료 ==>", move_title)
					found = 1
					if y1 == y2:
						pass
					else:
						excel.move_y_line(sheet_names[1], sheet_names[1], y2 + 1, y1 + 1)

			if found == 0:
				# 빈칸을 하나 넣는다
				excel.insert_y_line(sheet_names[1], y1 + 1)
