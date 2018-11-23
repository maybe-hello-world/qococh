import APIrequests
import datetime

def get_data():
    time = '2018-11-19T00:00:00'
    while(True):
        r = APIrequests.get_transprt_timestmp(time)
        step = yield (r)
        if step != None and step != 0:
            datetime_object = datetime.datetime.strptime(time[:10] + ' ' + time[11:], '%Y-%m-%d %H:%M:%S')
            time = str(datetime.timedelta(seconds=int(step)) + datetime_object)



if __name__ == "__main__":
    g = get_data()
    print('0: ' + g.send(None).text[:10])
    print("1: " + g.send(60).text[:10])
    print("2: " + g.send(45).text[:10])