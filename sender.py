import APIrequests

def get_data():
    time = None
    while(True):
        r = APIrequests.get_transprt_timestmp(time)
        time = yield (r)



if __name__ == "__main__":
    g = get_data()
    print('0: ' + g.send(None).text[:10])
    print("1: " + g.send("2018-11-19T01:00:00").text[:10])
    print("2: " + g.send("2018-11-19T02:00:00").text[:10])