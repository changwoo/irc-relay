#!/usr/bin/python
# -*- encoding: utf-8 -*-

from relay import ChannelRelay

data = {
    'ozinger': {
        'host': 'irc.ozinger.org',
        'port': 6666,
        'username': u'GNOMERELAY',
        'nick': u'♠한씨네',
        'channel': '#gnome',
        'charset': 'UTF-8',
        'max-msg-bytes': 400,
        #'prefix': u'>',
        #'mangle-nicks': True,
        },
    'hanirc': {
        'host': 'irc.hanirc.org',
        'port': 6666,
        'username': u'GNOMERELAY',
        'nick': u'♣오씨네',
        'channel': '#gnome',
        'charset': 'CP949',
        'max-msg-bytes': 400,
        #'mangle-nicks': True,
        },
    }

relay = ChannelRelay(data)
relay.main()
