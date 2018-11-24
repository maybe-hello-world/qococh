import APIrequests
import datetime
import json

debug = True

def get_data():
    time = '2018-11-19T00:00:00'
    old_r = []
    changes_to_show = {}
    step = 0
    itera = 0
    time_tracker = 0
    while True:
        cur_tracker = 0
        if step is not None and step != 0:
            datetime_object = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
            time = str(datetime.timedelta(seconds=int(step)) + datetime_object)
            time = time[:10]+'T'+time[11:]
            print(time)

        if debug:
            s = []
            while cur_tracker < step // 3600:
                with open("routes_data/data{}".format(time_tracker)) as f:
                    print('Reading file #{}'.format(time_tracker))
                    r = json.load(f)
                time_tracker += 1
                cur_tracker += 1
                s.extend(r)
            r = {"transports": s}
        else:
            r = APIrequests.get_transprt_timestmp(time)
            r = json.loads(r.text)


        tosent = []
        for i in r['transports']:
            if i not in old_r and i["actual_arr_datetime"] is None:
                tosent.append(i)
        # if tosent:
        #     with open(r"staff/chages" + str(itera) + ".txt", 'w') as f:
        #         json.dump(tosent, f)
        itera += 1
        for i1 in range(len(old_r) - 1):
            i = old_r[i1]
            for j1 in range(len(tosent)):  # replace old_r for tosent and move adding
                j = tosent[j1]
                if i['transport_number'] == j['transport_number']:
                    for k in i:
                        if i[k] != j[k]:
                            if str(k) + ': ' + str(i[k]) + ' - ' + str(j[k]) not in changes_to_show:
                                print(i['transport_number'], end=' :')
                                print('   ' + str(k) + ': ' + str(i[k]) + ' - ' + str(j[k]))
                                changes_to_show[str(k) + ': ' + str(i[k]) + ' - ' + str(j[k])] = 1
                                if ((k == "actual_arr_time") or (k == "actual_dep_time")) and (j[k] is not None):
                                    del tosent[j1]
        old_r += tosent
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
