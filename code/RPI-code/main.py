import subprocess
import os
import sys


from adc_class import ADC
from OLED_display import Display
from rotary_class import Rotary
from file_reader import File


import time

ADC_reader = ADC()

OLED = Display()



cmd_april = ["/home/raspberry/apriltag_env/bin/python",
       
       "/home/raspberry/april_detection.py"

]

cmd_retirement_scan = ["/home/raspberry/apriltag_env/bin/python",
             "/home/raspberry/april_detection_retirement.py"]

cmd_meter = ["/home/raspberry/apriltag_env/bin/python",
             "/home/raspberry/meter.py"]


WAIT_TIME_SHOW_MODES = 1 #Om die eerste bericht van "choose mode" te laten zien.
DELAY_GPIO = 0.3 #tja idk als dit helpt bro

def main():
    while True:

        OLED.wipe_all_lines()
        OLED.write_text("Choose mode.")

        time.sleep(WAIT_TIME_SHOW_MODES)

    
        OLED.write_text("april scanning")
        OLED.write_text("measurement mode")
        OLED.write_text("retire")
        OLED.write_text("Exit")


        try:

            scroller = Rotary(OLED=OLED,base_index=0,ceiling_index=0)

            scroller.thread.join() #we laten onze main programma niet lopen TOT de scroller klaar is.

            answer = scroller.selected_item

        except Exception as e:
            print(e)
        finally:
            scroller.close()
            time.sleep(DELAY_GPIO)

        if answer == "measurement mode":
            proc = subprocess.Popen(cmd_meter)
            proc.wait()
            

            
            
        elif answer == "april scanning":
            OLED.wipe_all_lines()
            OLED.write_text("april scanning")
            OLED.write_text("chosen")

            proc = subprocess.Popen(cmd_april)
            proc.wait()
            
            
        elif answer == "retire":
            OLED.wipe_all_lines()
            OLED.write_text("starting up!")
            OLED.write_text("retirement script..")

            os.execv(cmd_retirement_scan[0],cmd_retirement_scan)

            
        else:
            print("exiting program.")
            OLED.wipe_all_lines()
            break
            
main()

#print("BURGERRRRR")



















