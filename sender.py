import APIrequests
import datetime
import json

def get_data():
	time = '2018-11-19T00:00:00'
	old_r = []
	changes_to_show = {}
	step = 0
	itera = 0
	while True:
		if step is not None and step != 0:
			datetime_object = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
			time = str(datetime.timedelta(seconds=int(step)) + datetime_object)
			time = time[:10]+'T'+time[11:]
		r = APIrequests.get_transprt_timestmp(time)
		#print("got inf from {}".format(time))
		r = json.loads(r.text)
		tosent = []
		for i in r['transports']:
			if i not in old_r:
				tosent.append(i)
		old_r += tosent
		# if tosent:
		#     with open(r"staff/chages" + str(itera) + ".txt", 'w') as f:
		#         json.dump(tosent, f)
		itera += 1
		for i1 in range(len(old_r)-1):
			i = old_r[i1]
			for j1 in range(i1+1,len(old_r)):
				j = old_r[j1]
				if i['transport_number'] == j['transport_number']:
					for k in i:
						if i[k] != j[k]:
							if str(k) + ': ' + str(i[k]) + ' - ' +str(j[k]) not in changes_to_show:
								print(i['transport_number'], end=' :')
								print('   ' + str(k) + ': ' + str(i[k]) + ' - ' +str(j[k]))
								changes_to_show[str(k) + ': ' + str(i[k]) + ' - ' +str(j[k])] = 1

		step = yield (tosent)


if __name__ == "__main__":
	g = get_data()
	to = 50

	res = g.send(None)
	print('0: ' + str(res)[:to])

	h = 0
	with open("routes_data/data{}".format(h), 'w') as f:
		json.dump(res, f)

	step = 3600

	while True:
		res = g.send(step)
		h += 1
		print(h, len(res))
		with open("routes_data/data{}".format(h), 'w') as f:
			json.dump(res, f)
