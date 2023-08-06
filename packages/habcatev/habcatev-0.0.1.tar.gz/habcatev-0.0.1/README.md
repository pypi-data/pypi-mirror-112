# habcatev

Libreria python orientada a eventos para habcat.


## Quick run

```python
import habcatev,time
import random 

class SimpleExample(habcatev.device.Device.Device):
    """Ejemplo simple en el que se produce y consume"""
    def __init__(self):
        super(SimpleExample, self).__init__()
        # El dispositivo se subscribe a todos los topics
        self.setSubscriptionArr(['#'])

    def on_event(self,topic,data):
        # Lanzamos este codigo cuando se produce un evento
        self.log.logger.info("Ha llegado: Topic:" + topic + "  Data: " + data)

    def loop(self):
        # Suponemos que leemos el valor de un sensor y lo escribimos 
        # en un topic
        self.log.logger.info('Enviando un mensaje a mqtt ...')
        self.send('mitopico1', random.uniform(10.5, 75.5))
        time.sleep(5)

SimpleExample().run()
```