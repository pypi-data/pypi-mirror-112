import paho.mqtt.client as mqtt
from . import MQTTClient

class Device(MQTTClient.MQTTClient):
    """docstring for Device."""
    def __init__(self,mqttbroker="localhost:1883"):
        super(Device, self).__init__()
        self._subscriptionarr = ['#']

    def setSubscriptionArr(self,subarr):
        self._subscriptionarr = subarr
    
    def run(self):
        # Iniciamos el mqtt
        self.connect()
        self.subscribeto(self._subscriptionarr)
        self._startListeners()
        # Loop principal del dispositivo
        while True:
            self.loop()

    def on_event(self,topic,data):
        pass 

    def on_message(self,client, userdata, msg):
        self.on_event(msg.topic,msg.payload.decode())
        
    def loop(self):
        pass

