import networkx as nx
from booking_processor_2 import *
import datetime
INF_TIME = datetime.datetime.strptime('3018-01-01T00:00:00', '%Y-%m-%dT%H:%M:%S')
bookings = [{
     "booking_id": "empty-crab-97",
     "origin_station": "PEK",
     "destination_station": "GOT",
     "booking_date": "20181116",
     "total_weight": 795,
     "total_volume": 1.25,
     "high_priority": False
 }]
transports =[
    {
        "mode": "T",
        "transport_number": "20181112_lucky-moth-42",
        "dep_station": "ORD",
        "scheduled_arr_station": "JFK",
        "actual_arr_station": "JFK",
        "scheduled_dep_datetime": "2018-01-01T14:00:00",
        "scheduled_arr_datetime": "2018-01-02T13:00:00",
        "estimated_dep_datetime": "2018-01-01T14:00:00",
        "estimated_arr_datetime": "2018-01-02T13:00:00",
        "actual_dep_datetime": "2018-01-01T14:00:00",
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
        "transport_number": "20181112_lucky-moth-46",
        "dep_station": "JFK",
        "scheduled_arr_station": "MSK",
        "actual_arr_station": "MSK",
        "scheduled_dep_datetime": "2018-01-02T16:00:00",
        "scheduled_arr_datetime": "2018-01-03T18:00:00",
        "estimated_dep_datetime": "2018-01-02T16:00:00",
        "estimated_arr_datetime": "2018-01-03T18:00:00",
        "actual_dep_datetime": "2018-01-02T16:00:00",
        "actual_arr_datetime": None,
        "capacity_volume": 111.81,
        "capacity_weight": 50823.89,
        "cancelled": False
    },

    {
        "mode": "T",
        "transport_number": "20181112_lucky-moth-50",
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

BOOKINGS_WAYS = {i["booking_id"]: [] for i in bookings}



def addNodes(transports):
    G = nx.MultiDiGraph()
    for item in transports:
        G.add_edge(item["dep_station"],item["actual_arr_station"], data=item, key=item["transport_number"])
    return G

def find_unvisited_min (dist, visited):
    min_ind = 0
    min_val = INF_TIME
    for i in dist:
        if i not in visited:
            if dist[i] < min_val:
                min_val = dist[i]
                min_ind = i
    return min_ind

def deikstra (G, start_node ,stop_node, dep_time):
    dist = dict()
    min_paths ={}
    dist[start_node] = dep_time
    for item in G.nodes():
        if item != start_node:
            dist[item] = INF_TIME
    visited = set()
    while len(visited) < len(G.nodes) -1:
        min_ind = find_unvisited_min(dist,visited)
        if min_ind==0: break
        visited.add(min_ind)

        neighbours = G.adj[min_ind].keys()
        print('n_list {}: {}'.format(min_ind, list(neighbours)))
        for adj_node in neighbours:
            min_e = 0
            min_time = INF_TIME
            all_edges = G.get_edge_data(min_ind, adj_node)
            for i in all_edges:
                if (datetime.datetime.strptime(all_edges[i]['data']["estimated_arr_datetime"],'%Y-%m-%dT%H:%M:%S') < min_time) \
                        and (datetime.datetime.strptime(G.get_edge_data(min_ind, adj_node)[i]['data']["estimated_dep_datetime"], '%Y-%m-%dT%H:%M:%S') >= dist[min_ind]):
                    min_time = datetime.datetime.strptime(all_edges[i]['data']["estimated_arr_datetime"],'%Y-%m-%dT%H:%M:%S')
                    min_e = i
            adj_edge = (min_ind, adj_node)
            if min_e != 0:
                edj_data = G.get_edge_data(adj_edge[0], adj_edge[1])[min_e]['data']

                dist_delta = datetime.datetime.strptime(edj_data["estimated_arr_datetime"], '%Y-%m-%dT%H:%M:%S')

                if (dist[adj_edge[1]] > dist_delta) :
                    dist[adj_edge[1]] = dist_delta
                    if min_ind in min_paths:
                        min_paths[adj_edge[1]] = min_paths[min_ind] + [(G.get_edge_data(adj_edge[0], adj_edge[1])[min_e]['data']["transport_number"],
                                                                        G.get_edge_data(adj_edge[0], adj_edge[1])[min_e]['data']["estimated_arr_datetime"]
                                                                        )]
                    else:
                        min_paths[adj_edge[1]] = [(G.get_edge_data(adj_edge[0], adj_edge[1])[min_e]['data']["transport_number"], G.get_edge_data(adj_edge[0], adj_edge[1])[min_e]['data']["estimated_arr_datetime"])]
    if stop_node in min_paths:
        return min_paths[stop_node]
    else:
        return []


def update_tranp_graph(G, list_of_changes):
    bad_transports = []
    for item in list_of_changes:
        transp_key = item["transport_number"]
        bad_transports.append(transp_key)
        act_arr = item["actual_arr_station"]
        sch_arr = item["scheduled_arr_station"]
        act_dep = item["dep_station"]
        if (act_arr!=sch_arr) and (G.has_edge(act_dep,sch_arr,transp_key)) :
            G.remove_edge(act_dep,sch_arr,transp_key)
        G.add_edge(act_dep, act_arr, data=item, key=transp_key)
    return (G,bad_transports)
    BOOKINGS_WAYS = {i["booking_id"]:[] for i in bookings}

def update_bookings (booking_ways, G, bad_transports, cur_date):
    #get actual ways, new graph, bad_transports, and curruent date and
    dict_changes ={}
    for ke in booking_ways:
        # ke - name of booking
        # booking_ways[ke] - list of ()
        #for i in booking_ways[ke]:
        if any(l[0] in bad_transports for l in booking_ways[ke]):
            path_to_replace = [i[0] for i in (filter(lambda x: (datetime.datetime.strptime(x[1], '%Y-%m-%dT%H:%M:%S') >=  cur_date), booking_ways[ke]))]
        else:
            path_to_replace= []
        if path_to_replace:
            booking_to_change= list(filter(lambda x: x["booking_id"] == ke, bookings))[0]
            begin_with = filter(lambda x: (datetime.datetime.strptime(x[1], '%Y-%m-%dT%H:%M:%S') <  cur_date))
            last_tr_id = begin_with[-1][0]
            last_transport=0
            for d in G.edges.data():
                if d[2]["data"]["transport_number"]==last_tr_id:
                    last_transport = d
                    break
            adopt_G =get_package_graph(booking_to_change, G)
            ends_with = deikstra(adopt_G, last_transport["actual_arr_station"],booking_to_change["destination_station"] )
            new_path = begin_with + ends_with
            dict_changes[ke] ={ "old": booking_ways[ke], "new" : new_path, "booking" : booking_to_change}
    return dict_changes




if __name__=="__main__":
    G = addNodes(transports)
    print ("============================")
    # G=update_tranp_graph(G, [{"transport_number": "20181112_lucky-moth-42",
    #                               "dep_station": "ORD",
    #                               "scheduled_arr_station": "JFK",
    #                               "actual_arr_station": "QWE"}])
    # print(G.edges(keys=True))
    # print("-0000000000000000")
    # print(G.edges(data=True))

    for d in G.edges.data():
        print("11111111111111111111111111111111")
        if d[2]["data"]["transport_number"] == "20181112_lucky-moth-42":
            print("printing d "+str(d))
   # print(G.edges('ORD', 'JFK', '20181112_lucky-moth-42',data=True))
   #  d=deikstra(G,'ORD','MSK', datetime.datetime.strptime( '2018-01-01T14:00:00', '%Y-%m-%dT%H:%M:%S'))
   #  print(d)





