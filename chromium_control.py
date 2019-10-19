import requests
import numpy as np

API_URL = "http://localhost:9222/json"

class chrome:
    """
    Control chrome session through its remote interface.  Start chromium by
    e.g. chromium --remote-debugging-port=9222 to enable remote control.
    """

    def __init__(self, api_url=API_URL):
        self.api_url = api_url

    def new_tab(self, url):
        """
        Open new tab.
        """
        requests.post(self.api_url + '/new?' + url)

    def get_tabs(self):
        """
        Get list over tabs.
        """
        tabs = requests.get(API_URL).json()
        filtered_tabs = []

        #filter out child targets
        for tab in tabs:
            if 'parentId' not in list(tab):
                filtered_tabs.append(tab)
        return filtered_tabs

    def current_tab(self):
        """
        Get ID of current tab.
        """
        tabs = self.get_tabs()
        return tabs[0]['id']

    def activate_tab(self, tabid):
        """
        Activate tab with given tabid.
        """
        requests.get(self.api_url + '/activate/' + tabid)

    def next_tab(self):
        """
        Cycle through tabs, in user-defined order.
        """
        tabs = self.get_tabs()

        #if the user has cycled through e.g. four tabs in the order: 1, 2, 3,
        #4, then the currently shown tab (4) will be at position 0 in the tab
        #array, while the first shown tab underneath the rest (1) will be at
        #end of the array.  Always selecting the last tab should then cycle
        #through the tabs in a well-defined order.
        self.activate_tab(tabs[-1]['id'])

import argparse
import time
if __name__ == "__main__":

    #arguments
    parser = argparse.ArgumentParser(description='Control chromium session started with --remote-debugging-port=9222.')
    parser.add_argument('command', choices=['cycle_forever', 'next_tab'])
    parser.add_argument('--cycle-time', default=1.0, help='Cycle time.', type=float)
    args = parser.parse_args()

    #interface against chrome
    ctrl = chrome()

    if args.command == 'cycle_forever':
        #cycle through all tabs forever
        while True:
            ctrl.next_tab()
            time.sleep(args.cycle_time)
    elif args.command == 'next_tab':
        #select next tab
        ctrl.next_tab()
