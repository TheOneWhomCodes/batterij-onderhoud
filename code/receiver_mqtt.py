import paho.mqtt.client as mqtt
import json

#from pymongo import MongoClient
#from bson import ObjectId


from DB import Database
import time





#MongoDB SETUP
#-------------------------------------------------

DB = Database()





#MQTT SETUP
#-------------------------------------------------
DEFAULT_PORT = 1883 #-> de standaard poort voor unecrypted messages voor onze mqtt broker
ALIVE_TIME = 60 #-> Als de broker niks hoort na 60 seconden dan gaat hij niet meer luisteren
BROKER = "test.mosquitto.org" #-> onze broker die we gebruiken voor de mqtt
TOPIC = "RPITSM2/april_detection" #-> de topic waar we op subscriben


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)



def on_connect(client,userdata, flags, reason_code, properties):
    client.subscribe(TOPIC)
    
    
def on_message(client,userdata,msg):
    data_to_string = msg.payload.decode("UTF-8") # -> UTF-8 verandert bytes in leesbare text
    loaded_data = json.loads(data_to_string)
    converted_data = set(loaded_data)
    
    
    
    
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, DEFAULT_PORT, ALIVE_TIME)

client.loop_start()




print("STARTING UP MQTT RECEIVER")
print("----------------------------------------------------------")
















    

    