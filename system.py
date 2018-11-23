import time
# from sender import get_data
import requests as re
API_KEY = 'cdQh8jFpdGn8dzsgZ8kS3H7bpeJxCnfFn77VQM79EubXtsBY9cuxtvztJUyP4377'

g_bookings: list
g_stations: dict


def get_bookings() -> list:
	headers = {'x-api-key': API_KEY}
	url = 'https://qocojunction2018.northeurope.cloudapp.azure.com/bookings'
	return re.get(url, headers=headers).json()


def get_stations() -> dict:
	headers = {'x-api-key': API_KEY}
	url = 'https://qocojunction2018.northeurope.cloudapp.azure.com/stations'
	return re.get(url, headers=headers).json()


g_bookings = get_bookings()
g_stations = get_stations()


timer = None
while True:
	pass
	# get new data
	# data = get_data(timer)

	# start timer to countdown our time
	# if data is not None:
	# 	timer = time.perf_counter_ns()
	#
	# 	stats = recount_ways(data)
	# 	visualize_data(stats)
	#
	# 	find out how long we were waiting
		# timer = int((time.perf_counter_ns() - timer) * 10*9)
	# else:
	# 	time.sleep(5)
	# 	timer = 5
