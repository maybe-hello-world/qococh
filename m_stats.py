import data_getter
import json
import itertools


changed_data2 = """
{
	"посылка 1": {
		"old": [
		{
			"id": "20181116_brown-ladybug-6",
			"dep_station": "GOT",
			"actual_arr_station": "HEL"
		},
		{
			"id": "20181112_itchy-lion-83",
			"dep_station": "HEL",
			"actual_arr_station": "KBP"
		}],
		"new": [
		{
			"id": "20181116_yellow-gecko-53_A",
			"dep_station": "GOT",
			"actual_arr_station": "ARN"
		},
		{
			"id": "20181116_modern-goose-66",
			"dep_station": "ARN",
			"actual_arr_station": "HEL"
		},
		{
			"id": "20181112_itchy-lion-83",
			"dep_station": "HEL",
			"actual_arr_station": "KBP"
		}],
		"arrival_time": "2018-11-24T03:00:00"
	}
}
"""


def recalculate_stats(t):
	global changed_data
	changed_data = json.loads(changed_data2)

	old_e = list(itertools.chain.from_iterable([changed_data[i]['old'] for i in changed_data]))
	new_e = list(itertools.chain.from_iterable([changed_data[i]['new'] for i in changed_data]))

	old_e = [i for i in old_e if i not in new_e]

	return old_e, new_e



if __name__ == '__main__':
	print(recalculate_stats(None))
