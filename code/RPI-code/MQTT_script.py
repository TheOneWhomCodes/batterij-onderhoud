import warnings

warnings.filterwarnings("ignore",category=DeprecationWarning)
#We gebruiken een oude versie van de mqtt die deprecated is, en als we ze niet negeren breekt onze
#scriptje terwijl we eigenlijk kunnen werken ermee zonder probleem

import paho.mqtt.client as mqtt
import json


#client = mqtt.Client() -> maakt onze client aan van dit scriptje
#client.connect("test.mosquitto.org", DEFAULT_PORT, ALIVE_TIME) -> "test.mosquitto.org" is een gratis publieke mqtt broker
#client.loop_start() -> zorgt ervoor dat het over mqtt kan praten en luisteren


DEFAULT_PORT = 1883 #-> de standaard poort voor unecrypted messages voor onze mqtt broker
ALIVE_TIME = 60 #-> Als de broker niks hoort na 60 seconden dan gaat hij niet meer luisteren
BROKER = "test.mosquitto.org" #-> onze broker die we gebruiken voor de mqtt
TOPIC = "RPITSM2/april_detection" #-> de topic waar we op subscriben

class MQTT:

    def __init__(self,topic=TOPIC,default_port=DEFAULT_PORT,alive_time=ALIVE_TIME,broker=BROKER):
        self.DEFAULT_PORT = default_port
        self.ALIVE_TIME = alive_time
        self.TOPIC = topic
        self.BROKER = broker
        self.client = mqtt.Client()

    
    def connect_client(self):
        BROKER = self.BROKER
        DEFAULT_PORT = self.DEFAULT_PORT
        ALIVE_TIME = self.ALIVE_TIME
        
        #we blijven proberen om te connecteren tot dat het ons lukt
        while True:
            try:
                self.client.connect(BROKER,DEFAULT_PORT,ALIVE_TIME)
                self.client.loop_start()
                break # we breaken wanneer we eindelijk connected zijn.
            
            except OSError as error:
                print(f"ERROR: {error}")
                


    def publish_msg(self, msg):
        TOPIC = self.TOPIC
        message = json.dumps(msg)
        self.client.publish(TOPIC, message)

    


    def disconnect_client(self):
        self.client.loop_stop()
        self.client.disconnect()

    

