from time import gmtime, strftime
import random
list_o_events = ["Movies", "Theater", "Concerts", "Festivals", "Sports"]
list_o_foods = ["American", "Indian", "Mexican", "Chinese", "Thai"]
default_location = ['40.788022', '-74.399797']
default_time_range = ['2016-05-17T00:00:00', '2016-05-18T00:00:00']

food_search = [random.choice(list_o_foods), default_location[0], default_location[1], '1']
event_search = [random.choice(list_o_events), default_location[0], default_location[1], default_time_range[0], default_time_range[1]]

food = get_results_yelp(food_search)
event = get_results_event(event_search)
#yelp params is a list of type ['term','latitude','longitude', 'limit']
#example usage: x = ['beer','40.788022', '-74.399797', '1']
#get_results_yelp(x)

#eventbrite api
#by col-n

#takes a list of the form ['keyword', 'latitude', 'longitude', 'YYYY-MM-DDTHH:MM:SS'(start_range), 'YYYY-MM-DDTHH:MM:SS'(end_range)]
#example: x = ['beer','40.788022', '-74.399797', '2016-04-17T00:00:00', '2016-04-18T00:00:00']
#get_results_event(x)

def get_results_event(lparams):
    import requests
    import json
    payload = get_search_params_event(lparams)
    
    r = requests.get("https://www.eventbriteapi.com/v3/events/search/?q=",params=payload)
    answer = r.json()
    
    return answer

def get_search_params_event(lparams):
    import json
    with open("/Users/colin/Desktop/config_secret_ebrite.json") as json_file:
        json_data = json.load(json_file)
        anon_token = json_data["anon_token"]
    payload ={}
    payload["q"] = str(lparams[0])
    payload["location.latitude"] = str(lparams[1])
    payload["location.longitude"] = str(lparams[2])
    payload["start_date.range_start"] = str(lparams[3])
    payload["start_date.range_end"] = str(lparams[4])
    payload["token"] = str(anon_token)
    return payload
    
#yelp python api
#by col-n, h/t to phil johnson

#lparams is a list of type ['term','latitude','longitude', 'limit']
def get_results_yelp(lparams):
    import rauth
    import csv
    with open("/Users/colin/Desktop/config_secret.json") as json_file:
        json_data = json.load(json_file)
    session = rauth.OAuth1Session(
		consumer_key = json_data["consumer_key"]
		,consumer_secret = json_data["consumer_secret"]
		,access_token = json_data["token"]
		,access_token_secret = json_data["token_secret"])
    
    params = get_search_params_yelp(lparams)

    request = session.get("http://api.yelp.com/v2/search",params=params)
    data = request.json()
    session.close()
    return data
    
def get_search_params_yelp(lparams):
    params ={}
    params["term"] = str(lparams[0])
    params["ll"] = "{},{}".format(str(lparams[1]),str(lparams[2]))
    params["limit"] = str(lparams[3])
    
    return params
    
#example usage: x = ['beer','40.788022', '-74.399797', '1']
#get_results_yelp(x)