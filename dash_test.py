import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event, State
import dash_table_experiments as dte
import visdcc

import data_getter
import m_stats
# import booking_processor # TODO
from mercator import lat_to_mercator, long_to_mercator

MAP_WIDTH = 2048
MAP_HEIGHT = 1000

TIME = 5
PAGE_SIZE = 100


external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/vis/4.20.1/vis.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

edges = data_getter.get_initial_state()
# edges = [{'id': i['transport_number'], 'from': i['dep_station'], 'to': i['actual_arr_station']} for i in edges]
edges = []

stations = {x: (data_getter.g_stations[x]['name'], data_getter.g_stations[x]['location'])  for x in data_getter.g_stations.keys()}
stations = [{
	'id': k,
	'label': v[0],
	'y': lat_to_mercator(v[1]['latitude'], MAP_HEIGHT, MAP_WIDTH) * 10,
	'x': long_to_mercator(v[1]['longitude'], MAP_WIDTH) * 15}
	for k, v in stations.items()]

bookings = data_getter.g_routes

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
				html.Div([html.Button('Add', id='addBtn')],style={'margin-top': 30})
			],style={'margin-top': 50, 'margin-bottom': 50}),
			html.Div(id='nodes'),
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
	)], style={'width': '80%', 'float': 'right', 'border': 'solid', 'border-width': '0.5px'})]),
	html.Div([
	dte.DataTable(
		rows=bookings,
		row_selectable=False,
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
])


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
	s = []
	if x is not None and len(x['edges']):
		tmp = [{'point' :i} for i in x['edges']]
		s = tmp
	return s


@app.callback(Output('net', 'data'), [],state=[State('radioBtn','value')],events=[Event('addBtn', 'click')])
def update_metrics(n):
	# Get changes
	print("N is now: {}".format(n))

	data = {'nodes': stations, 'edges': []}

	n = n if n is not None else 0

	# new_data = data_getter.get_next_step(n)
	new_data = 1

	if new_data is not None and new_data:
		# changes = booking_processor.process_changes(new_data)
		changes = None

		old_edges, new_edges = m_stats.recalculate_stats(changes)
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



if __name__ == '__main__':
	app.run_server(debug=True, use_reloader=False)
