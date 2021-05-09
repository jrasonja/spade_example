import sys
import time
import logging

import settings
from avatar import Avatar
from server import Server


log = logging.getLogger('spade_example')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)



if __name__ == '__main__':

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

    avatar2.stop()
