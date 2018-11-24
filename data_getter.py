from sender import get_data
import requests as re
import json
API_KEY = 'cdQh8jFpdGn8dzsgZ8kS3H7bpeJxCnfFn77VQM79EubXtsBY9cuxtvztJUyP4377'

g_bookings: list
g_stations: dict
g_routes: list
data_gen = None

local = True


def get_bookings() -> list:
	headers = {'x-api-key': API_KEY}
	url = 'https://qocojunction2018.northeurope.cloudapp.azure.com/bookings'
	return re.get(url, headers=headers).json()


def get_stations() -> dict:
	headers = {'x-api-key': API_KEY}
	url = 'https://qocojunction2018.northeurope.cloudapp.azure.com/stations'
	return re.get(url, headers=headers).json()


def get_initial_state():
	global g_bookings, g_stations, g_routes, data_gen

	if local:
		with open("bkgs.txt", 'r') as f:
			g_bookings = json.load(f)
	else:
		g_bookings = get_bookings()

	print("bookings got")

	if local:
		with open("sts.txt", 'r') as f:
			g_stations = json.load(f)
	else:
		g_stations = get_stations()

	print("stations got")

	if local:
		with open('chages0.txt', 'r') as f:
			g_routes = json.load(f)
	else:
		data_gen = get_data()
		g_routes = data_gen.send(None)
	return g_routes


def get_next_step(timer):
	global data_gen

	print("timer: " + str(timer))
	data = data_gen.send(timer)
	print('data got')

	return data
