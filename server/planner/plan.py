from time import gmtime, strftime
import random
import requests
import json
import geocoder
import rauth
import time

def grabdata(zip):
    list_o_events = ["Movies", "Theater", "Concerts", "Festivals", "Sports"]
    list_o_foods = ["American", "Indian", "Mexican", "Chinese", "Thai"]
    default_time_range = ['2016-05-17T00:00:00', '2016-09-18T00:00:00']

    g = geocoder.google(zip)
    locations = [g.latlng]

    food_search = {'locations': locations, 'pref': random.choice(list_o_foods)}
    event_search = {'pref' : random.choice(list_o_events), 'locations': locations, 'start' : default_time_range[0], 'end' : default_time_range[1]}

    food = get_results_yelp(food_search)
    event = get_results_event(event_search)

    print food
    print event

def get_results_event(lparams):
    apiData = []
    eparams = {}
    for latitude, longitude in lparams['locations']:
        eparams['lat'] = latitude
        eparams['lng'] = longitude
        eparams['start'] = lparams['start']
        eparams['end'] = lparams['end']
        eparams['pref'] = lparams['pref']

        payload = get_search_params_event(eparams)
        r = requests.get("https://www.eventbriteapi.com/v3/events/search/?q=",params=payload)
        answer = r.json()
        if len(answer['events']) > 0:
                return answer['events'][0]['name']
        time.sleep(1.0)
    return []

def get_search_params_event(lparams):
    with open("config_secret_ebrite.json") as json_file:
        json_data = json.load(json_file)
        anon_token = json_data["anon_token"]
    payload ={}
    payload["q"] = str(lparams['pref'])
    payload["location.latitude"] = str(lparams['lat'])
    payload["location.longitude"] = str(lparams['lng'])
    payload["start_date.range_start"] = str(lparams['start'])
    payload["start_date.range_end"] = str(lparams['end'])
    payload["token"] = str(anon_token)
    return payload
    
#yelp python api
def defineParams(latitude, longitude, pref):
    params = {}
    params["term"] = pref
    params["ll"] = "{},{}".format(str(latitude), str(longitude))
    #params["radius_filter"] = "2000"
    #params["sort"] = "2"
    params["limit"] = "1"
    return params

def getData(params):
    # setting up personal Yelp account
    with open("config_secret.json",'r') as json_file:
        json_data = json.load(json_file)
          
    session = rauth.OAuth1Session(
        consumer_key = json_data["consumer_key"],
        consumer_secret = json_data["consumer_secret"],
        access_token = json_data["token"],
        access_token_secret = json_data["token_secret"])

    request = session.get("http://api.yelp.com/v2/search", params=params)
    
    #transforming the data in JSON format
    data = request.json()
    session.close()
    return data

def get_results_yelp(lparams):
    for latitude, longitude in lparams['locations']:
        params = defineParams(latitude, longitude, lparams['pref'])
        result = getData(params)
        
        if len(result['businesses']) > 0:
                return result['businesses'][0]['name']
        time.sleep(1.0)
        
    return []

if __name__ == "__main__":
    grabdata('10012')

