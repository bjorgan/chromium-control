import requests
import numpy as np

API_URL = "http://localhost:9222/json"

class chrome:
    """
    Control chrome session.
    """
    def __init__(self, api_url=API_URL):
        self.api_url = api_url
        self.current_id = None

    def new_tab(self, url):
        """
        Create new tab.
        """
        requests.post(self.api_url + '/new?' + url)

    def activate_tab(self, tabid):
        """
        Activate tab with given tabid.
        """
        requests.get(self.api_url + '/activate/' + tabid)

    def next_tab(self):
        """
        Cycle through tabs. Did not find a way to get the currently activated
        tab id, so cycles through the sorted list of tab ids and contains the
        currently set tab id as the attribute current_tabid of this class.
        """
        #list over tabs
        tabs = requests.get(API_URL).json()

        #list over tab ids
        ids = np.array([tab['id'] for tab in tabs])

        if self.current_id is None:
            self.current_id = ids[0]

        #sort tab ids in order to get a well-defined ordering of the tabs
        sorted_ids = np.sort(ids)

        try:
            #current position along sorted tab id list
            ind = np.where(sorted_ids == self.current_id)[0][0]

            #next index
            next_index = (ind + 1) % len(sorted_ids)

            #next tab id
            next_id = sorted_ids[(ind + 1) % len(sorted_ids)]
            next_ind = np.where(ids == next_id)[0][0]

            #set current tab
            self.current_id = tabs[next_ind]['id']
            self.activate_tab(self.current_id)
        except:
            #have probably ended up here because some tab
            #has been removed
            self.current_id = None

import argparse
import time
if __name__ == "__main__":

    #arguments
    parser = argparse.ArgumentParser(description='Control chromium session started with --remote-debugging-port=9222.')
    parser.add_argument('command', choices=['cycle_forever'],
                        help='Cycle tabs forever.')
    parser.add_argument('--cycle-time', default=1, help='Cycle time.')
    args = parser.parse_args()

    ctrl = chrome()

    if args.command == 'cycle_forever':
        while True:
            ctrl.next_tab()
            time.sleep(args.cycle_time)
