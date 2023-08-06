import paho.mqtt.client as mqtt
import threading,time
import sys,os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import common
import traceback

class MQTTClient(object):
    """Handles the mqtt connections"""
    def __init__(self, brokermqtt="localhost:1883"):
        super(MQTTClient, self).__init__()
        #Connection
        trimed = brokermqtt.split(':')
        self.mqttserver = trimed[0]
        self.mqttport   = int(trimed[1])
        self.deviceid = "habcatdevice-" + str(int(time.time()))
        self.mqClient = mqtt.Client(self.deviceid)
        self.log = common.logs.Logs()
    
    def connect(self):
        self.log.logger.debug('Tratando de conectar con MQTT ' + self.mqttserver + ':' + str(self.mqttport))
        try:
            self.mqClient.connect(self.mqttserver, self.mqttport)
        except Exception as e:
            traceback.print_exc()
            self.log.logger.error(e)
            self.log.logger.error('Ha sido imposible conectar con el servidor MQTT con la siguiente configuración ' + self.mqttserver + ':' + str(self.mqttport))
            self.log.logger.error('Verifique que el servidor está levantado')
            sys.exit(1)

    def _receiveDataFromMQTT(self):
        self.mqClient.loop_forever()
    
    def _startListeners(self):
        recdata = threading.Thread(
            target=self._receiveDataFromMQTT
        )
        recdata.start()
    
    def subscribeto(self,subscriptionsarr):
        self.mqClient.on_message = self.on_message
        for topic in subscriptionsarr:
            self.log.logger.debug('Subscribiendo a ' + topic)
            self.mqClient.subscribe(topic)


    def send(self,topic,message):
        """ Envia un mensaje a un determinado topic """
        self.mqClient.publish(topic,message)
    
    def on_message(self,client, userdata, msg):
        pass
