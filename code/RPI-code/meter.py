import sys
import os
import subprocess
import time

from MQTT_script import MQTT
from file_reader import File
from OLED_display import Display

from measure_class import Measure




#------------------------------------ command voor de main script.
cmd_main = ["/home/raspberry/apriltag_env/bin/python",
             "/home/raspberry/main.py"]

#------------------------------------ file reader.
file_manager = File()

#------------------------------------ mqtt data

ALIVE_TIME = 60 #-> Als de broker niks hoort na 60 seconden dan gaat hij niet meer luisteren
TOPIC = "RPITSM2/general" #-> de topic waar we op subscriben

MQTT_manager = MQTT(topic=TOPIC,alive_time=ALIVE_TIME)
MQTT_manager.connect_client()



#------------------------------------ OLED setup

OLED = Display()

OLED.write_text("Press the button!")
OLED.write_text("waiting for measure.")


meter = Measure()

meter.thread.join() #we laten dit programma niet lopen TOT er gemeten is.


OLED.write_text("Completed!")

voltage = meter.battery_voltage
load_voltage = meter.battery_voltage_load
current = meter.battery_current
estimation = meter.estimation

raw_data = {"voltage":voltage,"load_voltage":load_voltage,"current":current}


locatie,batterij,user = file_manager.get_data_aprils_and_user()

payload = {"dataType":"meter","raw_data":raw_data,"estimation":estimation,"locatie":locatie,"batterij":batterij,"user":user}

MQTT_manager.publish_msg(payload)


#sys.exit("pls out")
MQTT_manager.disconnect_client()
#print("we're leaving the damn script..")

#sys.exit()

os._exit(0)























