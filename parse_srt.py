def parse_srt(file_name):
	data = {}

	with open(file_name) as f:
		content = f.readlines()
	content = [x.strip() for x in content]

	start_time = ""
	end_time = ""
	key = 0
	lyric = ""
	step = 1
	index = 0
	for i in content:
		try:
			if step == 1:
				key = index
				step = 2
			elif step == 2:
				start_time = i[0:12]
				end_time = i[17:29]
				step = 3
			elif step == 3:
				if i[-1:] == "ª":
					for j in i:
						if (j != "â") and (j != "™") and (j != "ª"):
							if (j != ",") and (j != ".") and (j != "!" and (j != "?")):
								lyric += j.lower()
					step = 4
				elif i[-1:] == ")":
					step = 4
				elif i[0] == "(":
					step = 3
				else:
					for j in i:
						if (j != "â") and (j != "™") and (j != "ª"):
							if (j != ",") and (j != ".") and (j != "!" and (j != "?")):
								lyric += j.lower()
					lyric += " "
					step = 3
			elif step == 4:
				start_time_sec = (float(start_time[0:2])*60.0*60.0) + (float(start_time[3:5])*60.0) + (float(start_time[6:8])) + (float("." + start_time[9:12]))
				end_time_sec = (float(end_time[0:2])*60.0*60.0) + (float(end_time[3:5])*60.0) + (float(end_time[6:8])) + (float("." + end_time[9:12]))
				data[key] = ((start_time_sec, end_time_sec), lyric[1:-1])
				start_time = ""
				end_time = ""
				key = 0
				lyric = ""
				step = 1
				index += 1
		except:
			pass

	return data


if __name__ == '__main__':
	pass
	# data = parse_srt("srt/ryr75N0nki0.srt")

	# # print just a certain line, key is that line
	# print (data[53])

	# # print start time and end time
	# print (data[53][0][0], data[53][0][1])

	# # print lyrics
	# print (data[53][1])
