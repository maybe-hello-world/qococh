import APIrequests
import datetime

def get_data():
    time = '2018-11-19T00:00:00'
    old_r = []
    while(True):
        r = APIrequests.get_transprt_timestmp(time)
        tosent = []
        for i in r:
            if i not in old_r:
                tosent.append(i)
        old_r = tosent
        step = yield (tosent)
        if step is not None and step != 0:
            datetime_object = datetime.datetime.strptime(time[:10] + ' ' + time[11:], '%Y-%m-%d %H:%M:%S')
            time = str(datetime.timedelta(seconds=int(step)) + datetime_object)



if __name__ == "__main__":
    g = get_data()
    print('0: ' + str(g.send(None))[:10])
    print("1: " + str(g.send(60))[:10])
    print("2: " + str(g.send(1))[:10])