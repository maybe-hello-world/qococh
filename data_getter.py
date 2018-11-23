from sender import get_data
import requests as re
API_KEY = 'cdQh8jFpdGn8dzsgZ8kS3H7bpeJxCnfFn77VQM79EubXtsBY9cuxtvztJUyP4377'

g_bookings: list
g_stations: dict
g_routes: list
data_gen = None


def get_bookings() -> list:
	headers = {'x-api-key': API_KEY}
	url = 'https://qocojunction2018.northeurope.cloudapp.azure.com/bookings'
	return re.get(url, headers=headers).json()


def get_stations() -> dict:
	headers = {'x-api-key': API_KEY}
	url = 'https://qocojunction2018.northeurope.cloudapp.azure.com/stations'
	return re.get(url, headers=headers).json()


def get_initial_state() -> None:
	global g_bookings, g_stations, g_routes, data_gen

	g_bookings = get_bookings()
	print("bookings got")

	g_stations = get_stations()
	print("stations got")

	data_gen = get_data()
	data_gen.send(None)
	g_routes = data_gen.send(0)


def get_next_step(timer):
	global data_gen

	print("timer: " + str(timer))
	data = data_gen.send(timer)
	print('data got')

	return data
