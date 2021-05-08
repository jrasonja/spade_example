import sys
import time
import logging

import settings
from avatar import Avatar
from server import Server


log = logging.getLogger('spade_primjer')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler(sys.stdout))



if __name__ == '__main__':
    server = Server(
        settings.SERVER_JID,
        settings.SERVER_PASS
    )
    server.start()


    avatar = Avatar(
        settings.AGENT_JID,
        settings.AGENT_PASS
    )
    avatar.start()


    avatar2 = Avatar(
        settings.AGENT2_JID,
        settings.AGENT2_PASS
    )
    avatar2.start()


    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    server.stop()
    avatar.stop()
    avatar2.stop()
