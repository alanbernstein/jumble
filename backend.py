#!/usr/bin/python
"""backend for jumble app, handle retrieving and caching to file
the source used by http://www.chicagotribune.com/chi-jumbleclassic-htmlpage-htmlstory.html
"""
import json
import cgitb

from client import WebClient

cgitb.enable(format='text')
print("Content-Type: text/plain;charset=utf-8")
print("")


# only need one method - get latest
# - run on a daily cron, and cache the result
# - retrieve from cache
# - JumbleClient, unchanged, handles both

def main():
    # env = os.environ
    # url = env['REQUEST_URI']
    # params = urlparse.parse_qs(urlparse.urlparse(url).query)

    # TODO: allow requesting old data, either with date string or day-delta
    #       jumble.py?date=161127
    #       jumble.py?prev=1

    jc = WebClient()
    jumble = jc.get_jumble()
    print(json.dumps(jumble))


if __name__ == '__main__':
    main()
