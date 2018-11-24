import math


def long_to_mercator(x, width):
	return (x + 180) * (width/360)


def lat_to_mercator(y, height, width):
	lat_rad = y * math.pi / 180

	merc_n = math.log(math.tan((math.pi/4)+(lat_rad/2)))

	return (height/2)-(width*merc_n/(2*math.pi))
