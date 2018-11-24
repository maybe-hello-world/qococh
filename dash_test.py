import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event, State
import dash_table_experiments as dte
import visdcc
import datetime
import pickle
import os

import booking_processor
import data_getter
import m_stats

from mercator import lat_to_mercator, long_to_mercator

debug = False


MAP_WIDTH = 1433
MAP_HEIGHT = 930

PAGE_SIZE = 100

g_avg_h = 0
g_avg_i = 0
G = None
BOOKINGS_WAYS = None
bookings = None


external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/vis/4.20.1/vis.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

transports = data_getter.get_initial_state()
# edges = [{'id': i['transport_number'], 'from': i['dep_station'], 'to': i['actual_arr_station']} for i in edges]
edges = []


def init():
	global G, bookings, BOOKINGS_WAYS
	G = booking_processor.addNodes(transports)
	bookings = data_getter.g_bookings
	BOOKINGS_WAYS = {i["booking_id"]: {"ways": [], "obj": i} for i in bookings}

	i = 0
	print("Initial state calculation started, len of bookings: {}".format(len(bookings)))

	if os.path.exists("G") and os.path.exists("BOOKINGS_WAYS"):
		with open("G", 'r') as f:
			G = pickle.load(f)
		with open("BOOKINGS_WAYS", 'r') as f:
			BOOKINGS_WAYS = pickle.load(f)
		print("G and BOOKINGS_WAYS loaded from disk")
	else:
		for booking in bookings:
			i += 1
			print("Booking #{}".format(i))
			Gst = booking_processor.get_package_graph(booking=booking, G=G)

			way = booking_processor.deikstra(Gst, booking["origin_station"], booking["destination_station"],
						   datetime.datetime.strptime(booking['booking_date'], '%Y%m%d'))
			BOOKINGS_WAYS[booking["booking_id"]]["ways"] = way
			if way:
				G = booking_processor.update_graph(way, G, booking)

	try:
		with open("G", 'w') as f:
			pickle.dump(G, f)
		print("G dumped")

		with open("BOOKINGS_WAYS", 'w') as f:
			pickle.dump(BOOKINGS_WAYS, f)
		print("BOOKINGS_WAYS saved")
	except Exception:
		print("Couldn't save")

	print("Initial state calculated")


init()

stations = {x: (data_getter.g_stations[x]['name'], data_getter.g_stations[x]['location']) for x in data_getter.g_stations.keys()}
stations = [{
	'id': k,
	'label': k,
	'y': lat_to_mercator(v[1]['latitude'], MAP_HEIGHT, MAP_WIDTH),
	'x': long_to_mercator(v[1]['longitude'], MAP_WIDTH)}
	for k, v in stations.items()]

undeliverable = {}

app.layout = html.Div([
	html.Div([
		html.Div([
			html.Div([
			dcc.RadioItems(
				id='radioBtn',
				options=[
					{'label': '1h', 'value': 1},
					{'label': '6h', 'value': 6},
					{'label' : '12h', 'value': 12},
					{'label' : '1 day', 'value': 24}
				],
				value=1
			),
				html.Div([html.Button('Add', id='addBtn')], style={'margin-top': 30})
			], style={ 'margin-bottom': 50}),
			html.Div(id='avgDelivery', style={'white-space': 'pre-wrap', 'text-align':'center', 'font-size': '26pt', 'margin-bottom': 40}),
			html.Div(id='changeDelta', style={'white-space': 'pre-wrap', 'text-align':'center', 'font-size': '26pt'}),
			html.Div(id='nodes', style={'float': 'left','margin-top': '50'}),
			dte.DataTable(
				rows=[{'point': '1'}],
				row_selectable=False,
				editable=False,
				filterable=True,
				sortable=True,
				id='edges-data'
			)
		], style={'width': '19%', 'float': 'left'}),
		html.Div([
		visdcc.Network(
			id='net',
			data={'nodes': stations, 'edges': edges},
			options=dict(
				height='{}px'.format(MAP_HEIGHT),
				width='{}px'.format(MAP_WIDTH),
				physics={
					'enabled': False
				})
	)], style={'width': MAP_WIDTH, 'height' : MAP_HEIGHT,  'float': 'right', 'border-style':'solid' ,'border-width': "0.2px"})]),
	html.Div([
	dte.DataTable(
		rows=[{'undevirable' : 'shipment 1'}, {'undevirable' : 'shipment 2'} ],
		row_selectable=False,
		editable=False,
		filterable=True,
		sortable=True,
		id='undelirevable-data'
	),

	dte.DataTable(
		rows=bookings,
		row_selectable=False,
		editable=False,
		filterable=True,
		sortable=True,
		id='stations'
	)])
], style={})


# selection for nodes
@app.callback(
	Output('nodes', 'children'),
	[Input('net', 'selection')])
def myfun(x):
	s = 'Selected node: '
	if x is not None and len(x['nodes']):
		s += str(x['nodes'])
	return s


# selections for edges
@app.callback(
	Output('edges-data', 'rows'),
	[Input('net', 'selection')])
def myfun(x):
	s=[]
	if x is not None and len(x['edges']):
		s = [{'point': i} for i in x['edges']]
	return s


@app.callback(Output('net', 'data'), [], state=[State('radioBtn', 'value')], events=[Event('addBtn', 'click')])
def update_metrics(n):
	global g_avg_h, g_avg_i, G
	# Get changes
	print("N is now: {}".format(n))

	data = {'nodes': stations, 'edges': []}

	n = n * 3600 if n is not None else 0

	if not debug:
		new_data = data_getter.get_next_step(n)
	else:
		new_data = 1

	if new_data is not None and new_data:
		if not debug:
			G, bad_transports = booking_processor.update_tranp_graph(G, new_data)
			list_to_change = booking_processor.update_bookings(BOOKINGS_WAYS, G, bad_transports,
								datetime.datetime.strptime('2018-01-01T10:00:00', '%Y-%m-%dT%H:%M:%S'), bookings)
			G = booking_processor.canceled_bookings(list_to_change, G)
			for i in list_to_change:
				BOOKINGS_WAYS[i]["ways"] = i["new"]
		else:
			changes = None

		old_edges, new_edges, stats = m_stats.recalculate_stats(list_to_change)
		g_avg_h, g_avg_i = stats['avg_h'], stats['avg_i']

		old_edges = [{
			'id': i['id'],
			'from': i['dep_station'],
			'to': i['actual_arr_station'],
			'arrows': 'to',
			'dashes': True
		} for i in old_edges]
		new_edges = [{
			'id': i['id'],
			'from': i['dep_station'],
			'to': i['actual_arr_station'],
			'arrows': 'to'
		} for i in new_edges]

		old_edges.extend(new_edges)

		data['edges'] = old_edges

	return data


@app.callback(Output('avgDelivery', 'children'), [Input('net', 'data')])
def statistics_return(x):
	return 'Avg delivery time (hours)'+'\n' + "{0:.1f}".format(g_avg_h)

@app.callback(Output('changeDelta', 'children'), [Input('net', 'data')])
def statistics_return(x):
	return 'Avg delay (hours)'+'\n' + "{0:.1f}".format(g_avg_i)

if __name__ == '__main__':
	app.run_server(debug=True, use_reloader=False)
