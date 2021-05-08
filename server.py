import time
import logging
import sys

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

import settings

log = logging.getLogger('spade_primjer')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler(sys.stdout))


class Server(Agent):

    class Presence(OneShotBehaviour):

        def on_available(self, jid, stanza):
            print("[{}] Agent {} is available.".format(self.agent.name, jid.split("@")[0]))

        def on_subscribed(self, jid):
            print("[{}] Agent {} has accepted the subscription.".format(self.agent.name, jid.split("@")[0]))
            print("[{}] Contacts List: {}".format(self.agent.name, self.agent.presence.get_contacts()))

        def on_subscribe(self, jid):
            print("[{}] Agent {} asked for subscription. Let's aprove it.".format(self.agent.name, jid.split("@")[0]))
            self.presence.approve(jid)
            print("[{}] Contacts List: {}".format(self.agent.name, self.agent.presence.get_contacts()))
            self.presence.subscribe(jid)

        def on_unsubscribe(self, jid):
            print("[{}] Agent {} asked for unsubscription. Let's aprove it.".format(self.agent.name, jid.split("@")[0]))
            self.presence.approve(jid)
            print("[{}] Contacts List: {}".format(self.agent.name, self.agent.presence.get_contacts()))
            self.presence.unsubscribe(jid)

        def on_unsubscribed(self, jid):
            print("[{}] Agent {} has unsubscribe.".format(self.agent.name, jid.split("@")[0]))
            print("[{}] Contacts List: {}".format(self.agent.name, self.agent.presence.get_contacts()))

        async def run(self):
            self.presence.on_subscribe = self.on_subscribe
            self.presence.on_subscribed = self.on_subscribed
            self.presence.on_available = self.on_available

            self.presence.set_available()
            print("[{}] Contacts List: {}".format(self.agent.name, self.agent.presence.get_contacts()))
            #self.presence.unsubscribe(settings.AGENT_JID)
            #self.presence.unsubscribe(settings.AGENT2_JID)

    async def setup(self):
        log.info(f'Server {self.name} running')

        self.add_behaviour(self.Presence())
