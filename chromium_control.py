import requests
import numpy as np

class chrome:
    """
    Control chrome session through its remote interface.  Start chromium by
    e.g. chromium --remote-debugging-port=9222 to enable remote control.
    """

    def __init__(self, host, port):
        self.api_url = 'http://' + host + ':' + port + '/json'

    def new_tab(self, url):
        """
        Open new tab.
        """
        requests.post(self.api_url + '/new?' + url)

    def close_tab(self, tabid):
        """
        Close tab.
        """
        requests.post(self.api_url + '/close/' + tabid)

    def get_tabs(self):
        """
        Get list over tabs.

        Order is well-defined, first position corresponds to currently selected
        tab, while last position corresponds to the tab underneath all the
        other tabs after user selection.
        """
        tabs = requests.get(self.api_url).json()
        filtered_tabs = []

        #filter out child targets
        for tab in tabs:
            if 'parentId' not in list(tab) and tab['type'] == 'page':
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
    parser = argparse.ArgumentParser(description='Control chromium session started with --remote-debugging-port=PORT.\nExample: python3 chromium_control.py next_tab.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('command', choices=['cycle_forever', 'next_tab', 'new_tab', 'close_current'],
                        help="cycle_forever: Cycle through tabs. Set --cycle-time to change how long each tab\nshould be viewed.\n\nnext_tab: Select next tab.\n\nnew_tab: Open new tab. URL is set using --url.\n\nclose_current: Close currently activated tab.")
    parser.add_argument('--cycle-time', default=1.0, help='Cycle time, for cycle_forever option.', type=float)
    parser.add_argument('--url', help='URL to open for command new_tab', default='http://google.com')
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default='9222', help='Chrome debugging port')
    args = parser.parse_args()

    #interface against chrome
    ctrl = chrome(host=args.host, port=args.port)

    if args.command == 'cycle_forever':
        #cycle through all tabs forever
        while True:
            ctrl.next_tab()
            time.sleep(args.cycle_time)
    elif args.command == 'next_tab':
        #select next tab
        ctrl.next_tab()
    elif args.command == 'new_tab':
        #open new tab
        ctrl.new_tab(args.url)
    elif args.command == 'close_current':
        #close currently open tab
        ctrl.close_tab(ctrl.current_tab())
