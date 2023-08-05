# -*- coding: utf-8 -*-

import win32com.client
import re
import string
import win32gui
import time

class pyezxl:
    my_web_site = "www.halmoney.com"

    def __init__(self, filename=""):
        # 만약 화일의 경로가 있으면 그 화일을 열도록 한다
        self.xlApp = win32com.client.dynamic.Dispatch('Excel.Application')
        self.xlApp.Visible = 1

        if filename != None or filename != "":
            self.filename = filename.lower()

        if self.filename == 'activeworkbook' or self.filename == '':
            # activeworkbook으로 된경우는 현재 활성화된 workbook을 그대로 사용한다
            self.xlBook = self.xlApp.ActiveWorkbook
            if self.xlBook == None:
                # 만약 activework북을 부르면서도 화일이 존재하지 않으면 새로운 workbook을 만드는것이다
                try:
                    self.xlApp.WindowState = -4137
                    self.xlBook = self.xlApp.WorkBooks.Add()
                except:
                    win32gui.MessageBox(0, "There is no Activeworkbook", self.my_web_site, 0)

        elif not (self.filename == 'activeworkbook') and self.filename:
            # 만약 화일이름이 따로 주어지면 그화일을 연다
            try:
                self.xlApp.WindowState = -4137
                self.xlBook = self.xlApp.Workbooks.Open(self.filename)
            except:
                win32gui.MessageBox(0, "Please check file path", self.my_web_site, 0)
        else:
            # 빈것으로 된경우는 새로운 workbook을 하나 열도록 한다
            self.xlApp.WindowState = -4137
            self.xlBook = self.xlApp.WorkBooks.Add()

    def change_char_num(self, input_data):
        # input_data : aa => result : 27, 문자를 숫자로 바꿔주는 것
        if input_data.isalpha():
            input_data = input_data.lower()
            reversed_input_data = ''.join(reversed(input_data))
            temp_result = [ord(letter) - 96 for letter in reversed_input_data]
            result = 0
            for one in range(len(temp_result)):
                result = result + pow(26, one) * temp_result[one]
        else:
            result = input_data
        return int(result)

    def change_list_size(self, xy_list, resize=[1,1]):
        #0으로 표현하면 기존 자료를 그대로 유지한다
        # 리스트의 사이즈를 조정한다
        result = []

        #자료의 x갯수를 요청한것과 비교
        if len(xy_list) < resize[0] or resize[0] == 0:
            pass
        else:
            xy_list = xy_list[:resize[0]]

        #자료의 y갯수를 요청한것과 비교
        for x_list in xy_list:
            if len(x_list) < resize[1] or resize[1] == 0:
                pass
            else:
                x_list = xy_list[:resize[0]]
            result.append(x_list)
        return result

    def change_num_char(self, input_data):
        # input_data : 27 => result : aa, 숫자를 문자로 바꿔주는 것
        base_number = int(input_data)
        result_01 = ''
        result = []
        while base_number > 0:
            div = base_number // 26
            mod = base_number % 26
            if mod == 0:
                mod = 26
                div = div - 1
            base_number = div
            result.append(mod)
        for one_data in result:
            result_01 = string.ascii_lowercase[one_data - 1] + result_01
        return result_01

    def change_rgb_int(self, input_data):
        # rgb인 값을 color에서 인식이 가능한 정수값으로 변경
        result = (int(input_data[2]))*(256**2)+(int(input_data[1]))*256+int(input_data[0])
        return result

    def change_sheet_name(self, sheet_name_0, sheet_name_1):
        # 시트이름 변경
        self.xlBook.Worksheets(sheet_name_0).Name = sheet_name_1

    # [x, y]형태의 자료를 a1의 형태로 변경해 주는것
    def change_xy_a1(self, xy=[3, 4]):
        base_number = int(input_data)
        result_01 = ''
        result = []
        while base_number > 0:
            div = base_number // 26
            mod = base_number % 26
            if mod == 0:
                mod = 26
                div = div - 1
            base_number = div
            result.append(mod)
        for one_data in result:
            result_01 = string.ascii_lowercase[one_data - 1] + result_01
        return result_01

    def change_xylist_addresschar(self, xy_list=[[1, 1], [2, 3], [2, 4]]):
        # [1,1],[2,3] => "a1, b3"로 바꿔주는것
        # 이것은 한번에 같은일을 시킬수있는 방법으로 속도를 올리기 위한 것이다
        result = ""
        for one_data in xy_list:
            y_char = excel.change_num_char(one_data[1])
            result = result + str(y_char[0]) + str(one_data[0]) + ', '
        return result[:-2]

    def check_address_value(self, address=""):
        # 어떠한 형태의 주소값이 오더라도 결과값을 [x1, y1, x2, y2]의 형태로 만들어 주는것
        # input_data : [1,2],[1,1,2,3],[$A$1], [$A$1:$B$2], [$1:$7], [$A:$B], [A1]
        # output_data : [1,2],[1,1,2,3],[1,1], [1,1,2,2], [1,0,7.0], [0,1,0,2], [1,1]
        check_string = re.compile(r"([:$a-zA-Z]+)")
        check_range = re.compile(r"([:]+)")
        check_num = re.compile(r"([0-9]+)")

        result_final = []
        result_final_01 = []

        if address == "":
            address = self.read_select_address()
        elif type(address) != type([]):
            address = [address]

        for one_data in address:
            one_data = str(one_data)
            one_data = one_data.replace('$', '')
            result_temp = []
            result_final_01 = []
            data_type = {"range": "no", "num_only": "no", "string_only": "no"}
            # 어떤 형태의 주소인지 확인한다

            if check_range.findall(one_data):
                data_type["range"] = "yes"
            if check_num.findall(one_data.split(":")[0]):
                data_type["num_only"] = "yes"
            if check_string.findall(one_data.split(":")[0]):
                data_type["string_only"] = "yes"

            if data_type["range"] == "no" and data_type["num_only"] == "yes" and data_type["string_only"] == "no":
                # [1, 2], [1, 1, 2, 3] => 이런형태이므로 그대로 값을 넣어준다
                result_temp.append(one_data)

            if data_type["range"] == "no" and data_type["num_only"] == "no" and data_type["string_only"] == "yes":
                # [$A$1], [A1] => 이런형태
                temp_value = self.split_eng_num(one_data)
                temp_value1 = self.change_char_num(temp_value[0])
                result_temp.append(int(temp_value[1]))
                result_temp.append(int(temp_value1))

            if data_type["range"] == "no" and data_type["num_only"] == "yes" and data_type["string_only"] == "yes":
                # [$A$1], [A1] => 이런형태
                temp_value = self.split_eng_num(one_data)
                temp_value1 = self.change_char_num(temp_value[0])
                result_temp.append(int(temp_value[1]))
                result_temp.append(int(temp_value1))

            if data_type["range"] == "yes" and data_type["num_only"] == "yes" and data_type["string_only"] == "yes":
                # [$A$1:$B$2] => 이런형태
                for data_001 in one_data.split(":"):
                    temp_value = self.split_eng_num(data_001)
                    temp_value1 = self.change_char_num(temp_value[0])
                    result_temp.append(int(temp_value[1]))
                    result_temp.append(int(temp_value1))

            if data_type["range"] == "yes" and data_type["num_only"] == "no" and data_type["string_only"] == "yes":
                # [$A:$B] => 이런형태
                for data_001 in one_data.split(":"):
                    result_temp.append(int(0))
                    temp_value = self.change_char_num(data_001)
                    result_temp.append(int(temp_value))

            if data_type["range"] == "yes" and data_type["num_only"] == "yes" and data_type["string_only"] == "no":
                # [$1:$7] => 이런형태
                aaa = one_data.split(":")
                for data_001 in aaa:
                    result_temp.append(int(data_001))
                    result_temp.append(int(0))

            result_final.extend(result_temp)
        if len(result_final) == 2: result_final_01 = [int(result_final[0]), int(result_final[1]), int(result_final[0]), int(result_final[1])]
        if len(result_final) == 4: result_final_01 = [int(result_final[0]), int(result_final[1]), int(result_final[2]), int(result_final[3])]

        #혹시 입력한 자료가 [1,2,3,4]의 형태가 아닌 [3,4,1,2]로 되어잇을때 정렬을 다시하는것이다
        temp1 = [result_final_01[0], result_final_01[2]]
        temp1.sort()

        temp2 = [result_final_01[1], result_final_01[3]]
        temp2.sort()

        result_final_02 = [temp1[0], temp2[0], temp1[1], temp2[1]]
        return result_final_02

    def check_range_address(self, xyxy=""):
        #비슷하게 추측이 가능한 함수를 하나더 만든 것이다
        return self.check_address_value(xyxy)

    def check_sheet_name(self, sheet_name=""):
        # sheet이름을 확인해서 돌려준다.
        # 아무것도 없으면 현재 활성화된 activesheet를 돌려준다
        # 시트이름으로 확인하여 없다면, 일단 입력받은 시트이름으로 새로운 시트를 만든다
        # read와 check의 의미 차이는 check는 어떤 조건에서 2개이상의 다른 값을 보여줄때이며
        # read는 조건문등의 구문이 없이 단순히 값을 읽어올때 사용한다
        if str(sheet_name).lower() == "activesheet" or sheet_name == "":
            sheet = self.xlApp.ActiveSheet
        elif sheet_name in self.read_sheet_name():
            sheet = self.xlBook.Worksheets(sheet_name)
        else:
            self.insert_workbook_sheet()
            old_sheet_name = self.read_activesheet_name()
            self.change_sheet_name(old_sheet_name, sheet_name)
            sheet = self.xlBook.Worksheets(sheet_name)
        return sheet

    def read_sheet_name(self):
        # 현재 워크북의 모든 시트알아내기
        temp_list = []
        for var_02 in range(1, self.read_sheet_count() + 1):
            temp_list.append(self.xlBook.Worksheets(var_02).Name)
        return temp_list

    def check_x_empty(self, sheet_name, x):
        # 열전체가 빈 것인지 확인해서 돌려준다
        # 전체가 비었을때는 0을 돌려준다
        x_check = self.check_xy_address(x)
        x1 = self.change_char_num(str(x_check[0]))
        sheet = self.check_sheet_name(sheet_name)
        result = self.xlApp.WorksheetFunction.CountA(sheet.Rows(int(x1)).EntireRow)
        return result

    def check_xy_address(self, xy):
        # 입력의 형태 : 3, [3], [2,3], D, [A,D], [D]
        # 출력 : [3,3], [2,3], [4,4,], [1,4]
        # x나 y의 하나를 확인할때 입력을 잘못하는 경우를 방지하기위해 사용
        result = []
        if type([]) == type(xy):
            if len(xy) == 1:
                xy[0] = self.change_char_num(str(xy[0]))
                result = [xy[0], xy[0]]
            if len(xy) == 2:
                xy[0] = self.change_char_num(str(xy[0]))
                xy[1] = self.change_char_num(str(xy[1]))
                result = xy
        else:
            xy = str(xy)
            if re.match('[a-zA-Z0-9]', xy):
                if re.match('[a-zA-Z]', xy):
                    xy = self.change_char_num(xy)
                    result = [xy, xy]
                else:
                    result = [xy, xy]
        return result

    def check_y_empty(self, sheet_name, y):
        # 세로열 전체가 빈 것인지 확인해서 돌려준다
        # 전체가 비었을때는 0을 돌려준다
        y_check = self.check_xy_address(y)
        y1 = self.change_char_num(str(y_check[0]))
        sheet = self.check_sheet_name(sheet_name)
        result = self.xlApp.WorksheetFunction.CountA(sheet.Columns(y1).EntireColumn)
        return result

    def copy_x_line(self, sheet_name_1, sheet_name_2, x0, x1):
        # 세로의 값을 이동시킵니다
        sheet1 = self.check_sheet_name(sheet_name_1)
        sheet2 = self.check_sheet_name(sheet_name_2)

        x0_1, x0_2 = self.check_xy_address(x0)
        x1_1, x1_2 = self.check_xy_address(x1)

        x0_1 = self.change_char_num(x0_1)
        x0_2 = self.change_char_num(x0_2)
        x1_1 = self.change_char_num(x1_1)
        x1_2 = self.change_char_num(x1_2)

        sheet1.Select()
        sheet1.Rows(str(x0_1) + ':' + str(x0_2)).Select()
        sheet1.Rows(str(x0_1) + ':' + str(x0_2)).Copy()
        sheet2.Select()
        sheet2.Rows(str(x1_1) + ':' + str(x1_2)).Select()
        sheet2.Paste()

    def copy_y_line(self, sheet_name_1, sheet_name_2, y0, y1):
        # 세로의 값을 이동시킵니다
        sheet1 = self.check_sheet_name(sheet_name_1)
        sheet2 = self.check_sheet_name(sheet_name_2)

        y0_1, y0_2 = self.check_xy_address(y0)
        y1_1, y1_2 = self.check_xy_address(y1)

        y0_1 = self.change_num_char(y0_1)
        y0_2 = self.change_num_char(y0_2)
        y1_1 = self.change_num_char(y1_1)
        y1_2 = self.change_num_char(y1_2)
        #print(y0_1, y0_2, y1_1, y1_2)

        sheet1.Select()
        sheet1.Columns(str(y0_1) + ':' + str(y0_2)).Select()
        sheet1.Columns(str(y0_1) + ':' + str(y0_2)).Copy()
        sheet2.Select()
        sheet2.Columns(str(y1_1) + ':' + str(y1_2)).Select()
        sheet2.Paste()

    def cut_x_line(self, sheet_name_1, sheet_name_2, x0, x1):
        # 세로의 값을 이동시킵니다
        sheet1 = self.check_sheet_name(sheet_name_1)
        sheet2 = self.check_sheet_name(sheet_name_2)

        x0_1, x0_2 = self.check_xy_address(x0)
        x1_1, x1_2 = self.check_xy_address(x1)

        x0_1 = self.change_char_num(x0_1)
        x0_2 = self.change_char_num(x0_2)
        x1_1 = self.change_char_num(x1_1)
        x1_2 = self.change_char_num(x1_2)

        sheet1.Select()
        sheet1.Rows(str(x0_1) + ':' + str(x0_2)).Select()
        sheet1.Rows(str(x0_1) + ':' + str(x0_2)).Copy()
        sheet2.Select()
        sheet2.Rows(str(x1_1) + ':' + str(x1_2)).Select()
        sheet2.Rows(str(x1_1) + ':' + str(x1_2)).Insert()

        if sheet1 == sheet2:
            if x0_1 <= x1_1:
                sheet1.Rows(str(x0_1) + ':' + str(x0_2)).Delete()
            else:
                new_x0_1 = self.change_num_char(x0_1 + x1_2 - x1_1)
                new_x0_2 = self.change_num_char(x0_2 + x1_2 - x1_1)
                sheet1.Rows(str(new_x0_1) + ':' + str(new_x0_2)).Delete()
        else:
            sheet1.Rows(str(x0_1) + ':' + str(x0_2)).Delete()

    def cut_y_line(self, sheet_name_1, sheet_name_2, y0, y1):
        # 세로의 값을 이동시킵니다
        sheet1 = self.check_sheet_name(sheet_name_1)
        sheet2 = self.check_sheet_name(sheet_name_2)

        y0_1, y0_2 = self.check_xy_address(y0)
        y1_1, y1_2 = self.check_xy_address(y1)

        y0_1 = self.change_num_char(y0_1)
        y0_2 = self.change_num_char(y0_2)
        y1_1 = self.change_num_char(y1_1)
        y1_2 = self.change_num_char(y1_2)

        sheet1.Select()
        sheet1.Columns(str(y0_1) + ':' + str(y0_2)).Select()
        sheet1.Columns(str(y0_1) + ':' + str(y0_2)).Cut()
        sheet2.Select()
        sheet2.Columns(str(y1_1) + ':' + str(y1_2)).Select()
        sheet2.Columns(str(y1_1) + ':' + str(y1_2)).Insert()

    def count_sheet_shape(self, sheet_name=""):
        sheet = self.check_sheet_name(sheet_name)
        return sheet.Shapes.Count

    def delete_cell_memo(self, sheet_name, xy):
        # 메모를 삭제한는 것
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xy)
        sheet.Cells(x1, y1).ClearComments()

    def delete_sheet_shape(self, sheet_name="", name=""):
        sheet = self.check_sheet_name(sheet_name)
        sheet.Shapes(name).Delete()

    def delete_range_color(self, sheet_name, xyxy):
        # 영역의 모든 색을 지운다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Interior.Pattern = -4142
        my_range.Interior.TintAndShade = 0
        my_range.Interior.PatternTintAndShade = 0

    def delete_range_line(self, sheet_name, xyxy):
        # 영역에 선의색을 다 없애는것
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2)).Borders.LineStyle = 0

    def delete_range_linecolor(self, sheet_name, xyxy):
        # 영역에 선의색을 다 없애는것
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = xyxy
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range .Interior.Pattern = 0
        my_range .Interior.PatternTintAndShade = 0

    def delete_range_link(self, sheet_name, xyxy):
        # 영역의 모든 색을 지운다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Hyperlinks.Delete()

    def delete_range_samevalue(self, sheet_name, xyxy):
        # 선택 영역중 2번이상 반복되는 값은 지우는 것이다
        temp_result = []
        select_range = self.read_select_address()
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet = self.check_sheet_name(sheet_name)

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                temp_data = self.read_cell_value(sheet, [x, y])
                if temp_data in temp_result:
                    self.write_cell_value(sheet, [x, y], "")
                else:
                    temp_result.append(temp_data)

    def delete_range_value(self, sheet_name, xyxy):
        # 선택한영역의 모든 값을 지우는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.ClearContents()

    def delete_range_x(self, sheet_name, x):
        # 가로 한줄삭제하기
        # 입력형태는 2, [2,3]의 두가지가 가능하다
        sheet = self.check_sheet_name(sheet_name)
        new_x = self.check_xy_address(x)
        sheet.Rows(str(new_x[0]) + ':' + str(new_x[1])).Delete(-4121)

    def delete_range_xx(self, sheet_name, xx):
        self.delete_range_x(sheet_name, xx)

    def delete_range_y(self, sheet_name, y):
        # 세로 한줄삭제하기
        sheet = self.check_sheet_name(sheet_name)
        new_y = self.check_xy_address(y)
        sheet.Columns(str(new_y[0]) + ':' + str(new_y[1])).Delete()

    def delete_range_yy(self, sheet_name, yy):
        self.delete_range_y(sheet_name, yy)

    def delete_sheet_alldrawing(self, sheet_name=""):
        # 특정 시트안의 그림을 다 지우는 것이다
        sheet = self.check_sheet_name(sheet_name)
        for aa in range(sheet.Shapes.Count, 0, -1):
            # Range를 앞에서부터하니 삭제하자마자 번호가 다시 매겨져서, 뒤에서부터 삭제하니 잘된다
            sheet.Shapes(aa).Delete()
        return

    def delete_sheet_allsharp(self, sheet_name=""):
        # 특정 시트안의 그림을 다 지우는 것이다
        sheet = self.check_sheet_name(sheet_name)
        for aa in range(sheet.Shapes.Count, 0, -1):
            # Range를 앞에서부터하니 삭제하자마자 번호가 다시 매겨져서, 뒤에서부터 삭제하니 잘된다
            sheet.Shapes(aa).Delete()
        return

    def delete_sheet_value(self, sheet_name):
        # 시트의 모든 값을 삭제한다
        sheet = self.check_sheet_name(sheet_name)
        sheet.Cells.ClearContents()

    def delete_workbook_rangename(self, sheet_name, range_name):
        # 입력한 이름을 삭제한다
        # name은 workbook으로 되지만 동일하게 하기위하여 sheet_name을 넣은 것이다
        sheet = self.check_sheet_name(sheet_name)
        result = self.xlBook.Names(range_name).Delete()
        return result

    def delete_range_name(self, sheet_name, range_name):
        self.delete_workbook_rangename(sheet_name, range_name)
        # 예전 코드를 위해 남겨놓음

    def delete_workbook_allrangename(self):
        # 모든 이름을 삭제한다
        names_count = self.xlBook.Names.Count
        print("총 갯수 ==>", names_count)
        result = 0
        if names_count > 0:
            for aaa in range(names_count, 0, -1):
                range_name = self.xlBook.Names(aaa).Name
                print(result, range_name)
                self.xlBook.Names(aaa).Delete()
                result += 1
        print("총 삭제된 갯수 ==>", result)
        return result

    def delete_workbook_sheet(self, sheet_name=""):
        # 시트하나 삭제하기
        sheet = self.check_sheet_name(sheet_name)
        self.xlApp.DisplayAlerts = False
        sheet.Delete()
        self.xlApp.DisplayAlerts = True

    def delete_x_line(self, sheet_name, x):
        # 한줄삭제하기
        self.delete_range_x(sheet_name, x)

    def delete_line_x(self, sheet_name, x):
        # 한줄삭제하기
        self.delete_range_x(sheet_name, x)

    def delete_x_value(self, sheet_name, x):
        # 한줄값만 삭제하기
        sheet = self.check_sheet_name(sheet_name)
        new_x = self.check_xy_address(x)
        sheet.Rows(str(new_x[0]) + ':' + str(new_x[1])).ClearContents()

    def delete_y_line(self, sheet_name, y):
        # 한줄삭제하기
        self.delete_range_y(sheet_name, y)

    def delete_line_y(self, sheet_name, y):
        # 한줄삭제하기
        self.delete_range_y(sheet_name, y)

    def delete_y_value(self, sheet_name, y):
        # 한줄값만 삭제하기
        sheet = self.check_sheet_name(sheet_name)
        new_y = self.check_xy_address(y)
        sheet.Columns(str(new_y[0]) + ':' + str(new_y[1])).ClearContents()

    def draw_sheet_line(self, **input):
        enum_line = {
            "msoArrowheadNone": 1, "msoArrowheadTriangle": 2, "msoArrowheadOpen": 3, "msoArrowheadStealth": 4,
            "msoArrowheadDiamond": 5, "msoArrowheadOval": 6,
            "": 1, "<": 2, ">o": 3, ">>": 4, ">": 2, "<>": 5, "o": 6,
            "basic": 1, "none": 1, "triangle": 2, "open": 3, "stealth": 4, "diamond": 5, "oval": 6,
            "msoArrowheadNarrow": 1, "msoArrowheadWidthMedium": 2, "msoArrowheadWide": 3,
            "msoArrowheadShort": 1, "msoArrowheadLengthMedium": 2, "msoArrowheadLong": 3,
            "short": 1, "narrow": 1, "medium": 2, "long": 3, "wide": 3,
            "-1": 1, "0": 2, "1": 3,
            "dash": 4, "dashdot": 5, "dashdotdot": 6, "rounddot": 3, "longdash": 7, "longdashdot": 8,
            "longdashdotdot": 9,
            "squaredot": 2,
            "-": 4, "-.": 5, "-..": 6, ".": 3, "--": 7, "--.": 8, "--..": 9, "ㅁ": 2,
        }

        base_data = {
            "sheet_name": "",
            "xyxy": [100, 100, 0, 0],
            "color": 10058239,
            "line_style": "-.",
            "thickness": 0.5,
            "transparency": 0,
            "head_style": ">",
            "head_length": "0",
            "head_width": "0",
            "tail_style": ">",
            "tail_length": "0",
            "tail_width": "0",
        }

        # 기본자료에 입력받은값을 update하는것이다
        base_data.update(input)

        sheet = self.check_sheet_name(base_data["sheet_name"])
        set_line = sheet.Shapes.AddLine(base_data["xyxy"][0], base_data["xyxy"][1], base_data["xyxy"][2],
                                        base_data["xyxy"][3])
        set_line.Select()
        set_line.Line.ForeColor.RGB = base_data["color"]
        set_line.Line.DashStyle = enum_line[base_data["line_style"]]
        set_line.Line.Weight = base_data["thickness"]
        set_line.Line.Transparency = base_data["transparency"]
        # print(set_line.Name)
        # 엑셀에서는 Straight Connector 63의 형태로 이름이 자동적으로 붙여진다

        set_line.Line.BeginArrowheadStyle = enum_line[base_data["head_style"]]
        set_line.Line.BeginArrowheadLength = enum_line[base_data["head_length"]]
        set_line.Line.BeginArrowheadWidth = enum_line[base_data["head_width"]]
        set_line.Line.EndArrowheadStyle = enum_line[base_data["tail_style"]]  # 화살표의 머리의 모양
        set_line.Line.EndArrowheadLength = enum_line[base_data["tail_length"]]  # 화살표의 길이
        set_line.Line.EndArrowheadWidth = enum_line[base_data["tail_width"]]  # 화살표의 넓이
        result = set_line.Name
        return result

    def dump_range_value(self, sheet_name, xyxy, input_data):
        # 영역에 값을 한번에 써 넣는 것이다
        # 차음시작하는 셀을 기준으로 알아서 맞추는 기능이다
        # 입력값과 영역이 맞지 않으면 입력값의 갯수를 더 우선함
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        y_len = len(input_data[0])
        x_len = len(input_data)
        print ([x1, y1, x1+x_len-1, y1+y_len-1])
        sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x1+x_len-1, y1+y_len-1)).value = input_data

    def dump_y_value(self, sheet_name, xyxy, input_data):
        # 영역에 값을 한번에 써 넣는 것이다
        # 차음시작하는 셀을 기준으로 알아서 맞추는 기능이다
        # 입력값과 영역이 맞지 않으면 입력값의 갯수를 더 우선함
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        y_len = len(input_data[0])
        x_len = len(input_data)
        sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x1+x_len-1, y1+y_len-1)).value = input_data

    def dump_newsheet_value(self, input_data):
        # 새로운 시트에 값을 한번에 써 넣는 것이다
        sheet = self.insert_workbook_sheet()
        sheet.Range("A1").value = input_data

    def fun_trim(self, input_data):
        # 함수중 trim을 사용하는 것이며 엑셀 함수의 사용을 보여주기 위하여 만든 것이다
        aaa = self.xlApp.WorksheetFunction.Trim(input_data)
        return aaa

    def fun_ltrim(self, input_data):
        # 함수중 ltrim을 사용하는 것이며 엑셀 함수의 사용을 보여주기 위하여 만든 것이다
        aaa = self.xlApp.WorksheetFunction.LTrim(input_data)
        return aaa

    def fun_rtrim(self, input_data):
        # 함수중 rtrim을 사용하는 것이며 엑셀 함수의 사용을 보여주기 위하여 만든 것이다
        aaa = self.xlApp.WorksheetFunction.RTrim(input_data)
        return aaa

    def insert_range_button(self, sheet_name, xyxy, macro, title):
        # 버튼을 만들어서 그 버튼에 매크로를 연결하는 것이다
        # 매크로와 같은것을 특정한 버튼에 연결하여 만드는것을 보여주기위한 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        new_btn = sheet.Buttons()
        new_btn.Add(x1, x2, y1, y2)
        new_btn.OnAction = macro
        new_btn.Text = title

    def insert_range_picture(self, sheet_name="", file_name=""):
        # 사진을 입력하는 것
        sheet = self.check_sheet_name(sheet_name)
        sheet.Shapes.AddPicture(file_name, 0, 1, 541.5, 92.25, 192.75, 180)

    def insert_workbook_sheet(self, sheet_name=""):
        # 시트하나 추가하기
            self.xlBook.Worksheets.Add()

    def insert_x_line(self, sheet_name, x):
        # 가로열을 한줄삽입하기
        sheet = self.check_sheet_name(sheet_name)
        x1 = self.check_xy_address(x)
        x_no = self.change_char_num(str(x1[0]))
        sheet.Range(str(x_no) + ':' + str(x_no)).Insert()

    def insert_line_x(self, sheet_name, x):
        self.insert_x_line(sheet_name, x)
        #예전 코드를 위해 남겨놓음

    def insert_y_line(self, sheet_name, y):
        # 세로행을 한줄삽입하기
        sheet = self.check_sheet_name(sheet_name)
        num_r1 = self.change_num_char(y)
        sheet.Columns(str(num_r1) + ':' + str(num_r1)).Insert()

    def insert_line_y(self, sheet_name, y):
        self.insert_y_line(sheet_name, y)
        #예전 코드를 위해 남겨놓음

    def intersect_range1_range2(self, xyxy0, xyxy1):
        # 두개의 영역에서 교차하는 구간을 돌려준다
        # 만약 교차하는게 없으면 ""을 돌려준다
        range_1 = self.check_range_address(xyxy0)
        range_2 = self.check_range_address(xyxy1)

        x11, y11, x12, y12 = range_1
        x21, y21, x22, y22 = range_2

        if x11 == 0:
           x11 = 1
           x12 = 1048576
        if x21 == 0:
           x21 = 1
           x22 = 1048576
        if y11 == 0:
           y11 = 1
           y12 = 16384
        if y21 == 0:
           y21 = 1
           y22 = 16384

        new_range_x = [x11, x21, x12, x22]
        new_range_y = [y11, y21, y12, y22]

        new_range_x.sort()
        new_range_y.sort()

        if x11 <= new_range_x[1] and x12 >= new_range_x[2] and y11 <= new_range_y[1] and y12 >= new_range_y[1]:
            result = [new_range_x[1], new_range_y[1], new_range_x[2], new_range_y[2]]
        else:
            result = "교차점없음"
        return result

    def make_list_unique(self, input_data):
        #1차원의 리스트가 중복값을 제외하고 돌려주는것
        result = []
        temp_dic = {}
        for one in input_data:
            temp_dic[one] = ""
        result = list(temp_dic.keys())
        result.sort()

        return result

    def make_y_value(self, input_data):
        #1차원의 리스트가 오면 2차원으로 만들어주는 것
        result = []
        if len(input_data) > 0:
            if type(input_data[0]) != type([]):
                for one in input_data:
                    result.append([one, ])
        return result

    def move_activecell_bottom(self, sheet_name="", xyxy=""):
        # 선택한 위치에서 끝부분으로 이동하는것
        # xlDown  : - 4121,  xlToLeft : - 4159, xlToRight  : - 4161, xlUp : - 4162
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Cells(x1, y1).End(- 4121).Select()
        return "ok"

    def move_activecell_left(self, sheet_name="", xyxy=""):
        # 선택한 위치에서 끝부분으로 이동하는것
        # xlDown  : - 4121,  xlToLeft : - 4159, xlToRight  : - 4161, xlUp : - 4162
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Cells(x1, y1).End(- 4159).Select()
        return "ok"

    def move_activecell_right(self, sheet_name="", xyxy=""):
        # 선택한 위치에서 끝부분으로 이동하는것
        # xlDown  : - 4121,  xlToLeft : - 4159, xlToRight  : - 4161, xlUp : - 4162
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Cells(x1, y1).End(- 4161).Select()
        return "ok"

    def move_activecell_top(self, sheet_name="", xyxy=""):
        # 선택한 위치에서 끝부분으로 이동하는것
        # xlDown  : - 4121,  xlToLeft : - 4159, xlToRight  : - 4161, xlUp : - 4162
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Cells(x1, y1).End(- 4162).Select()
        return "ok"

    def move_degree_distance(self, degree, distance):
        #현재 위치 x,y에서 30도로 20만큼 떨어진 거리의 위치를 돌려주는 것
        degree = degree * 3.141592/180
        x = distance * math.cos(degree)
        y = distance * math.sin(degree)
        return [x, y]

    def move_x_line(self, sheet_name_1, sheet_name_2, x0, x1):
        self.cut_x_line(sheet_name_1, sheet_name_2, x0, x1)

    def move_y_line(self, sheet_name_1, sheet_name_2, y0, y1):
        self.cut_y_line(sheet_name_1, sheet_name_2, y0, y1)

    def read_activesheet_name(self):
        # 현재의 엑셀중에서 활성화된 시트의 이름을 돌려준다
        return self.xlApp.ActiveSheet.Name

    def read_activecell_address(self):
        xy = self.check_address_value(self.xlApp.ActiveCell.Address)
        return xy

    def read_activecell_value(self):
        # 현재 셀 하나의 값을 돌려준다
        # 예전 함수에서 약간 변형한것이다
        value = self.xlApp.ActiveCell.Value
        return value

    def read_activecell_range(self):
        # 돌려주는 값 [x, y]
        xyxy = self.read_activecell_address()
        return xyxy

    def read_cell_color(self, sheet_name, xy):
        # 셀 하나에 색을 입힌다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        result = my_range.Interior.Color
        return result

    def read_cell_memo(self, sheet_name, xy):
        # 메모를 읽어오는 것
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xy)
        result = sheet.Cells(x1, y1).Comment.Text()
        return result

    def read_cell_value(self, sheet_name, xy):
        # 값을 일정한 영역에서 갖고온다
        # 만약 영역을 두개만 주면 처음과 끝의 영역을 받은것으로 간주해서 알아서 처리하도록 변경하였다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xy)
        result = sheet.Cells(x1, y1).value
        return result

    def read_continousrange_value(self, sheet_name, xyxy):
        # 현재선택된 셀을 기준으로 연속된 영역을 가지고 오는 것입니다
        # **************다시한번 봐야할 코드이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)

        bottom = x1  # 아래의 행을 찾는다
        while sheet.Cells(bottom, y1).Value not in [None, '']:
            bottom = bottom + 1
        right = y2  # 오른쪽 열
        while sheet.Cells(x2, right).Value not in [None, '']:
            right = right + 1
        return sheet.Range(sheet.Cells(x1, y1), sheet.Cells(bottom, right)).Value

    def read_messagebox_value(self, text_01="www.halmoney.com"):
        # 메세지 박스로 원하는 겂을 알려주는 것이다
        result = self.xlApp.InputBox(text_01)
        return result

    def read_currentregion_address(self, xy=""):
        # 이것은 현재의 셀에서 공백과 공백열로 둘러싸인 활성셀영역을 돌려준다
        if xy == "":
            result = self.check_address_value(self.xlApp.ActiveCell.CurrentRegion.Address)
        else:
            sheet = self.check_sheet_name("")
            result = self.check_address_value(sheet.Cells(xy[0], xy[1]).CurrentRegion.Address)
        return result

    def read_range_unique(self, sheet_name, xyxy):
        # 선택한 자료중에서 고유한 자료만을 골라내는 것이다
        # 자료중에서 고유한것을 찾아내서, 선택영역에 다시 쓴다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        temp_data = self.read_range_value(sheet, xyxy)
        temp_result = []
        for one_list_data in temp_data:
            for one_data in one_list_data:
                if one_data in temp_result or type(one_data) == type(None):
                    pass
                else:
                    temp_result.append(one_data)
        self.delete_range_value(sheet, xyxy)

        for num in range(len(temp_result)):
            mox, namuji = divmod(num, x2 - x1 + 1)
            self.write_cell_value(sheet, [x1 + namuji, y1 + mox], temp_result[num])

    def read_range_value(self, sheet_name, xyxy):
        # 값을 일정한 영역에서 갖고온다
        # 만약 영역을 두개만 주면 처음과 끝의 영역을 받은것으로 간주해서 알아서 처리하도록 변경하였다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        temp_result = my_range.Value
        result = []
        if 1 < len(temp_result):
            for one_data in temp_result:
                result.append(list(one_data))
        else:
            result = temp_result
        return result

    def read_rangename_address(self, sheet_name, xyxy_name):
        sheet = self.check_sheet_name(sheet_name)
        temp = sheet.Range(xyxy_name).Address
        result = self.check_address_value(temp)
        return result

    def read_select_address(self):
        # 현재선택된 영역의 주소값을 돌려준다
        result = ""
        temp_address = self.xlApp.Selection.Address
        print(temp_address)
        temp_list = temp_address.split(",")
        if len(temp_list) == 1:
            result = self.check_address_value(self.xlApp.Selection.Address)
        if len(temp_list) > 1:
            result = []
            for one_address in temp_list:
                result.append(self.check_address_value(one_address))
        return result

    def read_range_name(self):
        names_count = self.xlBook.Names.Count
        result = []
        if names_count > 0:
            for aaa in range(1, names_count + 1):
                name_name = self.xlBook.Names(aaa).Name
                name_range = self.xlBook.Names(aaa)
                result.append([aaa, str(name_name), str(name_range)])
        return result

    def read_range_select(self):
        temp_address = self.xlApp.Selection.Address
        result = self.check_address_value(temp_address)
        return result

    def read_select_address (self):
        result = self.read_range_select()
        return result


    def read_shape_name(self, sheet_name="", no=""):
        sheet = self.check_sheet_name(sheet_name)
        return sheet.Shapes(no).Name

    def read_sheet_count(self):
        # 시트의 갯수를 돌려준다
        return self.xlBook.Worksheets.Count

    def read_sheet_object(self, sheet_name=""):
        if str(sheet_name).lower() == "activesheet" or sheet_name == "":
            sheet = self.xlApp.ActiveSheet
        elif sheet_name in self.read_sheet_name():
            sheet = self.xlBook.Worksheets(sheet_name)
        else:
            self.insert_workbook_sheet()
            old_sheet_name = self.read_activesheet_name()
            self.change_sheet_name(old_sheet_name, sheet_name)
            sheet = self.xlBook.Worksheets(sheet_name)
        return sheet

    def read_workbook_allsheetname(self):
        # 현재 워크북의 모든 시트알아내기
        temp_list = []
        for var_02 in range(1, self.read_sheet_count() + 1):
            temp_list.append(self.xlBook.Worksheets(var_02).Name)
        return temp_list

    def read_usedrange_address(self, sheet_name=""):
        # 이것은 usedrange를 돌려주는 것이다. 값은 리스트이며 처음은
        # usedrange의 시작셀 ,두번째는 마지막셀값이며 세번째는 전체영역을 돌려주는 것이다
        sheet = self.check_sheet_name(sheet_name)
        result = self.check_address_value(sheet.usedrange.address)
        return result

    def read_workbook_allrangename(self):
        # 현재 시트의 이름을 전부 돌려준다
        # [번호, 영역이름, 영역주소]
        names_count = self.xlBook.Names.Count
        result = []
        if names_count > 0:
            for aaa in range(1, names_count + 1):
                name_name = self.xlBook.Names(aaa).Name
                name_range = self.xlBook.Names(aaa)
                result.append([aaa, str(name_name), str(name_range)])
        return result

    def read_workbook_fullname(self):
        # application의 이름과 전체경로를 돌려준다
        return self.xlBook.FullName

    def read_workbook_name(self):
        # application의 이름을 돌려준다
        return self.xlBook.Name

    def read_workbook_path(self):
        # application의 경로를 돌려준다
        return self.xlBook.Path

    def read_workbook_username(self):
        #사용자 이름을 읽어온다
        return self.xlApp.Username

    def read_x_value(self, sheet_name, x):
        # 한 가로행의 전체값을 갖고온다
        sheet = self.check_sheet_name(sheet_name)
        x_check = self.change_char_num(x)
        result = sheet.Cells(x_check, 1).EntireRow.Value
        return result

    def set_cell_bold(self, sheet_name, xyxy):
        # 셀안의 값을 진하게 만든다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Font.Bold = True

    def set_cell_color(self, sheet_name, xy, input_data):
        # 셀 하나에 색을 입힌다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Interior.Color = input_data

    def set_cell_picture(self, sheet_name, xy, full_path):
        # 사진을 불러오는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xy)
        sheet.Cells(x1, y1).Select()
        aaa = sheet.Pictures
        aaa.Insert(full_path).Select()

    def set_cell_select(self, sheet_name, xyxy):
        #영역을 선택한다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Cells(x1, y1).Select()

    def set_print_page (self, sheet_name="", **var_dic):
        sheet = self.check_sheet_name(sheet_name)
        sheet.PageSetup.Zoom = False
        sheet.PageSetup.FitToPagesTall = 1
        sheet.PageSetup.FitToPagesWide = 1
        #sheet.PageSetup.PrintArea = print_area
        sheet.PageSetup.LeftMargin = 25
        sheet.PageSetup.RightMargin = 25
        sheet.PageSetup.TopMargin = 50
        sheet.PageSetup.BottomMargin = 50
        #sheet.ExportAsFixedFormat(0, path_to_pdf)
        sheet.PageSetup.LeftFooter = "&D" #날짜
        sheet.PageSetup.LeftHeader = "&T" #시간
        sheet.PageSetup.CenterHeader = "&F" #화일명
        sheet.PageSetup.CenterFooter = "&P/&N" #현 page/ 총 page
        sheet.PageSetup.RightHeader = "&Z" #화일 경로
        sheet.PageSetup.RightFooter = "&P+33" #현재 페이지 + 33
        return result

    def set_range_autofilter(self, sheet_name, row1, row2=None):
        # 엑셀의 자동필터 기능을 추가한 것입니다
        sheet = self.check_sheet_name(sheet_name)
        if row2 == None:
            row2 = row1
        a = str(row1) + ':' + str(row2)
        sheet.Rows(a).Select()
        sheet.Range(a).AutoFilter(1)

    def set_range_autofit (self, sheet_name="", xyxy=""):
        # 선택한 시트의 모든 컬럼에 대해 자동 맞춤을 한 후에 각 컴럼별로 10px만큼 더 키운다
        # 더 키우는 이유는 보통 프린트할때 문제가 생기는 것을 방지하기 위한 목적이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_y_range = sheet.Columns(str(y1) + ':' + str(y2))

        if xyxy == "":
            sheet.EntireColumn.AutoFit()
        else:
            sheet.my_y_range.AutoFit()
        for y in range(y1, y2):
            width = sheet.Columns(str(y) + ':' + str(y)).ColumnWidth
            sheet.Columns(str(y) + ':' + str(y)).ColumnWidth = width + 10

    def set_range_clear(self, sheet_name, xyxy):
        # clear기능을 한다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.ClearContents()

    def set_range_color(self, sheet_name, xyxy, input_data):
        # 영역에 색깔을 입힌다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Interior.Color = input_data

    def set_range_font(self, sheet_name, xyxy, font):
        # 영역에 글씨체를 설정한다
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet = self.check_sheet_name(sheet_name)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.font.Name = font

    def set_range_fontcolor(self, sheet_name, xyxy, font_name):
        # 영역에 글씨체를 설정한다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2)).Font.Color = font_name

    def set_range_fontsize(self, sheet_name, xyxy, input_data):
        # 영역에 글씨크기를 설정한다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.font.Size = input_data

    def set_range_formula(self, sheet_name, xyxy, input_data):
        #영역에 식을 할당하는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Formula = input_data

    def set_range_line(self, sheet_name, xyxy, line_value=""):
        # 안쪽의 선들지정
        # [선의위치, 라인스타일, 굵기, 색깔]
        # 입력예 : [7,1,2,1]
        # 선의위치 (5-대각선 오른쪽, 6-왼쪽대각선, 7:왼쪽, 8;위쪽, 9:아래쪽, 10:오른쪽, 11:안쪽세로, 12:안쪽가로)
        # 라인스타일 (1-실선, 2-점선, 3-가는점선, 6-굵은실선,
        # 굵기 (0-이중, 1-얇게, 2-굵게)
        # 색깔 (0-검정, 1-검정3-빨강),

        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)

        if line_value == "":
            for one in [7,8,9,10]:
                my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2)).Borders(one)
                my_range.Color = 1
                my_range.Weight = 2
                my_range.LineStyle = 1
        else:
            my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2)).Borders(line_value[0])
            print(line_value[0],line_value[1],line_value[2],line_value[3])
            my_range.Color = int(line_value[3])
            my_range.Weight = int(line_value[2])
            #여기에서 linestyle을 제일 나중에 해야지 잘적용이 되며, 만약 다른것을 나중에 하면 점선으로만 나온다
            my_range.LineStyle = int(line_value[1])

    def set_range_merge(self, sheet_name, xyxy):
        # 셀들을 합하는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        if x1 == x2:
            sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2)).Merge(0)
        else:
            for a in xyxy(y2 - y1 + 1):
                sheet.Range(sheet.Cells(y1 + a, x1), sheet.Cells(y1 + a, x2)).Merge(0)

    def set_range_numberformat(self, sheet_name, xyxy, numberformat):
        # 영역에 숫자형식을 지정하는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.NumberFormat = numberformat

    def set_range_rangename(self, sheet_name, xyxy, name):
        # 영역에 이름으로 설정하는 기능
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range  = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        self.xlBook.Names.Add(name, my_range)

    def set_range_rgbcolor(self, sheet_name, xyxy, input_data):
        # 영역에 색깔을 입힌다
        # 엑셀에서의 색깔의 번호는 아래의 공식처럼 만들어 진다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        rgb_to_int = (int(input_data[2]))*(256**2)+(int(input_data[1]))*256+int(input_data[0])
        my_range.Interior.Color = rgb_to_int

    def set_range_select(self, sheet_name, xyxy):
        #영역을 선택한다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Select()

    def set_range_unmerge(self, sheet_name, xyxy):
        #병합된 것을 푸는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Range(xyxy).UnMerge()

    def set_range_wrap(self, sheet_name, xyxy, input_data):
        # 셀의 줄바꿈을 설정할때 사용한다
        # 만약 status를 false로 하면 줄바꿈이 실행되지 않는다.
        sheet = self.check_sheet_name(sheet_name)
        sheet.Range(xyxy).WrapText = input_data

    def set_sheet_fullscreen(self, fullscreen=1):
        # 전체화면으로 보기
        self.xlApp.DisplayFullScreen = fullscreen

    def set_sheet_hide(self, sheet_name, hide=0):
        # 시트 숨기기
        sheet = self.check_sheet_name(sheet_name)
        sheet.Visible = hide

    def set_sheet_gridline(self):
        # 그리드 라인을 계속 바꾼다
        if self.xlApp.ActiveWindow.DisplayGridlines == 0:
            self.xlApp.ActiveWindow.DisplayGridlines = 1
        else:
            self.xlApp.ActiveWindow.DisplayGridlines = 0

    def set_sheet_preview(self, sheet_name=""):
        # 미리보기기능입니다
        sheet = self.check_sheet_name(sheet_name)
        sheet.PrintPreview()

    def set_sheet_lock(self, sheet_name="", password="1234"):
        # 시트 잠그기
        sheet = self.check_sheet_name(sheet_name)
        sheet.protect(password)

    def set_sheet_unlock(self, sheet_name="", password="1234"):
        # 시트 잠그기 해제
        sheet = self.check_sheet_name(sheet_name)
        sheet.Unprotect(password)

    def set_sheet_visible(self, input_data=0):
        # 실행되어있는 엑셀을 화면에 보이지 않도록 설정합니다
        self.xlApp.Visible = input_data

    def set_workbook_close(self):
        # 현재는 close를 시키면 엑셀워크북만이 아니라 엑셀자체도 종료 시킵니다
        self.xlBook.Close(SaveChanges=0)
        del self.xlApp

    def set_workbook_fullscreen(self, fullscreen=1):
        # 전체화면으로 보기
        self.xlApp.DisplayFullScreen = fullscreen

    def set_workbook_hide(self):
        # 실행되어있는 엑셀을 화면에 보이지 않도록 설정합니다
        # visible로 통합
        self.xlApp.Visible = 0

    def set_workbook_save(self, newfilename=None):
        # 별도의 지정이 없으면 기존의 화일이름으로 저장합니다
        if newfilename:
            self.xlBook.SaveAs(newfilename)
        else:
            self.xlBook.Save()

    def set_wrap_on(self, sheet_name, xyxy, input_data):
        # 셀의 줄바꿈을 설정할때 사용한다
        # 만약 status를 false로 하면 줄바꿈이 실행되지 않는다.
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet = self.check_sheet_name(sheet_name)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.WrapText = input_data

    def set_x_length(self, sheet_name, x, height=13.5):
        # 가로열의 높이를 설정하는 것이다
        sheet = self.check_sheet_name(sheet_name)
        new_x = self.check_xy_address(x)
        my_range = sheet.Range(sheet.Cells(new_x[0], 1), sheet.Cells(new_x[1], 5))
        my_range.Select()
        my_range.EntireRow.RowHeight = height

    def set_y_length(self, sheet_name, y, length=8.38):
        # 열이나 행의 넓이를 조절한다
        # 엑셀은 기본적으로 넓이는 8.38 로, 높이는 13.5로 되어있읍니다
        sheet = self.check_sheet_name(sheet_name)
        new_y = self.check_xy_address(y)
        my_range = sheet.Range(sheet.Cells(1, new_y[0]), sheet.Cells(1, new_y[1]))
        my_range.EntireColumn.ColumnWidth = length

    def set_y_numberproperty(self, sheet_name, y0, style):
        # 각 열을 기준으로 셀의 속성을 설정하는 것이다
        sheet = self.check_sheet_name(sheet_name)
        y1 = self.check_xy_address(y0)
        y = self.change_char_num(y1)
        if style == 1:  # 날짜의 설정
            sheet.Columns(y).NumberFormatLocal = "mm/dd/" \
                                                 ""
        elif style == 2:  # 숫자의 설정
            sheet.Columns(y).NumberFormatLocal = "_-* #,##0.00_-;-* #,##0.00_-;_-* '-'_-;_-@_-"
        elif style == 3:  # 문자의 설정
            sheet.Columns(y).NumberFormatLocal = "@"

    def show_messagebox_value(self, input_data, web="www.halmoney.com"):
        # 메세지박스를 이용하여 원하는 내용을 보여준다
        win32gui.MessageBox(0, input_data, web, 0)

    def split_eng_num(self, data):
        # 단어중에 나와있는 숫자, 영어를 분리하는기능
        re_compile = re.compile(r"([a-zA-Z]+)([0-9]+)")
        result = re_compile.findall(data)
        new_result = []
        for dim1_data in result:
            for dim2_data in dim1_data:
                new_result.append(dim2_data)
        return new_result



    def write_cell_memo (self, sheet_name, xy, text ):
        # 셀에 메모를 넣는 것
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xy)
        sheet.Cells(x1, y1).AddComment(text)

    def write_cell_value(self, sheet_name, xy, value):
        # 값을 셀에 넣는다. (사용법) write_cell(시트이름, 행번호, 열번호, 넣을값)
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xy)
        sheet.Cells(x1, y1).Value = value

    def write_range_list(self, sheet_name, xyxy, list_data):
        # 2차원 리스트로 된 값을 영역에 쓰는 것이다
        self.write_range_value(sheet_name, xyxy, list_data)

    def write_range_value(self, sheet_name, xyxy, input_data):
        # 영역에 값을 하나씩 써 넣는 것이다
        # 입력값과 영역이 맞지 않으면 입력값의 갯수를 더 우선함
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)

        for x in range(len(input_data)):
            for y in range(len(input_data[x])):
                sheet.Range(sheet.Cells(x1+x, y1+y), sheet.Cells(x1+x, y1+y)).value = input_data[x][y]
