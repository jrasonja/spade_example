import logging

from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message

import settings

log = logging.getLogger('spade_example')

class SendMessage(OneShotBehaviour):

    def __init__(self, jids, message):
        if jids == '__all__':
            #broadcast message go to server
            jids = [settings.SERVER_JID]
        elif isinstance(jids, str):
            jids = [jids]

        if not isinstance(jids, list):
            raise TypeError("Only jids or list of jids are allowed") 

        #Cleaning jids
        self.jids = [
            jid if '@' in jid else f'{jid}@{settings.XMPP_SERVER}'
            for jid in jids
        ]
        self.message = message

        super().__init__()

    async def run(self):
        log.debug(f'[{self.agent.name}] Sending message to: {self.jids}')
        for jid in self.jids:
            msg = Message(to=jid)
            #msg.set_metadata('action', 'send_message')
            msg.body = self.message
            await self.send(msg)

class ReceiveMessage(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)
        print("Trying..")
        if not msg:
            return
        print(f'@{msg.sender} -> {msg.body}')
             
