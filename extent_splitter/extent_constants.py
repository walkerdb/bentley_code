
integers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

def get_written_numbers_dict():
	ones_dict = {
		" one ": "1",
		" two ": "2",
		" three ": "3",
		" four ": "4",
		" five ": "5",
		" six ": "6",
		" seven ": "7",
		" eight ": "8",
		" nine ": "9"
	}

	ones_dict_caps = {
		" One ": "1",
		" Two ": "2",
		" Three ": "3",
		" Four ": "4",
		" Five ": "5",
		" Six ": "6",
		" Seven ": "7",
		" Eight ": "8",
		" Nine ": "9"
	}
	ten_to_nineteen_dict = {
		" ten ": "10",
		" eleven ": "11",
		" twelve ": "12",
		" thirteen ": "13",
		" fourteen ": "14",
		" fifteen ": "15",
		" sixteen ": "16",
		" seventeen ": "17",
		" eighteen ": "18",
		" nineteen ": "19",
		" Ten ": "10",
		" Eleven ": "11",
		" Twelve ": "12",
		" Thirteen ": "13",
		" Fourteen ": "14",
		" Fifteen ": "15",
		" Sixteen ": "16",
		" Seventeen ": "17",
		" Eighteen ": "18",
		" Nineteen ": "19",
	}
	tens_dict = {
		"twenty-": "2",
		"thirty-": "3",
		"forty-": "4",
		"fifty-": "5",
		"sixty-": "6",
		"seventy-": "7",
		"eighty-": "8",
		"ninety-": "9",
		"Twenty-": "2",
		"Thirty-": "3",
		"Forty-": "4",
		"Fifty-": "5",
		"Sixty-": "6",
		"Seventy-": "7",
		"Eighty-": "8",
		"Ninety-": "9"
	}

	full_numbers_dict = {}

	for tens_key, tens_value in tens_dict.items():
		for ones_key, ones_value in ones_dict.items():
			full_numbers_dict[" " + tens_key + ones_key.lstrip(" ")] = tens_value + ones_value

	full_numbers_dict.update(ten_to_nineteen_dict)
	full_numbers_dict.update(ones_dict)
	full_numbers_dict.update(ones_dict_caps)

	return full_numbers_dict

if __name__ == "__main__":
	get_written_numbers_dict()