import requests
import sys

API_TOKEN =

class Station:
    def __init__(self, name, uid):
        self.name = name
        self.uid = uid

def get_stations(coord_1, coord_2):
    res = requests.get(
        f'http://api.waqi.info/map/bounds?token={API_TOKEN}&latlng={coord_1[0]},{coord_1[1]},{coord_2[0]},{coord_2[1]}')

    if res.status_code != 200:
        print('Error:', res.status_code)
        sys.exit(1)
    
    station_data = res.json()['data']
    stations = []
    for item in station_data:
        station = Station(item['station']['name'], item['uid'])
        stations.append(station)
    return stations


def get_station_pm25(station_id):
    res = requests.get(
        f'http://api.waqi.info/feed/@{station_id}/?token={API_TOKEN}')

    if res.status_code != 200:
        print('Error:', res.status_code)
        sys.exit(1)

    station_data = res.json()['data']
    pm25 = station_data['iaqi']['pm25']['v']
    return pm25


if len(sys.argv) < 5:
    print('Usage: air-pollutant.py <lat1> <long1> <lat2> <long2> [sample_period (minutes)] [sample_rate (minutes)]')
    sys.exit(1)

stations = get_stations((float(sys.argv[1]), float(sys.argv[2])), (float(sys.argv[3]), float(sys.argv[4])))
readings  = []

for station in stations:
    pm25 = get_station_pm25(station.uid)
    readings.append(pm25)
    print(f'{station.name}: {pm25}')

print(f'Average: {sum(readings) / len(readings)}')