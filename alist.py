#!/bin/python
import show
import re
from rapidfuzz import fuzz

list_file="anime.list"

# Determines aniDB ID using regex
def get_id(line):
    # Regex to determine AniDB ID
    id = (re.search(r"\d*]$",line).group())[:-1]

    return id

# Generates a list of shows
def gen_list():
    content=open(list_file)
    shows=[]

    # Create list containing show info gathered using show.py
    for line in content:
        id = get_id(line)
        show_info = show.get_info(id)
        shows.append(show_info)

    return shows

# Fuzzy searches the anime list to provide a search feature
def filter(search, name):
    ratio = fuzz.partial_ratio(search.lower(), name.lower())
    # May need to be adjusted, but seems to work well
    if (ratio > 85):
        return 1
    else:
        return 0

# Updates list when searching
def new_list(search, shows):
    if (len(search) == 0):
        return shows
    output_list = []

    for listing in shows:
        # Calls filter to fuzzy search
        if (filter(search, listing.get("Title"))):
            output_list.append(listing)

    return output_list
