import networkx as nx
import datetime
import APIrequests
import json
from booking_processor import *

INF_TIME = datetime.datetime.strptime('3018-01-01T00:00:00', '%Y-%m-%dT%H:%M:%S')

transports =[
    {
        "mode": "T",
        "transport_number": "20181112_lucky-moth-42",
        "dep_station": "ORD",
        "scheduled_arr_station": "JFK",
        "actual_arr_station": "JFK",
        "scheduled_dep_datetime": "2018-01-01T14:00:00",
        "scheduled_arr_datetime": "2018-01-02T14:00:00",
        "estimated_dep_datetime": "2018-01-01T14:00:00",
        "estimated_arr_datetime": "2018-01-02T14:00:00",
        "actual_dep_datetime": "2018-01-02T14:00:00",
        "actual_arr_datetime": None,
        "capacity_volume": 111.81,
        "capacity_weight": 50823.89,
        "cancelled": False
    },
    {
        "mode": "T",
        "transport_number": "20181112_lucky-moth-43",
        "dep_station": "ORD",
        "scheduled_arr_station": "MSK",
        "actual_arr_station": "MSK",
        "scheduled_dep_datetime": "2018-01-01T14:00:00",
        "scheduled_arr_datetime": "2018-01-06T14:00:00",
        "estimated_dep_datetime": "2018-01-01T14:00:00",
        "estimated_arr_datetime": "2018-01-06T14:00:00",
        "actual_dep_datetime": "2018-01-06T14:00:00",
        "actual_arr_datetime": None,
        "capacity_volume": 111.81,
        "capacity_weight": 50823.89,
        "cancelled": False
    },
    {
        "mode": "T",
        "transport_number": "20181112_lucky-moth-123",
        "dep_station": "JFK",
        "scheduled_arr_station": "MSK",
        "actual_arr_station": "MSK",
        "scheduled_dep_datetime": "2018-01-02T14:00:00",
        "scheduled_arr_datetime": "2018-01-03T14:00:00",
        "estimated_dep_datetime": "2018-01-02T14:00:00",
        "estimated_arr_datetime": "2018-01-03T14:00:00",
        "actual_dep_datetime": "2018-01-03T14:00:00",
        "actual_arr_datetime": None,
        "capacity_volume": 111.81,
        "capacity_weight": 50823.89,
        "cancelled": False
    },

    {
        "mode": "T",
        "transport_number": "20181112_lucky-moth-46",
        "dep_station": "JFK",
        "scheduled_arr_station": "MSK",
        "actual_arr_station": "MSK",
        "scheduled_dep_datetime": "2018-01-03T14:00:00",
        "scheduled_arr_datetime": "2018-01-06T14:00:00",
        "estimated_dep_datetime": "2018-01-03T14:00:00",
        "estimated_arr_datetime": "2018-01-06T14:00:00",
        "actual_dep_datetime": "2018-01-03T14:00:00",
        "actual_arr_datetime": None,
        "capacity_volume": 111.81,
        "capacity_weight": 50823.89,
        "cancelled": False
    },
{
        "mode": "T",
        "transport_number": "20181112_lucky-moth-45",
        "dep_station": "ORD",
        "scheduled_arr_station": "MSK",
        "actual_arr_station": "MSK",
        "scheduled_dep_datetime": "2018-01-02T14:00:00",
        "scheduled_arr_datetime": "2018-01-04T14:00:00",
        "estimated_dep_datetime": "2018-01-02T14:00:00",
        "estimated_arr_datetime": "2018-01-04T14:00:00",
        "actual_dep_datetime": "2018-01-02T14:00:00",
        "actual_arr_datetime": None,
        "capacity_volume": 111.81,
        "capacity_weight": 50823.89,
        "cancelled": False
    }
]

def addNodes(transports):
    G = nx.MultiDiGraph()
    for item in transports:
        G.add_edge(item["dep_station"], item["actual_arr_station"], data=item, key=item["transport_number"])
    return G





# print("as".format(G))
def get_package_graph(booking, G):
    new_G = G.copy()
    for i in G.edges.data():
        if (i[2]["data"]["capacity_volume"] < booking["total_volume"])\
            or (i[2]["data"]["capacity_weight"] < booking["total_weight"])\
            or (i[2]["data"]["cancelled"] == True):
                new_G.remove_edge(i[2]["data"]["dep_station"], i[2]["data"]["scheduled_arr_station"], key=i[2]["data"]["transport_number"])
    return new_G



def update_graph(way, G, booking):
    #print(G.edges())
    new_G = G.copy()
    l = list(new_G.edges.data())
    dic = {}
    for i in l:
        dic[i[2]["data"]["transport_number"]] = (i[0], i[1])
    for w in way:
        print(new_G[dic[w[0]][0]][dic[w[0]][1]])
        new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_volume"] -= booking["total_volume"]
        new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_weight"] -= booking["total_weight"]
    return new_G

def update_graph_plus(way, G, booking):
    #print(G.edges())
    new_G = G.copy()
    l = list(new_G.edges.data())
    dic = {}
    for i in l:
        dic[i[2]["data"]["transport_number"]] = (i[0], i[1])
    for w in way:
        print("vol of way {}".format(new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_volume"]))
        print("wei of way {}".format(new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_weight"]))
        print("book vol {}".format(booking["total_volume"]))
        print("book wei {}".format(booking["total_weight"]))
        new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_volume"] += booking["total_volume"]
        new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_weight"] += booking["total_weight"]
        print("vol of way {}".format(new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_volume"]))
        print("wei of way {}".format(new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_weight"]))
    return new_G

def canceled_bookings(bookings_list, G):
    for i in bookings_list:
        # i - booking id
        # bookings_list[i][old] - old ways way[0] - name way w[1] - time way
        # bookings_list[i][new] - new ways
        # boking_item bookings_list[i][booking]
        #booking_v = list(filter(lambda x: x["booking_id"] == i,bookings))
        if bookings_list[i]["old"]:
            G = update_graph_plus(bookings_list[i]["old"], G, bookings_list[i]["booking"])
        if bookings_list[i]["new"]:
            G = update_graph_minus(bookings_list[i]["new"], G, bookings_list[i]["booking"])
    return G

def update_graph_minus(way, G, booking):
    #print(G.edges())
    new_G = G.copy()
    l = list(new_G.edges.data())
    dic = {}
    for i in l:
        dic[i[2]["data"]["transport_number"]] = (i[0], i[1])
    for w in way:
        # print(new_G[dic[w[0]][0]][dic[w[0]][1]])
        new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_volume"] -= booking["total_volume"]
        new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_weight"] -= booking["total_weight"]
    return new_G


if __name__ == "__main__":
    # print(G.edges())
    tmstmps = APIrequests.get_transprt_timestmp()
    #tmstmps = tmstmps.send(None)
    transports = json.loads(tmstmps.text)
    G = addNodes(transports["transports"])
    bookings = json.loads(APIrequests.get_booking().text)
    BOOKINGS_WAYS = {i["booking_id"]:[] for i in bookings}

    for booking in bookings:
        input("Horay, next booking")
        Gst = get_package_graph(booking, G)
        #print(Gst.edges())
        way = deikstra(Gst, booking["origin_station"], booking["destination_station"],
                       datetime.datetime.strptime(booking['booking_date'], '%Y%m%d'))
        #print(Gst.edges())
        BOOKINGS_WAYS[booking["booking_id"]] = way
        G = update_graph(way, G, booking)
        print(BOOKINGS_WAYS)







