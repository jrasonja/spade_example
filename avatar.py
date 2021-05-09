import time
import logging
import sys

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

import settings

log = logging.getLogger('spade_example')

class Avatar(Agent):

    class PresenceSetup(OneShotBehaviour):

        def on_available(self, jid, stanza):
            log.info(f"[{self.agent.name}] Agent {jid.split('@')[0]} is available.")

        def on_subscribed(self, jid):
            log.debug(f"[{self.agent.name}] Agent {jid.split('@')[0]} has accepted the subscription.")
            log.debug(f"[{self.agent.name}] Contacts: {self.agent.get_contacts_simple()}")

        def on_subscribe(self, jid):
            log.debug(f"[{self.agent.name}] Agent {jid.split('@')[0]} asked for subscription. Let's aprove it.")
            self.presence.approve(jid)
            log.debug(f"[{self.agent.name}] Contacts: {self.agent.get_contacts_simple()}")

        def on_unsubscribe(self, jid):
            log.debug(f"[{self.agent.name}] Agent {jid.split('@')[0]} asked for unsubscription. Let's aprove it.")
            log.debug(f"[{self.agent.name}] Contacts: {self.agent.get_contacts_simple()}")

        def on_unsubscribed(self, jid):
            log.debug(f"[{self.agent.name}] Agent {jid.split('@')[0]} has unsubscribe.")
            log.debug(f"[{self.agent.name}] Contacts: {self.agent.get_contacts_simple()}")

        async def run(self):
            self.presence.on_subscribe = self.on_subscribe
            self.presence.on_subscribed = self.on_subscribed
            self.presence.on_unsubscribe = self.on_unsubscribe
            self.presence.on_unsubscribed = self.on_unsubscribed
            self.presence.on_available = self.on_available

            self.presence.set_available()
            log.debug(f"[{self.agent.name}] Contacts: {self.agent.get_contacts_simple()}")

            self.presence.subscribe(settings.SERVER_JID)



    async def setup(self):
        log.info(f"[{self.name}] Avatar running")

        self.add_behaviour(self.PresenceSetup())

    def get_contacts_simple(self):
        return [
            str(jid)
            for jid in self.presence.get_contacts().keys() 
        ]

    def stop(self):
        log.debug(f'[{self.name}] Stopping...')

        log.debug(f'[{self.name}] Unsubscribe {settings.SERVER_JID}')
        self.presence.unsubscribe(settings.SERVER_JID)
        
        super().stop()

