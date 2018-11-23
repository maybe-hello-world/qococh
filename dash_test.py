import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import visdcc
import data_getter

external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/vis/4.20.1/vis.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data_getter.get_initial_state()

stations = {x: data_getter.g_stations[x]['name'] for x in data_getter.g_stations.keys()}
stations = [{'id': k, 'label': v} for k, v in stations.items()]


# 'edges':[{'id':'1-3', 'from': 1, 'to': 3},
# 								{'id': '1-2', 'from': 1, 'to': 2}]

app.layout = html.Div([
	visdcc.Network(
		id='net',
		data={'nodes': stations, 'edges': []},
		options=dict(height='600px', width='100%')),
	dcc.Interval(
		id='interval-component',
		interval=1 * 1000,  # in milliseconds
		n_intervals=0
	)]
)


@app.callback(Output('net', 'options'), [Input('interval-component', 'n_intervals')])
def update_metrics(n):
	# Get changes
	print("N is now: {}".format(n))

	colors = ['red', 'blue', 'green', 'white']

	return {'nodes': {'color': colors[n % 4]}}


if __name__ == '__main__':
	app.run_server(debug=True)
