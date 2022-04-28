import requests

API_TOKEN =

stations = requests.get(f'http://api.waqi.info/map/bounds?token={API_TOKEN}&latlng=54.17,37.6,54.17,37.6')
print(stations.json())