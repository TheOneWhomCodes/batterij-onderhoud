import paho.mqtt.client as mqtt
import json

#from pymongo import MongoClient
#from bson import ObjectId


from DB import Database
from receiver_class import Receiver
import time






#MongoDB SETUP
#-------------------------------------------------

DB = Database()

#Receiver SETUP

receiver = Receiver()





#MQTT SETUP
#-------------------------------------------------
DEFAULT_PORT = 1883 #-> de standaard poort voor unecrypted messages voor onze mqtt broker
ALIVE_TIME = 120 #-> Als de broker niks hoort na 60 seconden dan gaat hij niet meer luisteren
BROKER = "test.mosquitto.org" #-> onze broker die we gebruiken voor de mqtt

TOPIC_APRIL = "RPITSM2/april_detection" #-> de topic waar we op subscriben voor april detection
TOPIC_METER = "RPITSM2/meter"  #-> de topic waar we op subscriben voor de meter

GENERAL_TOPIC = "RPITSM2/general"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)




toggle = False # False is april topic, True is meter topic
def on_connect(client,userdata, flags, reason_code, properties):
    client.subscribe(GENERAL_TOPIC)



    
def on_message(client,userdata,msg):
    
    data_to_string = msg.payload.decode("UTF-8") # -> UTF-8 verandert bytes in leesbare text
    loaded_data = json.loads(data_to_string)

    dataType = loaded_data["dataType"]


    print(dataType)
    if dataType == "april":
        tagId = loaded_data["tagId"]

        receiver.update_all_collections(tagId)
        
    elif dataType == "retirement":
        tagId = loaded_data["tagId"]
        comment = loaded_data["comment"]
        print(f"tag:{tagId} with the comment:{comment}")
        
    else:

        raw_data = loaded_data["raw_data"]
        estimation = loaded_data["estimation"]
    
        
        locatie = loaded_data["locatie"].split("\n")[0]
        batterij = loaded_data["batterij"].split("\n")[0]
        
        if len(locatie) == 0 or len(batterij) == 0:
            print(f"ERROR: Locatie or batterij hebben geen ID. Loc:{locatie}, bat:{batterij}")
            return
        user = loaded_data["user"]
        
       
        print(f'ids locatie:{locatie}, batterij:{batterij}')
        print(raw_data,estimation,locatie,batterij,user)
        receiver.save_adc_data(raw_data,estimation,int(batterij),int(locatie),user)
    
    
    

    


client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, DEFAULT_PORT, ALIVE_TIME)

client.loop_start()




print("STARTING UP MQTT RECEIVER")

print("----------------------------------------------------------")



        



















    

    