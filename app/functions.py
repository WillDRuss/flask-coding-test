import json
import requests
import copy
import math

def get_stores():
    '''
    Returns: an alphabetical list of stores with corresponding postcodes
    '''
    with open('app/stores.json', 'r') as stores_json:
        data = stores_json.read()
    stores = json.loads(data)
    stores_ordered = sorted(stores, key=lambda k: k['name'])
    return stores_ordered


def postcode_api_call(postcode):
    '''
    Makes a call to the postcodes.io api
    Parameters: a UK postcode string
    Returns: a python dict containing the JSON data returned by the api
    '''
    if isinstance(postcode, str):
        postcode = postcode.replace(' ', '%20')
        main_api = 'http://api.postcodes.io/postcodes/'
        url = main_api+postcode
        json_data = requests.get(url).json()
        return json_data
    else:
        return {'status': 404, 'error': 'Invalid postcode'}

    
def get_lat_and_lon(postcode):
    '''
    return the latitude and longitude for a given postcode using postcodes.io
    Parameters: a UK postcode string
    Returns: a tuple (lat, lon)
    '''
    json_data = postcode_api_call(postcode)
    if json_data['status'] == 200:
        latitude = json_data['result']['latitude']
        longitude = json_data['result']['longitude']
    else:
        latitude = float('nan')
        longitude = float('nan')
    return (latitude, longitude)


def add_lat_and_lon(stores_list):
    '''
    Looks up the latitude and longitude for each store postcode
    Parameters: a list of stores, each store is a dict of name and postcode
    Returns: a new list of stores, with lat and long added to each store dict
    '''
    stores = copy.deepcopy(stores_list)
    for store in stores:
        postcode = store['postcode']
        lat, lon = get_lat_and_lon(postcode)
        store['latitude'] = lat
        store['longitude'] = lon
    return stores


all_stores = add_lat_and_lon(get_stores())


def calc_distance(lat1, lon1, lat2, lon2):
    '''
    Calculates the straight line distance between 2 points using haversine formula
    Parameters: latitude and longitude of 2 points in degrees (floats)
    Returns: the distance in kilometers (float)
    '''
    R = 6371
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lat_diff = math.radians(lat2 - lat1)
    lon_diff = math.radians(lon2 - lon1)

    a = ((math.sin((lat_diff)/2))**2 
         + math.cos(lat1_rad) * math.cos(lat2_rad) * (math.sin((lon_diff)/2))**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return round(d,2)


def find_stores(postcode, radius, stores_list=all_stores):
    '''
    Find the stores within a given radius of a UK postcode
    Parameters: UK postcode (string), radius in km (float), list of stores
    Returns: list of stores ordered from highest to lowest by latitude
    '''
    lat1, lon1 = get_lat_and_lon(postcode)
    if math.isnan(lat1) or math.isnan(lon1):
        return 'Invalid postcode'
    else:
        stores_in_radius = []
        for store in stores_list:
            lat2 = store['latitude']
            lon2 = store['longitude']
            if calc_distance(lat1, lon1, lat2, lon2) < radius:
                stores_in_radius.append(store)
            else:
                pass
        stores_north_to_south = sorted(
            stores_in_radius, 
            key=lambda k: k['latitude'], 
            reverse=True
            )
        return stores_north_to_south





