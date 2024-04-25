#!/bin/python
import show
import re

list_file="anime.list"

def get_id(line):
    # Regex to determine AniDB ID
    id = (re.search(r"\d*]$",line).group())[:-1]

    return id

def gen_list(filename):
    content=open(filename)
    shows=[]

    for line in content:
        shows.append(show.get_info(get_id(line)))

    return shows
