import paho.mqtt.client as mqtt
from . import MQTTClient
import argparse
import yaml

class Device(MQTTClient.MQTTClient):
    """docstring for Device."""
    def __init__(self,description='',mqttbroker="localhost:1883"):
        super(Device, self).__init__()
        self._subscriptionarr = ['#']
        self.deviceDescription = description
        self._argumentsParse()

    def init(self):
        pass 

    def _argumentsParse(self):
        # Device CLI
        self.parser = argparse.ArgumentParser(description=self.deviceDescription)
        self.parser.add_argument('--config', help='Fichero YAML de configuración del componente')
        self.parser.add_argument('--run', action='store_true', help='Ejecuta el componente')
        self.args = self.parser.parse_args()
        self.log.logger.debug('Input params:')
        self.log.logger.debug(self.args)

        if self.args.config:
            self.log.logger.debug('Cargando fichero de configuracion ...')
            with open(self.args.config) as file:
                self.config = yaml.load(file, Loader=yaml.FullLoader)
        else:
            self.log.logger.debug('No hay fichero de configuracion')
    
        if self.args.run:
            self.init()
            self.log.logger.debug('Se ejecuta el componente ...')
            self.run()

    def setSubscriptionArr(self,subarr):
        self.log.logger.debug('Seteando array de subscripciones ...')
        self.log.logger.debug(subarr)
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

