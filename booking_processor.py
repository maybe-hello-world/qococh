import networkx as nx
import datetime
import APIrequests
import json

INF_TIME = datetime.datetime.strptime('3018-01-01T00:00:00', '%Y-%m-%dT%H:%M:%S')

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

def deikstra (G, start_node, stop_node, dep_time):
    dist = dict()
    min_paths ={}
    dist[start_node] = dep_time
    for item in G.nodes():
        if item != start_node:
            dist[item] = INF_TIME
    visited = set()
    while len(visited) < len(G.nodes) -1:
        min_ind = find_unvisited_min(dist, visited)
        if min_ind==0: break
        visited.add(min_ind)
        neighbours = G.adj[min_ind].keys()

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



def update_bookings (booking_ways, G, bad_transports, cur_date, bookings):
    # get actual ways, new graph, bad_transports, and curruent date and
    dict_changes = {}
    for ke in booking_ways:
        # ke - name of booking
        # booking_ways[ke] - list of ()
        # for i in booking_ways[ke]:
        if any(l[0] in bad_transports for l in booking_ways[ke]["ways"]):
            path_to_replace = [i[0] for i in (filter(lambda x: (datetime.datetime.strptime(x[1], '%Y-%m-%dT%H:%M:%S') >=  cur_date), booking_ways[ke]["ways"]))]
        else:
            path_to_replace= []
        if path_to_replace:
            booking_to_change = booking_ways[ke]["obj"]
            begin_with = list(filter(lambda x: (datetime.datetime.strptime(x[1], '%Y-%m-%dT%H:%M:%S') <  cur_date),booking_ways[ke]["ways"]))
            if begin_with:
                last_tr_id = begin_with[-1][0]
                last_transport=0
                for d in G.edges.data():
                    if d[2]["data"]["transport_number"]==last_tr_id:
                        last_transport = d
                        break
            else:
                last_transport = {}
                last_transport["actual_arr_station"] = booking_to_change["origin_station"]
                last_transport["scheduled_arr_datetime"] = datetime.datetime.strptime(booking_to_change["booking_date"], '%Y%m%d')
            adopt_G = get_package_graph(booking = booking_to_change, G = G)
            ends_with = deikstra(adopt_G, last_transport["actual_arr_station"],booking_to_change["destination_station"], last_transport["scheduled_arr_datetime"])
            new_path = begin_with + ends_with
            dict_changes[ke] ={ "old": booking_ways[ke]["ways"], "new" : new_path, "booking" : booking_to_change}
    return dict_changes


##############################################liubias
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
    dic = {}
    for i in new_G.edges.data():
        dic[i[2]["data"]["transport_number"]] = (i[0], i[1])
    for w in way:
        new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_volume"] -= booking["total_volume"]
        new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_weight"] -= booking["total_weight"]
    return new_G

def update_graph_plus(way, G, booking):
    #print(G.edges())
    new_G = G.copy()
    dic = {}
    for i in new_G.edges.data():
        dic[i[2]["data"]["transport_number"]] = (i[0], i[1])
    for w in way:
        # print("vol of way {}".format(new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_volume"]))
        # print("wei of way {}".format(new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_weight"]))
        # print("book vol {}".format(booking["total_volume"]))
        # print("book wei {}".format(booking["total_weight"]))
        new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_volume"] += booking["total_volume"]
        new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_weight"] += booking["total_weight"]
        # print("vol of way {}".format(new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_volume"]))
        # print("wei of way {}".format(new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_weight"]))
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
    dic = {}
    for i in new_G.edges.data():
        dic[i[2]["data"]["transport_number"]] = (i[0], i[1])
    for w in way:
        # print(new_G[dic[w[0]][0]][dic[w[0]][1]])
        new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_volume"] -= booking["total_volume"]
        new_G[dic[w[0]][0]][dic[w[0]][1]][w[0]]["data"]["capacity_weight"] -= booking["total_weight"]
    return new_G




