#!/bin/python
import show
import re
from rapidfuzz import fuzz

list_file="anime.list"

def get_id(line):
    # Regex to determine AniDB ID
    id = (re.search(r"\d*]$",line).group())[:-1]

    return id

def gen_list():
    content=open(list_file)
    shows=[]

    for line in content:
        id = get_id(line)
        show_info = show.get_info(id)
        shows.append(show_info)

    return shows

def filter(search, name):
    ratio = fuzz.partial_ratio(search, name)
    if (ratio > 85):
        return 1
    else:
        return 0

def new_list(search, shows):
    newList = []

    for listing in shows:
        if (filter(search, listing.get("Title"))):
            newList.append(listing)

    return newList
