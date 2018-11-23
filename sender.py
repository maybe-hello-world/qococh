import APIrequests
import datetime
import json

def get_data():
    time = '2018-11-19 00:00:00'
    old_r = []
    step = yield
    while True:
        if step is not None and step != 0:
            datetime_object = datetime.datetime.strptime(time[:10] + ' ' + time[11:], '%Y-%m-%d %H:%M:%S')
            time = str(datetime.timedelta(seconds=int(step)) + datetime_object)
        r = APIrequests.get_transprt_timestmp(time[:10]+'T'+time[11:])
        #print("got inf from {}".format(time))
        r = json.loads(r.text)
        tosent = []
        #print("len of income is {}".format(len(r['transports'])))
        for i in r['transports']:
            if i not in old_r:
                tosent.append(i)
        old_r += tosent
        step = yield (tosent)


if __name__ == "__main__":
    g = get_data()
    to = 50
    print('0: ' + str(g.send(None))[:to])
    for i in range(1, 360000, 10000):
        print(len(g.send(i)))
