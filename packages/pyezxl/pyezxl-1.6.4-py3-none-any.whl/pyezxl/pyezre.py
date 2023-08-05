# -*- coding: utf-8 -*-
import re
import pyezxl

class ezre:

    def change_rgb_int(self, input_data):
        # rgb인 값을 color에서 인식이 가능한 값으로 변경하는 것이다
        result = (int(input_data[2]))*(256**2)+(int(input_data[1]))*256+int(input_data[0])
        return result

    def check_all_cap(self, input_data):
        # 모두 알파벳대문자
        re_basic ="^[A-Z]+$"
        result = re.findall(re_basic, input_data)
        return result

    def check_dash_date (self, input_data):
        # 모두 알파벳대문자
        re_basic ="^\d{4}-\d{1,2}-\d{1,2}$"
        result = re.findall(re_basic, input_data)
        return result


    def check_email_address(self, input_data):
        # 이메일주소 입력
        re_basic ="^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
        result = re.findall(re_basic, input_data)
        return result

    def check_eng_only (self, input_data):
        # 모두 영문인지
        re_basic ="[a-zA-Z]"
        result = re.findall(re_basic, input_data)
        return result

    def check_handphone_only (self, input_data):
        # 특수문자가들어가있는지
        re_basic ="^(010|019|011)-\d{4}-\d{4}"
        result = re.findall(re_basic, input_data)
        return result

    def check_ip_address(self, input_data):
        # 이메일주소 입력
        re_basic ="((?:(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d))"
        result = re.findall(re_basic, input_data)
        return result

    def check_korean_only (self, input_data):
        # 모두 한글인지
        re_basic ="[ㄱ-ㅣ가-힣]"
        result = re.findall(re_basic, input_data)
        return result

    def check_special_char (self, input_data):
        # 특수문자가들어가있는지
        re_basic ="^[a-zA-Z0-9]"
        result = re.findall(re_basic, input_data)
        return result

    def delete_except_engnum(self, input_text):
        # 알파벳과 숫자만 있는것을 확인하는것
        re_com= re.compile("[^A-Za-z0-9]")
        if (re_com.search(input_text) == None):
            new_text = input_text
        else:
            print(re_com.search(input_text))
            new_text = re_com.sub("", input_text)
            print(new_text)
        return new_text

    def delete_except_korengnum(self, input_text):
        # 한글, 영어, 숫자만 남기고 나머지는 모두 지우는 것이다
        re_com= re.compile("[^A-Za-z0-9ㄱ-ㅎㅏ-ㅣ가-힣]")
        if (re_com.search(input_text) == None):
            new_text = input_text
        else:
            print(re_com.search(input_text))
            new_text = re_com.sub("", input_text)
            print(new_text)
        return new_text

    def delete_except_numcomma(self, input_text):
        # 숫자중에서 ,로 분비리된것중에서 ,만 없애는것
        #1,234,567 => 1234567
        re_com= re.compile("[0-9,]")
        re_com_1= re.compile("[,]")
        if (re_com.search(input_text) == None):
            new_text = input_text
        else:
            new_text = re_com_1.sub("", input_text)
            print(new_text)
        return new_text

    def delete_except_specialchar (self, input_text):
        # 공백과 특수문자등을 제외하고 같으면 새로운 y열에 1을 넣는 함수
        # 리스트의 사이즈를 조정한다
        re_com= re.compile("[\s!@#$%^*()\-_=+\\\|\[\]{};:'\",.<>\/?]")
        if (re_com.search(input_text) == None):
            new_text = input_text
        else:
            new_text = re_com.sub("", input_text)
            print(new_text)
        return new_text

    def delete_text_specialletter(self, input_list):
        # 입력받은 텍스트로된 리스트의 자료를 전부 특수문자를 없앤후 돌려주는 것이다
        #입력된 자료가 1차원 리스트인지 판단한다
        if type(input_list) == type([]) and type(input_list[0]) != type([]):
            result = []
            for one in input_list:
                if one != "" or one != None:
                    temp = self.re_delete_specialletter(one)
                    result.append(temp)
        return result

    def draw_jaum_color(one_char="ㄱ", start=[2, 2], size=[20, 20]):
        # 사이즈를 변경한 자음의 좌표를 갖고온다
        excel = pyezxl.pyezxl("")
        ja_xyxy_lists = self.jaum_xy_list([size[0], size[1]], one_char)

        for xyxy in ja_xyxy_lists[1:]:
            x1 = int(xyxy[0]) + int(start[0])
            y1 = int(xyxy[1]) + int(start[1])
            x2 = int(xyxy[2]) + int(start[0])
            y2 = int(xyxy[3]) + int(start[1])

            if x1 == x2 or y1 == y2:
                excel.set_range_color("", [x1, y1, x2, y2], 0)
            else:
                get_range_xcells_simple([x1, y1, x2, y2])

    def draw_moum_color(one_char="ㅏ", start=[2, 2], size=[20, 20]):
        # 사이즈를 변경한 자음의 좌표를 갖고온다
        excel = pyezxl.pyezxl("")
        moum_xyxy_lists = self.moum_xy_list([size[0], size[1]], one_char)
        for xyxy in moum_xyxy_lists[1:]:
            # 아래의 경우는 직선일때이다
            x1 = int(xyxy[0]) + int(start[0])
            y1 = int(xyxy[1]) + int(start[1])
            x2 = int(xyxy[2]) + int(start[0])
            y2 = int(xyxy[3]) + int(start[1])
            excel.set_range_color("", [x1, y1, x2, y2], 0)

    def ezre(self, input_data):
        input_data = input_data.replace(" ", "")
        # 아래의 내용중 순서가 중요하므로 함부러 바꾸지 않기를 바랍니다
        # 1. 제일먼저의것은
        # &로 되어있는것은 제일 마지막에 처리를 하도록 하였다
        # 만약 새로운 글자셋이 있다면 아래의 3개를 같이 넣어야 한다
        # 1."[한글]": "[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]",
        # 2."한글&": "ㄱ-ㅎ|ㅏ-ㅣ|가-힣",
        # 3."한글": "ㄱ-ㅎ|ㅏ-ㅣ|가-힣",

        ezre_dic = {
            ":최소반복]": "]?",
            ":1번이상]": "]+",
            ":0번이상]": "]*",
            ":0-1번]": "]?",
            "또는": "|",
            "[특수문자": "[",
            "[not": "[^",

            "(앞에있음:": "(?=",
            "(뒤에있음:": "(?<=",
            "(앞에없음:": "(?!",
            "(뒤에없음:": "(?<!",

            "[1번이상]": "+",
            "[0번이상]": "*",
            "[0-1번]": "?",
            "[맨앞]": "^",
            "[시작]": "^",
            "[맨뒤]": "$",
            "[맨끝]": "$",
            "[끝]": "$",
            "[최소반복]": "?",

            "[공백]": "\s",
            "[문자]": ".",
            "[숫자]": "0-9",
            "[영어]": "[a-zA-Z]",
            "[영어대문자]": "[A-Z]",
            "[영어소문자]": "[a-z]",
            "[한글]": "[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]",

            "[영어&숫자]": "\w",
            "[숫자&영어]": "\w",

            "문자&": ".",
            "숫자&": "0-9",
            "영어&": "a-zA-Z",
            "영어대문자&": "A-Z",
            "영어소문자&": "a-z",
            "한글&": "ㄱ-ㅎ|ㅏ-ㅣ|가-힣",

            "숫자": "0-9",
            "영어": "a-zA-Z",
            "영어대문자": "A-Z",
            "영어소문자": "a-z",
            "한글": "ㄱ-ㅎ|ㅏ-ㅣ|가-힣",
        }

        ezre_list = ["\[최소\d*?번\]",
                     "\[최대\d*?번\]",
                     "\[\d*-\d*?번\]",
                     "\[\d*?번\]",
                     ":최소\d*?번\]",
                     ":최대\d*?번\]",
                     ":\d*-\d*?번\]",
                     ":\d*?번\]"]

        changed_data = input_data
        print("변환전 ==> ", changed_data)

        for num_1 in range(len(ezre_list)):
            compile_1 = re.compile(ezre_list[num_1])
            result_1 = compile_1.findall(changed_data)
            if result_1:
                for num in range(len(result_1)):
                    one = result_1[num]
                    compile_1 = re.compile("\d+")
                    no = compile_1.findall(one)
                    if num_1 == 0:
                        new_str = "{" + str(no[0]) + ",}"
                    elif num_1 == 1:
                        new_str = "{," + str(no[0]) + "}"
                    elif num_1 == 2:
                        new_str = "{" + str(no[0]) + "," + str(no[1]) + "}"
                    elif num_1 == 3:
                        new_str = "{" + str(no[0]) + "}"
                    elif num_1 == 4:
                        new_str = "]{" + str(no[0]) + ",}"
                    elif num_1 == 5:
                        new_str = "]{," + str(no[0]) + "}"
                    elif num_1 == 6:
                        new_str = "]{" + str(no[0]) + "," + str(no[1]) + "}"
                    elif num_1 == 7:
                        new_str = "]{" + str(no[0]) + "}"
                    changed_data = changed_data.replace(result_1[num], new_str)

        for ezre_value in ezre_dic.keys():
            re_value = ezre_dic[ezre_value]
            changed_data = changed_data.replace(ezre_value, re_value)
        print("중간변환 ==> ", changed_data)

        min_dic = {
            "a-zA-Z0-9": "\w",
            "0-9a-zA-Z": "\w",
            "0-9": "\d",
        }
        for ezre_value in min_dic.keys():
            re_value = min_dic[ezre_value]
            changed_data = changed_data.replace(ezre_value, re_value)

        print("변환완료 ==> ", changed_data)

        return changed_data

    def get_between_number_length(self, input_data, m, n):
        # m,n개사이인것만 추출
        re_basic ="^\d{"+str(m)+","+str(n) +"}$"
        result = re.findall(re_basic, input_data)
        return result

    def get_between_text_length(self, input_data, m, n):
        # 문자수제한 : m다 크고 n보다 작은 문자
        re_basic ="^.{"+str(m)+","+str(n) +"}$"
        result = re.findall(re_basic, input_data)
        return result

    def get_char_between(self, input_data, text_a, text_b):
        # 입력된 자료에서 두문자사이의 글자를 갖고오는것
        replace_lists=[
            ["(","\("],
            [")", "\)"],
        ]
        origin_a = text_a
        origin_b = text_b

        for one_list in replace_lists:
            text_a = text_a.replace(one_list[0], one_list[1])
            text_b = text_b.replace(one_list[0], one_list[1])
        re_basic =text_a+"[^"+str(origin_b)+"]*"+text_b
        result = re.findall(re_basic, input_data)
        return result

    def get_diagonal_xy (self, xyxy=[5, 9, 12, 21]):
        # 좌표와 대각선의 방향을 입력받으면, 대각선에 해당하는 셀을 돌려주는것
        # 좌표를 낮은것 부터 정렬하기이한것 [3, 4, 1, 2] => [1, 2, 3, 4]
        if xyxy[0] > xyxy[2]:
            x1, y1, x2, y2 = xyxy[2], xyxy[3], xyxy[0], xyxy[1]
        else:
            x1, y1, x2, y2 = xyxy

        x_height = abs(x2 - x1) + 1
        y_width = abs(y2 - y1) + 1
        step = x_height / y_width
        temp = 0

        if x1 <= x2 and y1 <= y2:
            # \형태의 대각선
            for y in range(1, y_width + 1):
                x = y * step
                if int(x) >= 1:
                    final_x = int(x) + x1 - 1
                    final_y = int(y) + y1 - 1
                    if temp != final_x:
                        result.append([final_x, final_y])
                        temp = final_x
        else:
            for y in range(y_width, 0, -1):
                x = x_height - y * step

                final_x = int(x) + x1
                final_y = int(y) + y1 - y_width
                temp_no = int(x)

                if temp != final_x:
                    temp = final_x
                    result.append([final_x, final_y])
        return result

    def get_diagonal_xy_1 (self, xyxy=[5, 9, 12, 21]):
        # 좌표와 대각선의 방향을 입력받으면, 대각선에 해당하는 셀을 돌려주는것
        # 좌표를 낮은것 부터 정렬하기이한것 [3, 4, 1, 2] => [1, 2, 3, 4]
        result = []
        if xyxy[0] > xyxy[2]:
            x1, y1, x2, y2 = xyxy[2], xyxy[3], xyxy[0], xyxy[1]
        else:
            x1, y1, x2, y2 = xyxy

        x_height = abs(x2 - x1) + 1
        y_width = abs(y2 - y1) + 1
        step = x_height / y_width
        temp = 0

        if x1 <= x2 and y1 <= y2:
            # \형태의 대각선
            for y in range(1, y_width + 1):
                x = y * step
                if int(x) >= 1:
                    final_x = int(x) + x1 - 1
                    final_y = int(y) + y1 - 1
                    excel.set_cell_color("", [final_x, final_y], 1)

        else:
            for y in range(y_width, 0, -1):
                x = x_height - y * step

                final_x = int(x) + x1
                final_y = int(y) + y1 - y_width
                temp_no = int(x)
                result.append([final_x, final_y])
        return result

    def get_re_data (self, input_data, re_text):
        # 어떤 문잣가 있는지 확인하는것
        re_basic = str(re_text)
        result = re.findall(re_basic, input_data)
        return result

    def get_text_between_ab(self, input_data, text_a, text_b):
        # 입력된 자료에서 두개문자사이의 글자를 갖고오는것
        replace_lists=[
            ["(","\("],
            [")", "\)"],
        ]
        origin_a = text_a
        origin_b = text_b

        for one_list in replace_lists:
            text_a = text_a.replace(one_list[0], one_list[1])
            text_b = text_b.replace(one_list[0], one_list[1])
        re_basic =text_a+"[^"+str(origin_b)+"]*"+text_b
        result = re.findall(re_basic, input_data)
        return result

    def moum_xy_list (size =[1, 2], input_data = "ㅏ"):
        x, y = size
        #x, y는 글자의 크기
        mo_01 = [["ㅏ"],[1, 0.6 * y,x, 0.6 * y],
                 [0.4 * x, 0.6 * y,0.4 * x, 0.8 * y]]
        mo_02 = [["ㅑ"],[1, 0.6 * y,x, 0.6 * y],
                 [0.4 * x, 0.6 * y,0.4 * x, 0.8 * y],
                 [0.6 * x, 0.6 * y,0.6 * x, 0.8 * y]]
        mo_03 = [["ㅓ"],[1, 0.6 * y,x, 0.6 * y],
                 [0.4 * x, 0.4 * y,0.4 * x, 0.6 * y]]
        mo_04 = [["ㅕ"],[1, 0.6 * y,x, 0.6 * y],
                 [0.4 * x, 0.4 * y,0.4 * x, 0.6 * y],
                 [0.6 * x, 0.4 * y,0.6 * x, 0.6 * y]]
        mo_10 = [["ㅣ"],[1, 0.6 * y,x, 0.6 * y]]
        mo_05 = [["ㅗ"],[x, 1,x, y],
                 [x, 0.5 * y,0.8 * x, 0.5 * y]]
        mo_06 = [["ㅛ"],[x, 1,x, y],
                 [x, 0.3 * y,0.8 * x, 0.3 * y],
                 [x, 0.7 * y,0.8 * x, 0.7 * y]]
        mo_07 = [["ㅜ"],[1, 1,1, y],
                 [1, 0.5 * y,0.5 * x, 0.5 * y]]
        mo_08 = [["ㅠ"],[1, 1,1, y],
                 [1, 0.3 * y,0.8 * x, 0.3 * y],
                 [1, 0.7 * y,0.8 * x, 0.7 * y]]
        mo_09 = [["ㅡ"],[0.5 * x, 1,0.5 * x, y]]

        mo_21 = [["ㅐ"],[1, 0.6 * y,x, 0.6 * y],
                 [1, 0.8 * y,x, 0.8 * y],
                 [0.4 * x, 0.6 * y,0.4 * x, 0.8 * y]]
        mo_22 = [["ㅒ"],[1, 0.6 * y,x, 0.6 * y],
                 [1, 0.8 * y,x, 0.8 * y],
                 [0.4 * x, 0.6 * y,0.4 * x, 0.6 * y],
                 [0.6 * x, 0.8 * y,0.6 * x, 0.8 * y]]
        mo_23 = [["ㅔ"],[1, 0.6 * y,x, 0.6 * y],
                 [1, 0.8 * y,x, 0.8 * y],
                 [0.4 * x, 0.4 * y,0.4 * x, 0.6 * y]]
        mo_24 = [["ㅖ"],[1, 0.6 * y,x, 0.6 * y],
                 [1, 0.8 * y,x, 0.8 * y],
                 [0.4 * x, 0.4 * y,0.4 * x, 0.6 * y],
                 [0.6 * x, 0.4 * y,0.6 * x, 0.6 * y]]

        jamo2_dic = {
                    "ㅏ": mo_01, "ㅑ": mo_02, "ㅓ": mo_03, "ㅕ": mo_04, "ㅗ": mo_05,
                    "ㅛ": mo_06, "ㅜ": mo_07, "ㅠ": mo_08, "ㅡ": mo_09, "ㅣ": mo_10,
                    "ㅐ": mo_21, "ㅒ": mo_22, "ㅔ": mo_23, "ㅖ": mo_24,
                    }
        result = jamo2_dic[input_data]
        return result

    def jaum_xy_list(size=[1, 2], input_data="ㄱ"):
        x, y = size
        # x, y는 글자의 크기
        ja_01 = [["ㄱ"], [1, 1, 1, y], [1, y, x, y]]
        ja_02 = [["ㄴ"], [1, 1, x, 1], [x, 1, x, y]]
        ja_03 = [["ㄷ"], [1, y, 1, 1], [1, 1, x, 1], [x, 1, x, y]]
        ja_04 = [["ㄹ"], [1, 1, 1, y], [1, y, 0.5 * x, y], [0.5 * x, y, 0.5 * x, 1], [0.5 * x, 1, x, 1], [x, 1, x, y]]
        ja_05 = [["ㅁ"], [1, 1, 1, y], [1, y, x, y], [x, y, x, 1], [x, 1, 1, 1]]
        ja_06 = [["ㅂ"], [1, 1, x, 1], [x, 1, x, y], [x, y, 1, y], [0.5 * x, 1, 0.5 * x, y]]
        ja_07 = [["ㅅ"], [1, 0.5 * y, 0.3 * x, 0.5 * y], [0.3 * x, 0.5 * y, x, 1], [0.3 * x, 0.5 * y, x, y]]
        ja_08 = [["ㅇ"], [0.8 * x, 0.2 * y, 0.8 * x, 0.8 * y], [0.8 * x, 0.8 * y, 0.6 * x, y, ""],
                 [0.6 * x, y, 0.2 * x, y], [0.2 * x, y, 1, 0.8 * y, "/"], [1, 0.8 * y, 1, 0.2 * y],
                 [1, 0.2 * y, 0.2 * x, 1, ""], [0.2 * x, 1, 0.6 * x, 1], [0.6 * x, 1, 0.8 * x, 0.2 * y, "/"]]
        ja_09 = [["ㅈ"], [1, 1, 1, y], [1, 0.5 * y, 0.5 * x, 0.5 * y], [0.5 * x, 0.5 * y, x, 1, "/"],
                 [0.5 * x, 0.5 * y, x, y, ""]]
        ja_10 = [["ㅊ"], [0.2 * x, 0.5 * y, 1, 0.5 * y], [0.2 * x, 1, 0.2 * x, y], [0.2 * x, 0.5 * y, 0.4 * x, 0.5 * y],
                 [1, 0.5 * y, 0.5 * x, 0.5 * y], [0.5 * x, 0.5 * y, x, 1], [0.5 * x, 0.5 * y, x, y, ""]]
        ja_11 = [["ㅋ"], [1, 1, 1, y], [1, y, x, y], [0.5 * x, 1, 0.5 * x, y]]
        ja_12 = [["ㅌ"], [1, y, 1, 1], [1, 1, x, 1], [x, 1, x, y], [0.5 * x, 1, 0.5 * x, y]]
        ja_13 = [["ㅍ"], [1, 1, 1, y], [x, 1, x, y], [1, 0.2 * y, x, 0.2 * y], [1, 0.8 * y, x, 0.8 * y]]
        ja_14 = [["ㅎ"], [1, 0.5 * y, 0.2 * x, 0.5 * y], [0.2 * x, 1, 0.2 * x, y], [0.4 * x, 0.3 * y, 0.4 * x, 0.8 * y],
                 [0.4 * x, 0.8 * y, 0.6 * x, y], [0.6 * x, y, 0.8 * x, y], [0.8 * x, y, x, 0.8 * y],
                 [x, 0.8 * y, x, 0.3 * y], [x, 0.3 * y, 0.8 * x, 1], [0.8 * x, 1, 0.6 * x, 1],
                 [0.6 * x, 1, 0.4 * x, 0.3 * y]]
        ja_31 = [["ㄲ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], ]
        ja_32 = [["ㄸ"], [1, 1, 1, 0.4 * y], [1, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y],
                 [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], ]
        ja_33 = [["ㅃ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [x, 0.4 * y, 1, 0.4 * y], [0.5 * x, 1, 0.5 * x, 0.4 * y],
                 [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], [x, y, 1, y], [0.5 * x, 0.7 * y, 0.5 * x, y], ]
        ja_34 = [["ㅆ"], [1, 0.3 * y, 0.4 * x, 0.3 * y], [0.4 * x, 0.3 * y, x, 1], [0.4 * x, 0.3 * y, x, 0.5 * y],
                 [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
        ja_35 = [["ㅉ"], [1, 1, 1, 0.5 * y], [1, 0.3 * y, 0.4 * x, 0.3 * y], [0.4 * x, 0.3 * y, x, 1],
                 [0.4 * x, 0.3 * y, x, 0.5 * y], [1, 0.6 * y, 1, y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
                 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
        ja_36 = [["ㄳ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, x, 0.4 * y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
                 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
        ja_37 = [["ㄵ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.6 * y, 1, y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
                 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
        ja_38 = [["ㄶ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [0.1 * x, 0.8 * y, 1, 0.8 * y],
                 [0.2 * x, 0.6 * y, 0.2 * x, y], [0.4 * x, 0.7 * y, 0.4 * x, 0.9 * y], [0.4 * x, 0.9 * y, 0.6 * x, y],
                 [0.6 * x, y, x, 0.9 * y], [x, 0.9 * y, x, 0.7 * y], [x, 0.7 * y, 0.8 * x, 0.6 * y],
                 [0.8 * x, 0.6 * y, 0.6 * x, 0.6 * y], [0.6 * x, 0.6 * y, 0.4 * x, 0.7 * y]]
        ja_39 = [["ㄺ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
                 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], ]
        ja_40 = [["ㄻ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
                 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], [x, y, x, 0.7 * y],
                 [x, 0.7 * y, 1, 0.7 * y], ]
        ja_41 = [["ㄼ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
                 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], [x, y, 1, y],
                 [0.5 * x, 0.7 * y, 0.5 * x, y], ]
        ja_42 = [["ㄽ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
                 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y],
                 [0.4 * x, 0.8 * y, x, y], ]
        ja_43 = [["ㄾ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
                 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, 0.7 * y, x, 0.7 * y],
                 [x, 0.7 * y, x, y], [0.5 * x, 0.7 * y, 0.5 * x, y], ]
        ja_44 = [["ㄿ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
                 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.6 * y, 1, y], [x, 0.6 * y, x, y],
                 [1, 0.7 * y, x, 0.7 * y], [1, 0.9 * y, x, 0.9 * y], ]
        ja_45 = [["ㅀ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
                 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [0.1 * x, 0.8 * y, 1, 0.8 * y], [0.2 * x, 0.6 * y, 0.2 * x, y],
                 [0.4 * x, 0.7 * y, 0.4 * x, 0.9 * y], [0.4 * x, 0.9 * y, 0.6 * x, y], [0.6 * x, y, x, 0.9 * y],
                 [x, 0.9 * y, x, 0.7 * y], [x, 0.7 * y, 0.8 * x, 0.6 * y], [0.8 * x, 0.6 * y, 0.6 * x, 0.6 * y],
                 [0.6 * x, 0.6 * y, 0.4 * x, 0.7 * y]]
        ja_46 = [["ㅄ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [x, 0.4 * y, 1, 0.4 * y], [0.5 * x, 1, 0.5 * x, 0.4 * y],
                 [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]

        jamo1_dic = {"ㄱ": ja_01, "ㄴ": ja_02, "ㄷ": ja_03, "ㄹ": ja_04, "ㅁ": ja_05,
                    "ㅂ": ja_06, "ㅅ": ja_07, "ㅇ": ja_08, "ㅈ": ja_09, "ㅊ": ja_10,
                    "ㅋ": ja_11, "ㅌ": ja_12, "ㅍ": ja_13, "ㅎ": ja_14,
                    "ㄲ": ja_31, "ㄸ": ja_32, "ㅃ": ja_33, "ㅆ": ja_34, "ㅉ": ja_35,
                    "ㄳ": ja_36, "ㄵ": ja_37, "ㄶ": ja_38, "ㄺ": ja_39, "ㄻ": ja_40,
                    "ㄼ": ja_41, "ㄽ": ja_42, "ㄾ": ja_43, "ㄿ": ja_44, "ㅀ": ja_45, "ㅄ": ja_46,
                    }

        result = jamo1_dic[input_data]
        return result

    def run_ezre(self, input_data, input_sql):
        re_com = re.compile(input_sql)
        re_results = re_com.finditer(input_data)
        result = []
        if re_results:
            for one in re_results:
                result.append([one.group(), one.start(), one.end()])
        return result


    def sort_list_data(self, input_data):
        # aa = [[111, 'abc'], [222, 222],['333', 333], ['777', 'sjpark'], ['aaa', 123],['zzz', 'sang'], ['jjj', 987], ['ppp', 'park']]
        # 정렬하는 방법입니다
        result = []
        for one_data in input_data:
            for one in one_data:
                result.append(one.sort())
        return result

    def split_double_moum (self, double_moum):
        #이중모음을 단모음으로 바꿔주는것
        mo2_dic = { "ㅘ": ["ㅗ", "ㅏ"], "ㅙ": ["ㅗ", "ㅐ"], "ㅚ": ["ㅗ", "ㅣ"], "ㅝ": ["ㅜ", "ㅓ"], "ㅞ": ["ㅜ", "ㅔ"], "ㅟ": ["ㅜ", "ㅣ"], "ㅢ": ["ㅡ", "ㅣ"], }
        result = mo2_dic[double_moum]
        return result

    def split_engnum(self, data):
        # 단어중에 나와있는 숫자, 영어를 분리하는기능
        re_compile = re.compile(r"([a-zA-Z]+)([0-9]+)")
        result = re_compile.findall(data)
        new_result = []
        for dim1_data in result:
            for dim2_data in dim1_data:
                new_result.append(dim2_data)
        return new_result

    def split_hangul_jamo (self, text):
        #한글자의 한글을 자음과 모음으로 구분해 주는것
        first_letter = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]  # 19 글자
        second_letter = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ",
                         "ㅣ"]  # 21 글자
        third_letter = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ",
                        "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]  # 28 글자, 없는것 포함
        one_byte_data = text.encode("utf-8")
        no_1 = int(one_byte_data[0])
        no_2 = int(one_byte_data[1])
        no_3 = int(one_byte_data[2])

        new_no_1 = (no_1-234)*64*64
        new_no_2 = (no_2-128)*64
        new_no_3 = (no_3-128)

        bite_no =  [no_1, no_2, no_3] #바이트번호인 16진수를 10진수로 나타낸것
        bite_no_1 =  [new_no_1, new_no_2, new_no_3] #바이트번호를 각 자릿수에 맞도록 1자리 숫자로 만들기 위해 변경한것

        value_sum = new_no_1 + new_no_2 + new_no_3
        value = value_sum - 3072 # 1의자리에서부터 시작하도록 만든것

        temp_num_1 = divmod(value, 588) #초성이 몇번째 자리인지를 알아내는것
        temp_num_2 = divmod(temp_num_1[1], 28) #중성과 종성의 자릿수를 알아내는것것

        chosung = first_letter[divmod(value, 588)[0]] #초성
        joongsung = second_letter[divmod(temp_num_1[1], 28)[0]] #중성
        jongsung = third_letter[temp_num_2[1]] #종성

        step_letter = [temp_num_1[1],temp_num_2[0],temp_num_2[1] ] #초성, 중성, 종성의 자릿수
        chojoongjong = [chosung, joongsung, jongsung ]#초성, 중성, 종성의 글자

        print("encode한 것 ==> ", one_byte_data)
        print("바이트번호를 각 자릿수에 맞도록 1자리 숫자로 만들기 위해 변경한것 ==> ", bite_no_1)
        print("입력한 한글 한글자는 ==> ", text)
        print("초성, 중성, 종성의 자릿수 ==> ", step_letter)
        print("초성, 중성, 종성의 글자 ==> ", chojoongjong)

        return [chojoongjong, step_letter, bite_no, value, one_byte_data]

    def swap(self, a, b):
        #a,b를 바꾸는 함수이다
        t = a
        a = b
        b = t
        return [a, b]

    def swap_list_data(self, input_data):
        # input_data : [a, b, c, d]
        # result : [b, a, d, c]
        # 두개의 자료들에 대해서만 자리를 바꾸는 것이다
        result = []
        for one_data in range(int(len(input_data) / 2)):
            result.append(input_data[one_data * 2 + 1])
            result.append(input_data[one_data * 2])
        return result

    def text_encoding_data(self, text, encoding_type):
        byte_data = text.encode(encoding_type)
        hex_data_as_str = " ".join("{0}".format(hex(c)) for c in byte_data)
        int_data_as_str = " ".join("{0}".format(int(c)) for c in byte_data)

        print("\"" + text + "\" 전체 문자 길이: {0}".format(len(text)))
        print("\"" + text + "\" 전체 문자를 표현하는 데 사용한 바이트 수: {0} 바이트".format(len(byte_data)))
        print("\"" + text + "\" 16진수 값: {0}".format(hex_data_as_str))
        print("\"" + text + "\" 10진수 값: {0}".format(int_data_as_str))
        # 사용법 : text_encoding_data("Hello", "utf-8")
        return int_data_as_str

    def write_hangul_cjj(self, letters = "박상진", canvas_size=[50,50], stary_xy = [1,1]):
        #입력받은 한글을 크기가 50 x 50의 엑셀 시트에 글씨를 색칠하여 나타내는 것이다
        
        #기본 설정부분
        size_x = canvas_size[0]
        size_y = canvas_size[1]
        # 문자 하나의 기본크기
        # 기본문자는 10을 기준으로 만들었으며, 이것을 얼마만큼 크게 만들것인지 한글자의 배수를 정하는것 
        h_mm = int(canvas_size[0]/10)
        w_mm = int(canvas_size[1]/10)
        # 시작위치
        h_start = stary_xy[0]
        w_start = stary_xy[1]

        check_han = re.compile("[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]")
        for one_char in letters:
            #한글을 초성, 중성, 종성으로 나누는 것이다
            if check_han.match(one_char):
                jamo123 = self.split_hangul_jamo(one_char)
                if jamo123[0][2] =="":
                    #가, 나, 다
                    if jamo123[0][1] in ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅣ"]:

                        #기본설정은 시작점은 [1,1]이며, 캔버스의 크기는 [50, 50]인것이다

                        start_xy = [1, 1]
                        size =[10,5] #위에서 배수를 5,5를 기본으로 해서 50x50되는 것이다
                        # 자음의 시작점은 1,1이며, 크기는 50 x 25의 사이즈의 자음을 만드는 것이다
                        self.draw_jaum_color(jamo123[0][0], [h_start+h_mm*(start_xy[0]-1), w_start+w_mm*(start_xy[1]-1)], [h_mm * size[0], w_mm * size[1]] )
                        # 모음의 시작점은 자음의 끝점에서 5를 이동한 1,30이며, 크기는 자음보다 가로의 크기를 좀 줄인
                        # 50 x 20의 사이즈의 자음을 만드는 것이다

                        start_xy = [1, 7]
                        size =[10,4]
                        self.draw_moum_color(jamo123[0][1], [h_start+h_mm*(start_xy[0]-1), w_start+w_mm*(start_xy[1]-1)], [h_mm * size[0], w_mm * size[1]])

                    # 구, 누, 루
                    if jamo123[0][1] in ["ㅗ", "ㅛ", "ㅜ", "ㅡ"]:
                        start_xy = [1, 1]
                        size =[4,10]
                        self.draw_jaum_color(jamo123[0][0], [h_start+h_mm*(start_xy[0]-1), w_start+w_mm*(start_xy[1]-1)], [h_mm * size[0], w_mm * size[1]] )
                        start_xy = [6, 1]
                        size =[5, 10]
                        self.draw_moum_color(jamo123[0][1], [h_start+h_mm*(start_xy[0]-1), w_start+w_mm*(start_xy[1]-1)], [h_mm * size[0], w_mm * size[1]])

                    # 와, 왜, 궈
                    if jamo123[0][1] in ["ㅘ", "ㅙ", "ㅚ", "ㅝ", "ㅞ", "ㅟ", "ㅢ"]:
                        lists = div_mo2_mo1(jamo123[0][1])

                        start_xy = [1, 1]
                        size =[10,5]
                        self.draw_jaum_color(jamo123[0][0], [h_start+h_mm*(start_xy[0]-1), w_start+w_mm*(start_xy[1]-1)], [h_mm * size[0], w_mm * size[1]] )
                        start_xy = [8, 1]
                        size =[3, 8]
                        self.draw_moum_color(jamo123[0][1], [h_start+h_mm*(start_xy[0]-1), w_start+w_mm*(start_xy[1]-1)], [h_mm * size[0], w_mm * size[1]])
                        start_xy = [1, 8]
                        size =[6,3]
                        self.draw_moum_color(jamo123[0][1], [h_start+h_mm*(start_xy[0]-1), w_start+w_mm*(start_xy[1]-1)], [h_mm * size[0], w_mm * size[1]])

                if jamo123[0][2] !="":
                    #왕, 웍, 윔
                    if jamo123[0][1] in ["ㅘ", "ㅙ", "ㅚ", "ㅝ", "ㅞ", "ㅟ", "ㅢ"]:
                        hangul_type = "23자음+1332-2중모음+24자음"
                        lists = div_mo2_mo1(jamo123[0][1])

                        start_xy = [1, 1]
                        size =[4,5]
                        self.draw_jaum_color(jamo123[0][0], [h_start+h_mm*(start_xy[0]-1), w_start+w_mm*(start_xy[1]-1)], [h_mm * size[0], w_mm * size[1]] )
                        start_xy = [4, 1]
                        size =[3,7]
                        self.draw_moum_color(jamo123[0][1], [h_start+h_mm*(start_xy[0]-1), w_start+w_mm*(start_xy[1]-1)], [h_mm * size[0], w_mm * size[1]])
                        start_xy = [1, 7]
                        size =[6, 3]
                        self.draw_moum_color(jamo123[0][1], [h_start+h_mm*(start_xy[0]-1), w_start+w_mm*(start_xy[1]-1)], [h_mm * size[0], w_mm * size[1]])
                        start_xy = [8, 1]
                        size =[3,6]
                        self.draw_jaum_color(jamo123[0][0], [h_start+h_mm*(start_xy[0]-1), w_start+w_mm*(start_xy[1]-1)], [h_mm * size[0], w_mm * size[1]] )

                    # 앙, 양, 건
                    if jamo123[0][1] in ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅣ"]:
                        start_xy = [1, 1]
                        size =[3,5]
                        self.draw_jaum_color(jamo123[0][0], [h_start+h_mm*(start_xy[0]-1), w_start+w_mm*(start_xy[1]-1)], [h_mm * size[0], w_mm * size[1]] )
                        start_xy = [1, 6]
                        size =[5,4]
                        self.draw_moum_color(jamo123[0][1], [h_start+h_mm*(start_xy[0]-1), w_start+w_mm*(start_xy[1]-1)], [h_mm * size[0], w_mm * size[1]])
                        start_xy = [7, 2]
                        size =[3,6]
                        self.draw_jaum_color(jamo123[0][0], [h_start+h_mm*(start_xy[0]-1), w_start+w_mm*(start_xy[1]-1)], [h_mm * size[0], w_mm * size[1]] )

                    # 곡, 는
                    if jamo123[0][1] in ["ㅗ", "ㅛ", "ㅜ", "ㅡ"]:
                        start_xy = [1, 1]
                        size =[3, 10]
                        self.draw_jaum_color(jamo123[0][0], [h_start+h_mm*(start_xy[0]-1), w_start+w_mm*(start_xy[1]-1)], [h_mm * size[0], w_mm * size[1]] )
                        start_xy = [4, 1]
                        size =[3, 10]
                        self.draw_moum_color(jamo123[0][1], [h_start+h_mm*(start_xy[0]-1), w_start+w_mm*(start_xy[1]-1)], [h_mm * size[0], w_mm * size[1]])
                        start_xy = [8, 1]
                        size =[3, 10]
                        self.draw_jaum_color(jamo123[0][0], [h_start+h_mm*(start_xy[0]-1), w_start+w_mm*(start_xy[1]-1)], [h_mm * size[0], w_mm * size[1]] )
                time.sleep(1)
