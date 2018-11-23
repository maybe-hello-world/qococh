import APIrequests
import datetime
import json

def get_data():
    time = '2018-11-19T00:00:00'
    old_r = []
    while(True):
        r = APIrequests.get_transprt_timestmp(time)
        r = json.loads(r.text)
        tosent = {}
        for i in r:
            if i not in old_r:
                tosent[i] = r[i]
        old_r = tosent
        step = yield (tosent)
        if step is not None and step != 0:
            datetime_object = datetime.datetime.strptime(time[:10] + ' ' + time[11:], '%Y-%m-%d %H:%M:%S')
            time = str(datetime.timedelta(seconds=int(step)) + datetime_object)



if __name__ == "__main__":
    g = get_data()
    to = 50
    print('0: ' + str(g.send(None))[:to])
    print("1: " + str(g.send(1))[:to])
    print("2: " + str(g.send(1))[:to])