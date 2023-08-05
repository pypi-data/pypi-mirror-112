import pyezxl
excel = pyezxl.pyezxl("activeworkbook")

list_wai = """간단 메뉴얼
좀더 상세한 메뉴얼은 pyezxl_manual안의 자료를 참조 하세요

* 함수의 이름은 3개로 나누어서 언더바를 이용하여 작성
  셀에 값을 넣는것은 : write_cell_value(시트이름, 셀주소, 값)
  함수이름의 형태 : 동작_영역_무엇을 (쓰다_셀에_값을)

* 이 패키지의 기본적인 목적
  엑셀의 자동활를 쉽고 편하게 사용하기 위하여 만들었으며
  어려운 엑셀 VBA를 사용하기 쉽게 Python으로 만듦
  이것은 엑셀에 쓰고, 읽고, 색등을 바꾸는것에 촛점을 두었으며
  복잡한 문서의 처리등은 파이썬의 정규분포식등의 다른 모듈을 
  이용하여 가공한후, 읽고 쓰는것은 이 패키지를 사용하기를 권장한다

* 이 패키지의 Excel_addin에 대하여
  기존에 VBA와 Python으로 만들어서 혼자 사용하던 기능들을
  좀더 사용하기 편하게 만들어 pyezxl에 같이 넣었으며
  pyezxl의 실제 사용방법을 볼수있으며
  사용자가 직접 자주사용하는 코드는 만들어서 넣을 수 있게 만들었으며
  좋은 코드를 보내주시면, 공유자의 이름을 넣어 공유하도록 하겠읍니다

* 향후 다른 스프레드쉬트 (openoffice, 한셀, libre 등)도 
  동일한 함수와 방법으로 사용이 가능하도록 만들 예정이다
  
* 가격정책
  등록용과 비등록용의 사용상 차이는 없으며, 
  등록용은 차후 개별 serial_no을 별도로 송부 예정이며
  등록비용은 향후 다른 프로젝트의 일부로 사용될 에정입니다
  등록비용 : www.halmoney.com방문 요망
"""

all_text=""
for a in list_wai:
	all_text = all_text + a + '\n'

excel.show_messagebox_value(list_wai)

