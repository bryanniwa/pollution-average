import requests
import sys

API_TOKEN =

def get_station_ids(coord_1, coord_2):
    res = requests.get(
        f'http://api.waqi.info/map/bounds?token={API_TOKEN}&latlng={coord_1[0]},{coord_1[1]},{coord_2[0]},{coord_2[1]}')

    if res.status_code != 200:
        print('Error:', res.status_code)
        sys.exit(1)
    
    station_data = res.json()['data']
    station_ids = [item['uid'] for item in station_data]
    return station_ids


if len(sys.argv) < 5:
    print('Usage: air-pollutant.py <lat1> <long1> <lat2> <long2> [sample_period (minutes)] [sample_rate (minutes)]')
    sys.exit(1)

station_ids = get_station_ids((float(sys.argv[1]), float(sys.argv[2])), (float(sys.argv[3]), float(sys.argv[4])))
print(station_ids)
