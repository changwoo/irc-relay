#!/usr/bin/python
# -*- encoding: utf-8 -*-

from relay import ChannelRelay

data = {
    'ozinger': {
        'host': 'irc.ozinger.org',
        'port': 6666,
        'username': u'GNOMERELAY',
        'nick': u'♠릴레이',
        'channel': '#gnome',
        'prefix': u'>',
        'charset': 'UTF-8',
        'max-msg-bytes': 400,
        },
    'hanirc': {
        'host': 'irc.hanirc.org',
        'port': 6666,
        'username': u'GNOMERELAY',
        'nick': u'♠릴레이',
        'channel': '#gnome',
        'charset': 'CP949',
        'max-msg-bytes': 400,
        },
    }

relay = ChannelRelay(data)
relay.main()
