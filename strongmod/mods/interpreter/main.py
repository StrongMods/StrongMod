import code
import threading
import api
from internal import game_controller

threading.Thread(target=code.interact, kwargs={"local": locals()}).start()
