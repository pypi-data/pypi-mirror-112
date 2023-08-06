import os
import logging
import logging.config
currentdir = os.path.dirname(os.path.realpath(__file__))

class Logs(object):
    def __init__(self):
        super(Logs, self).__init__()
        self.conffile=currentdir + '/logging.py'
        self._getConfigFile()
        logging.config.fileConfig(self.conffile)
        self.logger = logging.getLogger('habcatLogger')

    def _getConfigFile(self):
        try:
            # Configuración de loggging externa
            osenv = os.environ['HABCATEV_LOGCONFIG']
            if osenv and os.path.isfile(osenv):
                self.conffile = osenv
            print(osenv)
        except Exception as e:
            pass
    