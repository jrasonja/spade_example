import time
import logging
import sys
import re

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from spade.template import Template

from behaviour import SendMessage, ReceiveMessage
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

    class Chat(CyclicBehaviour):
        async def run(self):
            pattern = re.compile('^@(?P<to>[\w\d\_@-]*) +(?P<msg>.+)$')
            message = input("@<to?> <message>:")

            matched = pattern.match(message)

            if not matched:
                return
            
            send_message = SendMessage(
                matched.group('to') or '__all__',
                matched.group('msg')
            )
            self.agent.add_behaviour(send_message)
            

    async def setup(self):
        log.info(f"[{self.name}] Avatar running")

        self.add_behaviour(self.PresenceSetup())
        message_template = Template()
        message_template.set_metadata('action','send_message')
        self.add_behaviour(ReceiveMessage(), message_template)
        self.add_behaviour(self.Chat())

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

