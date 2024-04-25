#!/bin/python
# Module for making requests to Shoko about the series in question

import requests
import json

shokoUrl = "http://shoko:8111"
keyLocation = "api.key"

# Read key from keyfile
def get_key():
    with open(keyLocation, 'r') as keyFile:
        apiKey = keyFile.read().replace('\n','')
    return apiKey

def get_episode(id):
    reqUrl = shokoUrl + "/api/v3/Episode/AniDB/" + str(id) + \
        "/Episode?includeFiles=true&includeMediaInfo=false&includeAbsolutePaths=false&includeDataFrom=Shoko"
    resJson = get_req(reqUrl)

    episode_data = {
        "AniDB"    : resJson["IDs"]["AniDB"],
        "ShokoID"  : resJson["IDs"]["ID"],
        "EpName"   : resJson["Name"],
        "Duration" : resJson["Duration"],
        "Watched"  : resJson["Watched"],
        "RelPath"  : resJson["Files"][0]["Locations"][0]["RelativePath"]
    }

    return episode_data

# Send HTTP Get request to Shoko
def get_req(reqUrl):
    reqHeaders = {'accept': 'text/plain', 'apikey': get_key()}
    res = requests.get(reqUrl,headers=reqHeaders)

    # Check if series even exists
    if (res.status_code != 200):
        print("Either the client cannot connect to Shoko, or the series does not exist")
        quit()
    else:
        resJson = json.loads(res.text)
    return resJson

# Get generic information about the series
def get_info(id):
    reqUrl = shokoUrl + "/api/v3/Series/AniDB/" + str(id)
    resJson = get_req(reqUrl)

    series_data = {
        "ID"      : str(resJson['ID']),
        "Title"   : resJson['Title'],
        "EpCount" : str(resJson['EpisodeCount']),
        "AirDate" : resJson['AirDate']
    }
    return series_data

# Get information on episodes of a series
def get_episodes(id):
    reqUrl = shokoUrl + "/api/v3/Series/AniDB/" + str(id) + \
        "/Episode?pageSize=0&page=1&includeMissing=false&includeHidden=false&includeWatched=true&fuzzy=true"
    resJson = get_req(reqUrl)
    episode_list = []

    # Loop through each episode and get required data
    for episode in resJson["List"]:
        cur_episode = {
            "EpNumber" : str(episode["EpisodeNumber"]),
            "Title"    : episode["Title"],
            "AirDate"  : episode["AirDate"],
            "EpType"   : episode["Type"],
            "EpID"     : str(episode["ID"])
        }
        episode_list.append(cur_episode)
    return episode_list
