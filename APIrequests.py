import requests as re
import json

def get_booking():
    headers = {'x-api-key': 'cdQh8jFpdGn8dzsgZ8kS3H7bpeJxCnfFn77VQM79EubXtsBY9cuxtvztJUyP4377'}
    url = 'https://qocojunction2018.northeurope.cloudapp.azure.com/bookings'
    return re.get(url,  headers=headers)

def get_transprt_timestmp(time='2018-11-19T00:00:00'):
    headers = {'x-api-key': 'cdQh8jFpdGn8dzsgZ8kS3H7bpeJxCnfFn77VQM79EubXtsBY9cuxtvztJUyP4377'}
    url= 'https://qocojunction2018.northeurope.cloudapp.azure.com/transports'
    parametrs = {'time':time}
    return re.get(url,  headers=headers, params=parametrs)

def get_all_stations():
    headers = {'x-api-key': 'cdQh8jFpdGn8dzsgZ8kS3H7bpeJxCnfFn77VQM79EubXtsBY9cuxtvztJUyP4377'}
    url = 'https://qocojunction2018.northeurope.cloudapp.azure.com/stations'
    return re.get(url,  headers=headers)

if __name__ == "__main__":
    r = get_all_stations()
    print(r)
    print(r.headers)
    print(json.loads(r.text))

