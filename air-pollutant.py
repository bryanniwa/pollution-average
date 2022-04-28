import requests
import sys
import time
from threading import Thread, Lock

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


def read_all_stations(stations):
    readings = []
    reading_lock = Lock()

    def read_station(station):
        pm25 = get_station_pm25(station.uid)
        with reading_lock:
            readings.append(pm25)
        print(f'{station.name}: {pm25}')

    threads = []
    for station in stations:
        t = Thread(target=read_station, args=(station,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return readings


if len(sys.argv) < 5:
    print('Usage: air-pollutant.py <lat1> <lng1> <lat2> <lng2> [sample_period (minutes)] [sample_rate (minutes)]')
    sys.exit(1)

lat1, lng1, lat2, lng2 = [float(arg) for arg in sys.argv[1:5]]
sample_period_sec = int(sys.argv[5])*60 if len(sys.argv) > 5 else 5*60
sample_rate_sec = int(sys.argv[6])*60 if len(sys.argv) > 6 else 1*60
read_cycles = (sample_period_sec // sample_rate_sec) + 1

stations = get_stations((lat1, lng1), (lat2, lng2))
readings  = []

for i in range(read_cycles-1):
    print(f'({i+1}/{read_cycles})\n')
    current_readings = read_all_stations(stations)
    readings += current_readings
    print('\n\n')
    time.sleep(sample_rate_sec)

print(f'({read_cycles}/{read_cycles})\n')
current_readings = read_all_stations(stations)
readings += current_readings
print('\n\n')

print(f'Average: {sum(readings) / len(readings)}')