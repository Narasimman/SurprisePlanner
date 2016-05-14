#eventbrite api
#by col-n

#takes a list of the form ['keyword', 'latitude', 'longitude', 'YYYY-MM-DDTHH:MM:SS'(start_range), 'YYYY-MM-DDTHH:MM:SS'(end_range)]
#example: x = ['beer','40.788022', '-74.399797', '2016-04-17T00:00:00', '2016-04-18T00:00:00']
#get_results(x)

def get_results(lparams):
    import requests
    import json
    payload = get_search_params(lparams)
    
    r = requests.get("https://www.eventbriteapi.com/v3/events/search/?q=",params=payload)
    answer = r.json()
    
    return answer

def get_search_params(lparams):
    import json
    with open("config_secret_ebrite.json") as json_file:
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

