import networkx as nx
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
        "transport_number": "20181112_lucky-moth-46",
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



def addNodes(transports):
    G = nx.MultiDiGraph()
    for item in transports:
        G.add_edge(item["dep_station"],item["actual_arr_station"], data=item)
    return G

def find_unvisited_min (dist, visited):
    min_ind =0
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
        visited.add(min_ind)
        neighbours = G.adj[min_ind].keys()
        print('asdf {},{}'.format(min_ind, list(neighbours)))
        for adj_node in neighbours:
            min_e = 0
            min_time = INF_TIME
            all_edges = G.get_edge_data(min_ind, adj_node)
            for i in all_edges:
                if datetime.datetime.strptime(all_edges[i]['data']["estimated_arr_datetime"],'%Y-%m-%dT%H:%M:%S') < min_time:
                    min_time = datetime.datetime.strptime(all_edges[i]['data']["estimated_arr_datetime"],'%Y-%m-%dT%H:%M:%S')
                    min_e = i
            adj_edge = (min_ind, adj_node)
            dist_delta = datetime.datetime.strptime(G.get_edge_data(adj_edge[0], adj_edge[1])[min_e]['data']["estimated_arr_datetime"], '%Y-%m-%dT%H:%M:%S')
            if dist[adj_edge[1]] > dist_delta:
                dist[adj_edge[1]] = dist_delta
                if min_ind in min_paths:
                    min_paths[adj_edge[1]] = min_paths[min_ind] + [(G.get_edge_data(adj_edge[0], adj_edge[1])[min_e]['data']["transport_number"], G.get_edge_data(adj_edge[0], adj_edge[1])[min_e]['data']["estimated_arr_datetime"])]
                else:
                    min_paths[adj_edge[1]] =  [(G.get_edge_data(adj_edge[0], adj_edge[1])[min_e]['data']["transport_number"], G.get_edge_data(adj_edge[0], adj_edge[1])[min_e]['data']["estimated_arr_datetime"])]
    return min_paths[stop_node]

G = addNodes(transports)
#print(G.edges())
d=deikstra(G,'ORD','MSK', datetime.datetime.strptime( '2018-01-01T14:00:00', '%Y-%m-%dT%H:%M:%S'))
print(d)





