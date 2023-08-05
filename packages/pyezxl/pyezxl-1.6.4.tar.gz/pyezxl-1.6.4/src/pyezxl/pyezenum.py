class ezenum:
	my_web_site = "www.halmoney.com"
	def __init__(self):
		# 사용가능한 색깔을 보다 쉽게 표현하기위해 만들었다
		# 색은 3가지로 구분 : 테이블등을 만들때 사용하면 좋은 색 : color1~15번까지
		# 12가지의 색을 기본, 약간 옅은 테이블색칠용, 파스텔톤의 3가지로 구분
		# 각 3종류는 7개의 형태로 구분하여 +, -의 형태로 표현을 하도록 하였다
		pass

	def color_dic(self, input_data):
			original_data = {
				"": -4142, "none": -4142,
				"color1": 6384127, "color2": 4699135, "color3": 9895421, "color4": 7855479, "color5": 13616814, "color6": 11902643, "color7": 12566463, "color8": 12419407, "color9": 5066944, "color10": 5880731,
				"color11": 10642560, "color12": 13020235, "color13": 4626167, "color14": 65535, "color15": 13566071,
				"whi---": 15790320, "whi--": 16119285, "whi-": 16448250, "whi": 16777215, "whi+": 16777215, "whi++": 16777215, "whi+++": 16777215,
				"whi_t---": 15790320, "whi_t--": 16119285, "whi_t-": 16448250, "whi_t": 16777215, "whi_t+": 16777215, "whi_t++": 16777215, "whi_t+++": 16777215,
				"whi_p---": 15790320, "whi_p--": 16119285, "whi_p-": 16448250, "whi_p": 16777215, "whi_p+": 16777215,	"whi_p++": 16777215, "whi_p+++": 16777215,
				"bla---": 0, "bla--": 0, "bla-": 0, "bla": 0, "bla+": 1052688, "bla++": 2171169, "bla+++": 3289650,
				"bla_t---": 0, "bla_t--": 0, "bla_t-": 0, "bla_t": 0, "bla_t+": 1052688, "bla_t++": 2171169, "bla_t+++": 3289650,
				"bla_p---": 0, "bla_p--": 1052688, "bla_p-": 2171169, "bla_p": 3289650, "bla_p+": 4342338, "bla_p++": 5460819, "bla_p+++": 6579300,
				"gra---": 5855577, "gra--": 6710886, "gra-": 7566195, "gra": 8421504, "gra+": 9211020, "gra++": 10066329, "gra+++": 10921638,
				"gra_t---": 8355711, "gra_t--": 9605778, "gra_t-": 10855845, "gra_t": 12105912, "gra_t+": 13355979, "gra_t++": 14606046, "gra_t+++": 15921906,
				"gra_p---": 13355979, "gra_p--": 13750737, "gra_p-": 14211288, "gra_p": 14606046, "gra_p+": 15066597, "gra_p++": 15461355, "gra_p+++": 15921906,
				"red---": 179, "red--": 204, "red-": 230, "red": 255, "red+": 1710847, "red++": 3355647, "red+++": 5066239,
				"red_t---": 2303075, "red_t--": 4276858, "red_t-": 6316434, "red_t": 8356010, "red_t+": 10329794, "red_t++": 12369370, "red_t+++": 14408946,
				"red_p---": 1384703, "red_p--": 3029503, "red_p-": 4739583, "red_p": 6384127, "red_p+": 8094207, "red_p++": 9738751, "red_p+++": 11449087,
				"ora---": 29875, "ora--": 33996, "ora-": 38374, "ora": 42495, "ora+": 1748735, "ora++": 3389439, "ora+++": 5095679,
				"ora_t---": 411799, "ora_t--": 2712488, "ora_t-": 5013177, "ora_t": 7379402, "ora_t+": 9680091, "ora_t++": 11980780, "ora_t+++": 14347005,
				"ora_p---": 37626, "ora_p--": 1351423, "ora_p-": 3057919, "ora_p": 4699135, "ora_p+": 6405887, "ora_p++": 8046847, "ora_p+++": 9753599,
				"yel---": 46003, "yel--": 52428, "yel-": 59110, "yel": 65535, "yel+": 1769471, "yel++": 3407871, "yel+++": 5111807,
				"yel_t---": 47292, "yel_t--": 115655, "yel_t-": 249810, "yel_t": 383965, "yel_t+": 452584, "yel_t++": 586739, "yel_t+++": 720895,
				"yel_p---": 4979964, "yel_p--": 6618364, "yel_p-": 8257021, "yel_p": 9895421, "yel_p+": 11533821, "yel_p++": 13172478, "yel_p+++": 14810878,
				"gre---": 13312, "gre--": 19712, "gre-": 26368, "gre": 32768, "gre+": 39424, "gre++": 45824, "gre+++": 52480,
				"gre_t---": 2646351, "gre_t--": 4618601, "gre_t-": 6590851, "gre_t": 8563101, "gre_t+": 10535351, "gre_t++": 12507601, "gre_t+++": 14545387,
				"gre_p---": 3853882, "gre_p--": 5165902, "gre_p-": 6543459, "gre_p": 7855479, "gre_p+": 9167499, "gre_p++": 10545056, "gre_p+++": 11857076,
				"blu---": 11730944, "blu--": 13369344, "blu-": 15073280, "blu": 16711680, "blu+": 16718362, "blu++": 16724787, "blu+++": 16731469,
				"blu_t---": 6772768, "blu_t--": 8286527, "blu_t-": 9800286, "blu_t": 11379581, "blu_t+": 12893340, "blu_t++": 14407099, "blu_t+++": 15986395,
				"blu_p---": 11773054, "blu_p--": 12365710, "blu_p-": 13024158, "blu_p": 13616814, "blu_p+": 14209470, "blu_p++": 14867918, "blu_p+++": 15460574,
				"ind---": 3538975, "ind--": 5177390, "ind-": 6881340, "ind": 8519755, "ind+": 10223706, "ind++": 11862120, "ind+++": 13566071,
				"ind_t---": 6373412, "ind_t--": 7953218, "ind_t-": 9533281, "ind_t": 11113087, "ind_t+": 12693150, "ind_t++": 14272956, "ind_t+++": 15853019,
				"ind_p---": 3538975, "ind_p--": 5177390, "ind_p-": 6881340, "ind_p": 8519755, "ind_p+": 10223706, "ind_p++": 11862120, "ind_p+++": 13566071,
				"pur---": 3407924, "pur--": 5046349, "pur-": 6750311, "pur": 8388736, "pur+": 10092698, "pur++": 11731123, "pur+++": 13435085,
				"pur_t---": 5321023, "pur_t--": 6966874, "pur_t-": 8678262, "pur_t": 10389650, "pur_t+": 12101037, "pur_t++": 13812425, "pur_t+++": 15524069,
				"pur_p---": 9728913, "pur_p--": 10453404, "pur_p-": 11178152, "pur_p": 11902643, "pur_p+": 12627134, "pur_p++": 13351882, "pur_p+++": 14076373,
				"pin---": 4656639, "pin--": 6435327, "pin-": 8214015, "pin": 10058239, "pin+": 11836927, "pin++": 13615615, "pin+++": 15459839,
				"pin_t---": 8543231, "pin_t--": 9201919, "pin_t-": 9860607, "pin_t": 10519295, "pin_t+": 11177983, "pin_t++": 11836671, "pin_t+++": 12495615,
				"pin_p---": 10651135, "pin_p--": 11441919, "pin_p-": 12298239, "pin_p": 13154559, "pin_p+": 14010879, "pin_p++": 14867199, "pin_p+++": 15723519,
				"bro---": 4478571, "bro--": 4807795, "bro-": 5137019, "bro": 5466499, "bro+": 5795723, "bro++": 6124947, "bro+++": 6454427,
				"bro_t---": 7243428, "bro_t--": 7769256, "bro_t-": 8295341, "bro_t": 8821426, "bro_t+": 9347255, "bro_t++": 9873340, "bro_t+++": 10399425,
				"bro_p---": 11977425, "bro_p--": 12634839, "bro_p-": 13292253, "bro_p": 13949924, "bro_p+": 14607338, "bro_p++": 15264752, "bro_p+++": 15922423,
				1: 0, 2: 16777215, 3: 255, 4: 65280, 5: 16711680, 6: 65535, 7: 16711935, 8: 16776960, 9: 128, 10: 32768,
				11: 8388608, 12: 32896, 13: 8388736, 14: 8421376, 15: 12632256, 16: 8421504, 17: 16751001, 18: 6697881,
				19: 13434879, 20: 16777164,
				21: 6684774, 22: 8421631, 23: 13395456, 24: 16764108, 25: 8388608, 26: 16711935, 27: 65535, 28: 16776960,
				29: 8388736, 30: 128,
				31: 8421376, 32: 16711680, 33: 16763904, 34: 16777164, 35: 13434828, 36: 10092543, 37: 16764057, 38: 13408767,
				39: 16751052, 40: 10079487,
				41: 16737843, 42: 13421619, 43: 52377, 44: 52479, 45: 39423, 46: 26367, 47: 10053222, 48: 9868950, 49: 6697728,
				50: 6723891,
				51: 13056, 52: 13107, 53: 13209, 54: 6697881, 55: 10040115, 56: 3355443,
			}
			result = original_data[input_data]

			return result

	def color_list(self, color_name="none", type=0, no=0):
		original_data = {
			"ez": [[""], [6384127], [4699135], [9895421], [7855479], [13616814], [11902643], [12566463], [12419407],
			       [5066944], [5880731], [10642560], [13020235], [4626167], [65535], [13566071]],
			"basic": [[""], [0], [16777215], [255], [65280], [16711680], [65535], [16711935], [16776960], [128],
			          [32768],
			          [8388608], [32896], [8388736], [8421376], [12632256], [8421504], [16751001], [6697881],
			          [13434879], [16777164],
			          [6684774], [8421631], [13395456], [16764108], [8388608], [16711935], [65535], [16776960],
			          [8388736], [128],
			          [8421376], [16711680], [16763904], [16777164], [13434828], [10092543], [16764057], [13408767],
			          [16751052], [10079487],
			          [16737843], [13421619], [52377], [52479], [39423], [26367], [10053222], [9868950], [6697728],
			          [6723891],
			          [13056], [13107], [13209], [6697881], [10040115], [3355443], ],
			"none" : [[-4142]],
			"whi" : [[16777215, 16777215, 16777215, 16777215, 15790320, 16119285, 16448250, ], [16777215, 16777215, 16777215, 16777215, 15790320, 16119285, 16448250, ],[16777215, 16777215, 16777215, 16777215, 15790320, 16119285, 16448250, ]],
			"bla" : [[0, 1052688, 2171169, 3289650, 0, 0, 0, ], [0, 1052688, 2171169, 3289650, 0, 0, 0, ],[3289650, 4342338, 5460819, 6579300, 0, 1052688, 2171169, ]],
			"gra" : [[8421504, 9211020, 10066329, 10921638, 5855577, 6710886, 7566195, ],[12105912, 13355979, 14606046, 15921906, 8355711, 9605778, 10855845, ],[14606046, 15066597, 15461355, 15921906, 13355979, 13750737, 14211288, ]],
			"red" : [[255, 1710847, 3355647, 5066239, 179, 204, 230, ],[8356010, 10329794, 12369370, 14408946, 2303075, 4276858, 6316434, ], [6384127, 8094207, 9738751, 11449087, 1384703, 3029503, 4739583, ]],
			"ora" : [[42495, 1748735, 3389439, 5095679, 29875, 33996, 38374, ], [7379402, 9680091, 11980780, 14347005, 411799, 2712488, 5013177, ], [4699135, 6405887, 8046847, 9753599, 37626, 1351423, 3057919, ]],
			"yel" : [[65535, 1769471, 3407871, 5111807, 46003, 52428, 59110, ], [383965, 452584, 586739, 720895, 47292, 115655, 249810, ], [9895421, 11533821, 13172478, 14810878, 4979964, 6618364, 8257021, ]],
			"gre" : [[32768, 39424, 45824, 52480, 13312, 19712, 26368, ], [8563101, 10535351, 12507601, 14545387, 2646351, 4618601, 6590851, ], [7855479, 9167499, 10545056, 11857076, 3853882, 5165902, 6543459, ]],
			"blu" : [[16711680, 16718362, 16724787, 16731469, 11730944, 13369344, 15073280, ], [11379581, 12893340, 14407099, 15986395, 6772768, 8286527, 9800286, ], [13616814, 14209470, 14867918, 15460574, 11773054, 12365710, 13024158, ]],
			"ind" : [[8519755, 10223706, 11862120, 13566071, 3538975, 5177390, 6881340, ], [11113087, 12693150, 14272956, 15853019, 6373412, 7953218, 9533281, ], [8519755, 10223706, 11862120, 13566071, 3538975, 5177390, 6881340, ]],
			"pur" : [[8388736, 10092698, 11731123, 13435085, 3407924, 5046349, 6750311, ], [10389650, 12101037, 13812425, 15524069, 5321023, 6966874, 8678262, ], [11902643, 12627134, 13351882, 14076373, 9728913, 10453404, 11178152, ]],
			"pin" : [[10058239, 11836927, 13615615, 15459839, 4656639, 6435327, 8214015, ], [10519295, 11177983, 11836671, 12495615, 8543231, 9201919, 9860607, ], [13154559, 14010879, 14867199, 15723519, 10651135, 11441919, 12298239, ]],
			"bro" : [[5466499, 5795723, 6124947, 6454427, 4478571, 4807795, 5137019, ], [8821426, 9347255, 9873340, 10399425, 7243428, 7769256, 8295341, ], [13949924, 14607338, 15264752, 15922423, 11977425, 12634839, 13292253, ]],
			}

			# 1. 빨주노초파남보(무지개) 와 검정, 하양, 회색, 분홍, 고동으로 총 12개의 색을 나타낸다
			#   white,black,gray,red,orange,yellow,gre,blu,ind,pur,pin,bro
			# 2. 모든색은 기본보다 어두운색, 기본색, 기본보다 밝은색의 3가지로 구분하고
			# 3. 각 구분된색은 7단계로 세분하여 총 21가지의 색을 정의하였다
			# 4. 2차원의 배열로 표시하였고, 1차원에서 3단게로 구분 : 어두운색은 red[-1], 기본색은 red[0], 좀 밝은색은 red[-1]
			# 5. 2차원에서 -3 ~ 3 까지의 7단계로 구분한다 : red[0][-3] ~ red[0][3]
			# 6. 색을 없애는것은 nocolor을 이용

		# basic의 첫번째것은 색이 없는것이다
		color_list = original_data[color_name]
		result = color_list[type][no]

		return result

	def copy_type(self, input_data):
			original_data = {
			"basic" : -4104,	    	"all" : -4104,	                      	"memo" : -4144,	                    	    "format" : -4122,		"formula" : -4123,
			"formula+format" : 11,  	"value" : -4163,        	            "value+format" : 12,
			"pasteall" : -4104,	    	"pasteallexceptborders" : 7,            "pasteallmergingconditionalformats" : 14,	"pasteallusingsourcetheme" : 13,
			"pastecolumnwidths" : 8,	"pastecomments" : -4144,	        	"pasteformats" : -4122,
			"pasteformulas" : -4123,	"pasteformulasandnumberformats" : 11,	"pastevalidation" : 6,
			"pastevalues" : -4163,		"pastevaluesandnumberformats" : 12,
			}
			result = original_data[input_data]

			return result

	def letter(self, input_data):
			original_data = {
				# 시작하는 첫글자로 이름을 사용한다
				# 원으로된 글자는 "a원"처럼 이름을 만듦
				"a": "abcdefghijklmnopqrstuvwxyz",
				"알파벳": "abcdefghijklmnopqrstuvwxyz",
				"영어": "abcdefghijklmnopqrstuvwxyz",
				"alphabet": "abcdefghijklmnopqrstuvwxyz",
				"ㄱ": "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ",
				"자음": "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ",
				"모음": "ㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣ",
				"ㅏ": "ㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣ",
				"가": "가나다라마바사아자차카타파하",
				"1": "1234567890",
				"숫자": "1234567890",
				"α": "αβγδεζήθικλμνξόπρΣτ",
				"그리스문자": "αβγδεζήθικλμνξόπρΣτ",
				"Ⅰ": "ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ",
				"로마숫자": "ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ",
				"원ㄱ": "㉠㉡㉢㉣㉤㉥㉦㉧㉨㉩㉪㉫㉬㉭",
				"ㄱ원": "㉠㉡㉢㉣㉤㉥㉦㉧㉨㉩㉪㉫㉬㉭",
				"원가": "㉮㉯㉰㉱㉲㉳㉴㉵㉶㉷㉸㉹㉺㉻",
				"가원": "㉮㉯㉰㉱㉲㉳㉴㉵㉶㉷㉸㉹㉺㉻",
				"a원": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ",
				"원a": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ",
				"원1": "⓪①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚㉛㉜㉝㉞㉟㊱㊲㊳㊴㊵㊶㊷㊸㊹㊺㊻㊼㊽㊾㊿",
				"1원": "⓪①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚㉛㉜㉝㉞㉟㊱㊲㊳㊴㊵㊶㊷㊸㊹㊺㊻㊼㊽㊾㊿",
			}
			result = original_data[input_data]

			return result

	def line(self, input_data):
			original_data = {
			"msoArrowheadNone": 1,   "msoArrowheadTriangle": 2, "msoArrowheadOpen": 3,
			 "msoArrowheadStealth": 4,"msoArrowheadDiamond": 5, "msoArrowheadOval": 6,
			"": 1, "<": 2, ">o": 3, ">>": 4, ">": 2, "<>": 5, "o": 6,
			"basic": 1, "none": 1, "triangle": 2, "open": 3, "stealth": 4, "diamond": 5, "oval": 6,
			"msoArrowheadNarrow": 1, "msoArrowheadWidthMedium": 2, "msoArrowheadWide": 3,
			"msoArrowheadShort": 1, "msoArrowheadLengthMedium": 2, "msoArrowheadLong": 3,
			"short": 1, "narrow": 1, "medium": 2, "long": 3, "wide": 3,
			"-1": 1, "0": 2, "+1": 3,
			"dash": 4, "dashdot": 5, "dashdotdot": 6, "rounddot": 3, "longdash": 7, "longdashdot": 8, "longdashdotdot": 9, "squaredot": 2,
			"-": 4, "-.": 5, "-..": 6, ".": 3, "--": 7, "--.": 8, "--..": 9, "ㅁ": 2,
			}
			result = original_data[input_data]

			return result

	def line_t(self, input_data):
			original_data = {
				"hairline": 1,			"thin": 2,				"medium": -4138,			"thick": 4,
				"t1": 1,				"t2": 2,				"t3": -4138,				"t4": 4,
				"basic--": 1,			"basic-": 2,			"basic+": -4138,			"basic++": 4,
			}
			result = original_data[input_data]

			return result

	def line_thick(self, input_data):
		original_data = {
			"" : 1,	    	    "basic" : 1,	"-" : -4115 ,		"-." : 4,		"-.." : 5,		"." : -4118,		"=" : -4119,		"none" : -4142,		"/." : 13,
			"t1" : 1,	    	"t2" : 2,		"t3" : -4138,		"t4" : 4,
			"basic--" : 1,		"basic-" : 2,	"basic+" : -4138,	"basic++" : 4,
			"\\" : 5,	    	"/" : 6,		"b" : 9,	    	"l" : 7,		"r" : 8,		"t" : 10,
			"in-h" : 12,		"in-v" : 11,	"bottom" : 9,		"left" : 7,		"right" : 10,	"top" : 8,
			"bottom-in" : 12,	"top-in" : 11,	"rightleft-in" : 12,"leftright-in" : 5,
			"continuous" : 1,	"dash" : -4115 ,"dashdot" : 4,		"dashdotdot" : 5,		"dot" : -4118,
			"double" : -4119,	"slantdashdot" : 13,		"hairline" : 1,		"thin" : 2,		"medium" : -4138,		"thick" : 4,
			"diagonaldown" : 5,	"diagonalup" : 6,		"edgebottom" : 9,		"edgeleft" : 7,		"edgeright" : 8,		"edgetop" : 10,
			"insidehorizontal" : 12,		"insidevertical" : 11,		"inside-h" : 12,		"inside-v" : 11,
			}
		result = original_data[input_data]

		return result

	def sharp(self, input_data):
			result = {
			"10pointStar" : 149, #10-point star,
			"12pointStar" : 150, #12-point star,
			"16pointStar" : 94, #16-point star,
			"24pointStar" : 95, #24-point star,
			"32pointStar" : 96, #32-point star,
			"4pointStar" : 91, #4-point star,
			"5pointStar" : 92, #5-point star,
			"6pointStar" : 147, #6-point star,
			"7pointStar" : 148, #7-point star,
			"8pointStar" : 93, #8-point star,
			"ActionButtonBackorPrevious" : 129, #Back or Previous button. Supports mouse-click and mouse-over actions.,
			"ActionButtonBeginning" : 131, #Beginning button. Supports mouse-click and mouse-over actions.,
			"ActionButtonCustom" : 125, #Button with no default picture or text. Supports mouse-click and mouse-over actions.,
			"ActionButtonDocument" : 134, #Document button. Supports mouse-click and mouse-over actions.,
			"ActionButtonEnd" : 132, #End button. Supports mouse-click and mouse-over actions.,
			"ActionButtonForwardorNext" : 130, #Forward or Next button. Supports mouse-click and mouse-over actions.,
			"ActionButtonHelp" : 127, #Help button. Supports mouse-click and mouse-over actions.,
			"ActionButtonHome" : 126, #Home button. Supports mouse-click and mouse-over actions.,
			"ActionButtonInformation" : 128, #Information button. Supports mouse-click and mouse-over actions.,
			"ActionButtonMovie" : 136, #Movie button. Supports mouse-click and mouse-over actions.,
			"ActionButtonReturn" : 133, #Return button. Supports mouse-click and mouse-over actions.,
			"ActionButtonSound" : 135, #Sound button. Supports mouse-click and mouse-over actions.,
			"Arc" : 25, #원호, Arc,
			"Balloon" : 137, #Balloon,
			"BentArrow" : 41, #화살표(굽음)Block arrow that follows a curved 90-degree angle.,
			"BentUpArrow" : 44, #Block arrow that follows a sharp 90-degree angle. Points up by default.,
			"Bevel" : 15, #사각형(빗면)Bevel,
			"BlockArc" : 20, #원형(안이막힌것), Block arc,
			"Can" : 13, #원통형, Can,
			"ChartPlus" : 182, #Square divided vertically and horizontally into four quarters,
			"ChartStar" : 181, #Square divided into six parts along vertical and diagonal lines,
			"ChartX" : 180, #Square divided into four parts along diagonal lines,
			"Chevron" : 52, #Chevron,
			"Chord" : 161, #Circle with a line connecting two points on the perimeter through the interior of the circle; a circle with a chord,
			"CircularArrow" : 60, #Block arrow that follows a curved 180-degree angle,
			"Cloud" : 179, #Cloud shape,
			"CloudCallout" : 108, #Cloud callout,
			"Corner" : 162, #Rectangle with rectangular-shaped hole.,
			"CornerTabs" : 169, #Four right triangles aligning along a rectangular path; four 'snipped' corners.,
			"Cross" : 11, #십자형, Cross,
			"Cube" : 14, #정육면체, Cube,
			"CurvedDownArrow" : 48, #Block arrow that curves down,
			"CurvedDownRibbon" : 100, #Ribbon banner that curves down,
			"CurvedLeftArrow" : 46, #Block arrow that curves left,
			"CurvedRightArrow" : 45, #Block arrow that curves right,
			"CurvedUpArrow" : 47, #Block arrow that curves up,
			"CurvedUpRibbon" : 99, #Ribbon banner that curves up,
			"Decagon" : 144, #Decagon,
			"DiagonalStripe" : 141, #Rectangle with two triangles-shapes removed; a diagonal stripe,
			"Diamond" : 4, #Diamond,
			"Dodecagon" : 146, #Dodecagon,
			"Donut" : 18, #원형(빈것)도넛형, Donut,
			"DoubleBrace" : 27, #중괄호(양쪽)Double brace,
			"DoubleBracket" : 26, #대괄호(양쪽)Double bracket,
			"DoubleWave" : 104, #Double wave,
			"DownArrow" : 36, #화살표(아래쪽)Block arrow that points down,
			"DownArrowCallout" : 56, #Callout with arrow that points down,
			"DownRibbon" : 98, #Ribbon banner with center area below ribbon ends,
			"Explosion1" : 89, #Explosion,
			"Explosion2" : 90, #Explosion,
			"FlowchartAlternateProcess" : 62, #Alternate process flowchart symbol,
			"FlowchartCard" : 75, #Card flowchart symbol,
			"FlowchartCollate" : 79, #Collate flowchart symbol,
			"FlowchartConnector" : 73, #Connector flowchart symbol,
			"FlowchartData" : 64, #Data flowchart symbol,
			"FlowchartDecision" : 63, #Decision flowchart symbol,
			"FlowchartDelay" : 84, #Delay flowchart symbol,
			"FlowchartDirectAccessStorage" : 87, #Direct access storage flowchart symbol,
			"FlowchartDisplay" : 88, #Display flowchart symbol,
			"FlowchartDocument" : 67, #Document flowchart symbol,
			"FlowchartExtract" : 81, #Extract flowchart symbol,
			"FlowchartInternalStorage" : 66, #Internal storage flowchart symbol,
			"FlowchartMagneticDisk" : 86, #Magnetic disk flowchart symbol,
			"FlowchartManualInput" : 71, #Manual input flowchart symbol,
			"FlowchartManualOperation" : 72, #Manual operation flowchart symbol,
			"FlowchartMerge" : 82, #Merge flowchart symbol,
			"FlowchartMultidocument" : 68, #Multi-document flowchart symbol,
			"FlowchartOfflineStorage" : 139, #Offline storage flowchart symbol,
			"FlowchartOffpageConnector" : 74, #Off-page connector flowchart symbol,
			"FlowchartOr" : 78, #"Or" flowchart symbol,
			"FlowchartPredefinedProcess" : 65, #Predefined process flowchart symbol,
			"FlowchartPreparation" : 70, #Preparation flowchart symbol,
			"FlowchartProcess" : 61, #Process flowchart symbol,
			"FlowchartPunchedTape" : 76, #Punched tape flowchart symbol,
			"FlowchartSequentialAccessStorage" : 85, #Sequential access storage flowchart symbol,
			"FlowchartSort" : 80, #Sort flowchart symbol,
			"FlowchartStoredData" : 83, #Stored data flowchart symbol,
			"FlowchartSummingJunction" : 77, #Summing junction flowchart symbol,
			"FlowchartTerminator" : 69, #Terminator flowchart symbol,
			"FoldedCorner" : 16, #사각형(모서리접힘)Folded corner,
			"Frame" : 158, #Rectangular picture frame,
			"Funnel" : 174, #Funnel,
			"Gear6" : 172, #Gear with six teeth,
			"Gear9" : 173, #Gear with nine teeth,
			"HalfFrame" : 159, #Half of a rectangular picture frame,
			"Heart" : 21, #하트, Heart,
			"Heptagon" : 145, #Heptagon,
			"Hexagon" : 10, #육각형, Hexagon,
			"HorizontalScroll" : 102, #Horizontal scroll,
			"IsoscelesTriangle" : 7, #이등변삼각형, Isosceles triangle,
			"LeftArrow" : 34, #화살표(왼쪽)Block arrow that points left,
			"LeftArrowCallout" : 54, #Callout with arrow that points left,
			"LeftBrace" : 31, #중괄호(왼쪽)Left brace,
			"LeftBracket" : 29, #대괄호(왼쪽)Left bracket,
			"LeftCircularArrow" : 176, #Circular arrow pointing counter-clockwise,
			"LeftRightArrow" : 37, #화살표(왼쪽오른쪽)Block arrow with arrowheads that point both left and right,
			"LeftRightArrowCallout" : 57, #Callout with arrowheads that point both left and right,
			"LeftRightCircularArrow" : 177, #Circular arrow pointing clockwise and counter-clockwise; a curved arrow with points at both ends,
			"LeftRightRibbon" : 140, #Ribbon with an arrow at both ends,
			"LeftRightUpArrow" : 40, #화살표(상/좌/우)Block arrow with arrowheads that point left, right, and up,
			"LeftUpArrow" : 43, #화살표(왼쪽위쪽)Block arrow with arrowheads that point left and up,
			"LightningBolt" : 22, #번개, Lightning bolt,
			"LineCallout1" : 109, #Callout with border and horizontal callout line,
			"LineCallout1AccentBar" : 113, #Callout with horizontal accent bar,
			"LineCallout1BorderandAccentBar" : 121, #Callout with border and horizontal accent bar,
			"LineCallout1NoBorder" : 117, #Callout with horizontal line,
			"LineCallout2" : 110, #Callout with diagonal straight line,
			"LineCallout2AccentBar" : 114, #Callout with diagonal callout line and accent bar,
			"LineCallout2BorderandAccentBar" : 122, #Callout with border, diagonal straight line, and accent bar,
			"LineCallout2NoBorder" : 118, #Callout with no border and diagonal callout line,
			"LineCallout3" : 111, #Callout with angled line,
			"LineCallout3AccentBar" : 115, #Callout with angled callout line and accent bar,
			"LineCallout3BorderandAccentBar" : 123, #Callout with border, angled callout line, and accent bar,
			"LineCallout3NoBorder" : 119, #Callout with no border and angled callout line,
			"LineCallout4" : 112, #Callout with callout line segments forming a U-shape,
			"LineCallout4AccentBar" : 116, #Callout with accent bar and callout line segments forming a U-shape,
			"LineCallout4BorderandAccentBar" : 124, #Callout with border, accent bar, and callout line segments forming a U-shape,
			"LineCallout4NoBorder" : 120, #Callout with no border and callout line segments forming a U-shape,
			"LineInverse" : 183, #Line inverse,
			"MathDivide" : 166, #Division symbol ÷,
			"MathEqual" : 167, #Equivalence symbol =,
			"MathMinus" : 164, #Subtraction symbol -,
			"MathMultiply" : 165, #Multiplication symbol x,
			"MathNotEqual" : 168, #Non-equivalence symbol ≠,
			"MathPlus" : 163, #Addition symbol +,
			"Mixed" : -2, #Return value only; indicates a combination of the other states.,
			"Moon" : 24, #달, Moon,
			"NonIsoscelesTrapcoloroid" : 143, #Trapcoloroid with asymmetrical non-parallel sides,
			"NoSymbol" : 19, #"No" symbol,
			"NotchedRightArrow" : 50, #Notched block arrow that points right,
			"NotPrimitive" : 138, #Not supported,
			"Octagon" : 6, #팔각형, Octagon,
			"Oval" : 9, #타원형, Oval,
			"OvalCallout" : 107, #Oval-shaped callout,
			"Parallelogram" : 2, #평행사변형, Parallelogram,
			"Pentagon" : 51, #Pentagon,
			"Pie" : 142, #Circle ('pie') with a portion missing,
			"PieWedge" : 175, #Quarter of a circular shape,
			"Plaque" : 28, #Plaque,
			"PlaqueTabs" : 171, #Four quarter-circles defining a rectangular shape,
			"QuadArrow" : 39, #화살표(사방)Block arrows that point up, down, left, and right,
			"QuadArrowCallout" : 59, #Callout with arrows that point up, down, left, and right,
			"Rectangle" : 1, #사각형, Rectangle,
			"RectangularCallout" : 105, #Rectangular callout,
			"RegularPentagon" : 12, #5각형, Pentagon,
			"RightArrow" : 33, #화살표(오른쪽)Block arrow that points right,
			"RightArrowCallout" : 53, #Callout with arrow that points right,
			"RightBrace" : 32, #중괄호(오른쪽)Right brace,
			"RightBracket" : 30, #대괄호(오른쪽)Right bracket,
			"RightTriangle" : 8, #직각삼각형, Right triangle,
			"Round1Rectangle" : 151, #Rectangle with one rounded corner,
			"Round2DiagRectangle" : 157, #Rectangle with two rounded corners, diagonally-opposed,
			"Round2SameRectangle" : 152, #Rectangle with two-rounded corners that share a side,
			"RoundedRectangle" : 5, #Rounded rectangle,
			"RoundedRectangularCallout" : 106, #Rounded rectangle-shaped callout,
			"SmileyFace" : 17, #웃는얼굴, Smiley face,
			"Snip1Rectangle" : 155, #Rectangle with one snipped corner,
			"Snip2DiagRectangle" : 157, #Rectangle with two snipped corners, diagonally-opposed,
			"Snip2SameRectangle" : 156, #Rectangle with two snipped corners that share a side,
			"SnipRoundRectangle" : 154, #사각형(둥근모서리)Rectangle with one snipped corner and one rounded corner,
			"SquareTabs" : 170, #Four small squares that define a rectangular shape,
			"StripedRightArrow" : 49, #Block arrow that points right with stripes at the tail,
			"Sun" : 23, #해, Sun,
			"SwooshArrow" : 178, #Curved arrow,
			"Tear" : 160, #Water droplet,
			"Trapcoloroid" : 3, #사다리꼴, Trapcoloroid,
			"UpArrow" : 35, #화살표(위쪽)Block arrow that points up,
			"UpArrowCallout" : 55, #Callout with arrow that points up,
			"UpDownArrow" : 38, #화살표(위쪽아래쪽)Block arrow that points up and down,
			"UpDownArrowCallout" : 58, #Callout with arrows that point up and down,
			"UpRibbon" : 97, #Ribbon banner with center area above ribbon ends,
			"UTurnArrow" : 42, #화살표(U턴)Block arrow forming a U shape,
			"VerticalScroll" : 101, #Vertical scroll,
			"Wave" : 103, #Wave,

			}
			result = original_data[input_data]

			return result

	def orientation(self, input_data):
			original_data = {
			"bottom" : -4170,		"horizontal" : -4128,		"up" : -4171,
			"vertical" : -4166,		"downward" : -4170, 		"upward" : -4171,
			}
			result = original_data[input_data]

			return result
