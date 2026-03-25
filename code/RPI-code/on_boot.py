
import socket

import time
import subprocess
import os
from OLED_display import Display
from file_reader import File

from rotary_class import Rotary

from adc_class import ADC

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)



# we willen graag onze ip adres weten, dus moeten we met de OS "connecteren" namelijk door de import socket
# We vragen aan hem als we een IPv4 adres zouden gebruiken (socket.AF_INET) en we de UDP protocol gebruiken voor ons transport(socket.SOCK_DGRAM)

s.connect(("8.8.8.8",80))
#en als we zouden connecteren met google op poort 80, welk adres zou ons OS gebruiken?

ip = s.getsockname()[0] #Hij geeft dan ons zijn ip adres en de lokale poort die we gebruiken in een tupel

s.close() #Nu dat we ons adres hebben sluiten we onze "connectie" met google


OLED = Display()

file_reader = File()

#------------------- ADC yap
ADC_reader = ADC()
MIN_VOLT = 6 #de eerste punt van onze calibratie.
MAX_VOLT = 14 #de tweede punt van onze calibratie


BOOT_MSG = "Booting up.."
DEVICE_MSG = "RPI Zero 2 W"

DIMENSIONS_MSG = f"DIM: {OLED.WIDTH} x {OLED.HEIGHT}"

IP_ADDRESS_MSG = f"IP:{ip}"

PATIENCE_MSG = "Please be patient."




cmd_april = ["/home/raspberry/apriltag_env/bin/python",
       
       "/home/raspberry/april_detection.py"

]

cmd_meter = ["/home/raspberry/apriltag_env/bin/python",
             "/home/raspberry/meter.py"]

cmd_main = ["/home/raspberry/apriltag_env/bin/python",
             "/home/raspberry/main.py"]




INTERVAL_MSGS = 1.5 # seconden per keer dat we iets toevoegen

FINAL_WAIT = 1#seconden dat we wachten voor we deze stoppen
print("----------------------------------")

#-----------------------------------  BOOT SEQUENCE


print(BOOT_MSG)
OLED.write_text(BOOT_MSG)

time.sleep(INTERVAL_MSGS)

print(DEVICE_MSG)
OLED.write_text(DEVICE_MSG)

time.sleep(INTERVAL_MSGS)

print(DIMENSIONS_MSG)
OLED.write_text(DIMENSIONS_MSG)

time.sleep(INTERVAL_MSGS)

print(IP_ADDRESS_MSG)
OLED.write_text(IP_ADDRESS_MSG)



print(PATIENCE_MSG)
OLED.write_text(PATIENCE_MSG)

time.sleep(FINAL_WAIT)


#------------------------------ CALIBRATION CHOOSE?:

OLED.wipe_all_lines()

OLED.write_text("Want to calibrate?")
OLED.write_text("Yes")
OLED.write_text("No")

scroller = Rotary(OLED=OLED,base_index=2,ceiling_index=0)

scroller.thread.join() #we laten onze main programma niet lopen TOT de scroller klaar is.

answer = scroller.selected_item

if answer == "Yes":

    #------------- eerste calibratie
    OLED.wipe_all_lines()

    OLED.write_text("Calibrate at 6V.")
    OLED.write_text("Done.")

    scroller = Rotary(OLED=OLED,base_index=1,ceiling_index=0)

    scroller.thread.join()

    ADC_reader.calibrate_adc_first(MIN_VOLT)
    #------------- tweede calibratie

    OLED.wipe_all_lines()

    OLED.write_text("Calibrate at 14V.")
    OLED.write_text("Done.")

    scroller = Rotary(OLED=OLED,base_index=1,ceiling_index=0)

    scroller.thread.join()

    ADC_reader.calibrate_adc_second(MAX_VOLT)


    





#------------------------------ VERIFICATION

file_reader.clear_file_data() #clearen onze file van data ja

names = file_reader.get_list_names()

OLED.wipe_all_lines()


OLED.write_text("Please pick your name")

for name in names:
    OLED.write_text(name)



scroller = Rotary(OLED=OLED,base_index=3,ceiling_index=0)

scroller.thread.join() #we laten onze main programma niet lopen TOT de scroller klaar is.
username = scroller.selected_item

scroller.close()

file_reader.save_user(username)



#cmd_main[0] we moeten de pad geven en dan de command
# os.execv kills de huidige proces om dan een andere uit te voeren.
os.execv(cmd_main[0], cmd_main)

#proc = subprocess.run(cmd) #nu lopen we onze scanner, yay!








