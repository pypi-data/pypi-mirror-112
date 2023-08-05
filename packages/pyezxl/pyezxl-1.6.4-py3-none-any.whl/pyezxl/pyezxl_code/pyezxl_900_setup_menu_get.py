#  -*- coding: utf-8 -*-

from requests import get
#사이트에 접속해서 메뉴화일을 다운받아 내 PC에 저장하는 방법
def download(url, file_name):
    with open(file_name, "wb") as file:   # open in binary mode
        response = get(url)               # get request
        file.write(response.content)      # write to file

if __name__ == '__main__':
	url = "http://halmoney.com/menu_001.txt"
	download(url,"d://menu1.txt")

