#!/usr/bin/python
# -*- encoding: utf-8 -*-

from relay import ChannelRelay

name_version = u'그놈 릴레이 20110228'

data = {
    'ozinger': {
        'host': 'irc.ozinger.org',
        'port': 6666,
        'username': u'GNOMERELAY',
        'nick': u'♠한씨네',
        'realname': name_version,
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
        'realname': name_version,
        'channel': '#gnome',
        'charset': 'CP949',
        'max-msg-bytes': 400,
        #'mangle-nicks': True,
        'reconnect-delay': 3,
        },
    }

relay = ChannelRelay(data)
relay.main()
