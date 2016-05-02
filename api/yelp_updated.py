import time
import rauth

import pandas
import simplejson as json


def defineParams(latitude, longitude):
    params = {}
    params["term"] = "burger"
    params["ll"] = "{},{}".format(str(latitude), str(longitude))
    params["radius_filter"] = "2000"
    params["sort"] = "2"
    params["limit"] = "1"
 
    return params

def getData(params):

    # setting up personal Yelp account
    with open("config_secret.json",'r') as json_file:
        json_data = json.load(json_file)
    session = rauth.OAuth1Session(
        consumer_key = json_data["consumer_key"]
        ,consumer_secret = json_data["consumer_secret"]
        ,access_token = json_data["token"]
        ,access_token_secret = json_data["token_secret"])
     
    request = session.get("http://api.yelp.com/v2/search", params=params)
   
    # transforming the data in JSON format
    data = request.json()
    session.close()

    return data

def main():

    locations = [(39.98,-82.98)]
    
    apiData = []
    for latitude, longitude in locations:
        params = defineParams(latitude, longitude)
        apiData.append(getData(params))
        time.sleep(1.0)

    print(json.dumps(apiData[0]["businesses"][0]["name"], sort_keys=True, indent=4 * ' '))

if __name__ == '__main__':
    main()
