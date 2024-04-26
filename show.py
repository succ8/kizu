#!/bin/python
# Module for making requests to Shoko about the series in question

import requests
import json

shoko_url = "http://shoko:8111"
key_location = "api.key"

# Read key from keyfile
def get_key():
    with open(key_location, 'r') as key_file:
        api_key = key_file.read().replace('\n','')
    return api_key

def get_episode(id):
    req_url = shoko_url + "/api/v3/Episode/AniDB/" + str(id) + \
        "/Episode?includeFiles=true&includeMediaInfo=false&includeAbsolutePaths=false&includeDataFrom=Shoko"
    res_json = get_req(req_url)

    episode_data = {
        "AniDB"    : res_json["IDs"]["AniDB"],
        "ShokoID"  : res_json["IDs"]["ID"],
        "EpName"   : res_json["Name"],
        "Duration" : res_json["Duration"],
        "Watched"  : res_json["Watched"],
        "RelPath"  : res_json["Files"][0]["Locations"][0]["RelativePath"]
    }

    return episode_data

# Send HTTP Get request to Shoko
def get_req(req_url):
    req_headers = {'accept': 'text/plain', 'apikey': get_key()}
    res = requests.get(req_url,headers=req_headers)

    # Check if series even exists
    if (res.status_code != 200):
        print("Either the client cannot connect to Shoko, or the series does not exist")
        quit()
    else:
        res_json = json.loads(res.text)
    return res_json

# Get generic information about the series
def get_info(id):
    req_url = shoko_url + "/api/v3/Series/AniDB/" + str(id)
    res_json = get_req(req_url)

    series_data = {
        "ID"      : str(res_json['ID']),
        "Title"   : res_json['Title'],
        "EpCount" : str(res_json['EpisodeCount']),
        "AirDate" : res_json['AirDate']
    }
    return series_data

# Get information on episodes of a series
def get_episodes(id):
    req_url = shoko_url + "/api/v3/Series/AniDB/" + str(id) + \
        "/Episode?pageSize=0&page=1&includeMissing=false&includeHidden=false&includeWatched=true&fuzzy=true"
    res_json = get_req(req_url)
    episode_list = []

    # Loop through each episode and get required data
    for episode in res_json["List"]:
        cur_episode = {
            "EpNumber" : str(episode["EpisodeNumber"]),
            "Title"    : episode["Title"],
            "AirDate"  : episode["AirDate"],
            "EpType"   : episode["Type"],
            "EpID"     : str(episode["ID"])
        }
        episode_list.append(cur_episode)
    return episode_list
