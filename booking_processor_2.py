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

def update_booking_ways(way):
    global BOOKINGS_WAYS
    pass

def update_graph(way,G):
    new_G = G.copy()
    return new_G


[{}]
if __name__ == "__main__":
    # print(G.edges())
    tmstmps = APIrequests.get_transprt_timestmp()
    #tmstmps = tmstmps.send(None)
    transports = json.loads(tmstmps.text)
    G = addNodes(transports["transports"])
    bookings = json.loads(APIrequests.get_booking().text)
    BOOKINGS_WAYS = {i["booking_id"]:[] for i in bookings}

    for booking in bookings:
        Gst = get_package_graph(booking, G)
        way = deikstra(Gst, booking["origin_station"], booking["destination_station"],
                       datetime.datetime.strptime(booking['booking_date'], '%Y%m%d'))
        update_booking_ways(way)
        G = update_graph(way, Gst)







