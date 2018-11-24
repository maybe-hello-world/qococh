import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table_experiments as dte
import visdcc

import data_getter
from mercator import lat_to_mercator, long_to_mercator

MAP_WIDTH = 1024
MAP_HEIGHT = 1000

TIME = 5
PAGE_SIZE = 100


external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/vis/4.20.1/vis.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

edges = data_getter.get_initial_state()
edges = [{'id': i['transport_number'], 'from': i['dep_station'], 'to': i['actual_arr_station']} for i in edges]

stations = {x: (data_getter.g_stations[x]['name'], data_getter.g_stations[x]['location'])  for x in data_getter.g_stations.keys()}
stations = [{
	'id': k,
	'label': v[0],
	'y': lat_to_mercator(v[1]['latitude'], MAP_HEIGHT, MAP_WIDTH) * 10,
	'x': long_to_mercator(v[1]['longitude'], MAP_WIDTH) * 15}
	for k, v in stations.items()]

bookings = data_getter.g_bookings


app.layout = html.Div([
	html.Div([
		html.Div([
			html.Div(id='nodes'),
			html.Div(id='edges')
		], style={'width': '19%', 'display': 'inline-block'}),
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
	)], style={'width': '80%', 'float': 'right', 'display': 'inline-block'})]),
	dte.DataTable(
		rows=bookings,  # initialise the rows
		row_selectable=True,
		filterable=True,
		sortable=True,
		selected_row_indices=[],
		id='datatable'
	)
	,
	dcc.Interval(id='my-interval', interval=1000*1000)
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
	Output('edges', 'children'),
	[Input('net', 'selection')])
def myfun(x):
	s = 'It\'s edges: '
	if x is not None and len(x['edges']):
		s = [s] + [html.Div(i) for i in x['edges']]
	return s


@app.callback(Output('net', 'options'), [Input('my-interval', 'n_intervals')])
def update_metrics(n):
	# Get changes
	print("N is now: {}".format(n))

	if n is None: n = 0

	edges = [
		[{'id': 'someidhere', 'from': 'AGP', 'to': 'ALC'}, {'id': 'someidhhere', 'from': 'ALC', 'to': 'ALF'}],
		[]
	]

	data = {'nodes': stations, 'edges': edges[n % 2]}

	return dict(height='1000px', width='100%')


if __name__ == '__main__':
	app.run_server(debug=True, use_reloader=False)
