import requests

API_URL = "http://localhost:9222/json"

def tab_id_by_name(name):
    req = requests.get(API_URL).json()
    print(req)

def new_tab(url):
    requests.post(API_URL + '/new?' + url)

def set_tab(tabid):
    requests.get(API_URL + '/activate/' + tabid)

import numpy as np

current_id = None

def next_tab():
    global current_id

    #list over tabs
    tabs = requests.get(API_URL).json()

    #list over tab ids
    ids = np.array([tab['id'] for tab in tabs])

    if current_id is None:
        current_id = ids[0]

    #sort tab ids in order to get a well-defined ordering of the tabs
    sorted_ids = np.sort(ids)

    #current position along sorted tab id list
    try:
        ind = np.where(sorted_ids == current_id)[0][0]

        #next index
        next_index = (ind + 1) % len(sorted_ids)

        #next tab id
        next_id = sorted_ids[(ind + 1) % len(sorted_ids)]
        next_ind = np.where(ids == next_id)[0][0]

        #set current tab
        current_id = tabs[next_ind]['id']
        set_tab(current_id)
    except:
        current_id = None
    return current_id
