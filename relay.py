# irc relay
# Copyright (C) 2011 Changwoo Ryu
#
# This program is free software; you can redistribute it and'or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from irclib import IRC

class ChannelRelay:
    def __init__(self, infos):
        self.conns = []
        self.data = infos
        for name in infos.keys():
            host = infos[name]['host']
            port = infos[name]['port']
            nick = infos[name]['nick']
            try:
                password = infos[name]['password']
            except KeyError:
                password = ''
            try:
                username = infos[name]['username']
            except KeyError:
                username = nick
            try:
                realname = infos[name]['realname']
            except KeyError:
                realname = nick

            charset = infos[name]['charset']

            ircobj = IRC()
            self.data[name]['ircobj'] = ircobj
            conn = ircobj.server().connect(host, port, nick.encode(charset),
                                           password, username.encode(charset),
                                           realname.encode(charset))
            self.data[name]['conn'] = conn
            conn.server_name = name

            conn.add_global_handler('welcome', self.on_welcome)
            conn.add_global_handler('pubmsg', self.on_msg)
            conn.add_global_handler('action', self.on_msg)
            self.conns.append(conn)

    def main(self):
        while True:
            for name in self.data.keys():
                self.data[name]['ircobj'].process_once(0.5)

    # irclib callbacks
    def on_welcome(self, conn, event):
        name = conn.server_name
        channel = self.data[name]['channel']
        charset = self.data[name]['charset']
        print 'source: %s' % event.source()
        print 'target: %s' % event.target()
        print 'msg: %s' % event.arguments()[0]
        conn.join(channel)

    def on_msg(self, conn, event):
        name = conn.server_name
        channel = self.data[name]['channel']
        if event.target() != channel:
            return
        charset = self.data[name]['charset']

        try:
            uninick = event.source().split('!')[0].decode(charset)
            msg = event.arguments()[0]
            unimsg = msg.decode(charset)
            try:
                prefix = self.data[name]['prefix']
                if not unimsg.startswith(prefix):
                    return
                unimsg = unimsg[len(prefix):].lstrip()
            except KeyError:
                # no prefix - relay it
                pass
        except UnicodeDecodeError:
            return

        # avoid possible duplicated relay
        try:
            if unimsg[0] == u'<':
                return
        except IndexError:
            pass

        print 'pubmsg: %s' % unimsg

        for n in self.data.keys():
            if n == name:
                continue

            target_channel = self.data[n]['channel']
            target_charset = self.data[n]['charset']
            
            try:
                try:
                    if self.data[n]['mangle-nicks']:
                        pnick = (uninick[0] + '_' + uninick[1:])
                    else:
                        pnick = uninick
                except KeyError:
                    pnick = uninick
                pnick = uninick.encode(target_charset, 'replace')
                target_msg = '<%s> ' % (pnick,)
                target_msg += unimsg.encode(target_charset, 'replace')
            except UnicodeEncodeError:
                continue

            # truncate the string under the IRC line length limit
            try:
                max_msg_bytes = self.data[n]['max-msg-bytes']
                target_msg = target_msg[:max_msg_bytes]
                tempunimsg = target_msg.decode(target_charset, 'ignore')
                target_msg = tempunimsg.encode(target_charset)
            except KeyError:
                pass

            if event.eventtype() == 'pubmsg':
                self.data[n]['conn'].privmsg(target_channel, target_msg)
            elif event.eventtype() == 'action':
                self.data[n]['conn'].action(target_channel, target_msg)
