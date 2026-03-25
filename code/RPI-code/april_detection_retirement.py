import subprocess
import os
import sys

import numpy as np
import cv2
from pupil_apriltags import Detector

from MQTT_script import MQTT
from OLED_display import Display
from file_reader import File
from rotary_class import Rotary

import time

# Onze command die we lopen
cmd = [
    "rpicam-vid",
    "--codec", "mjpeg",      # MJPEG = makkelijk decoderen
    "--width", "640", #halveer dit als dit goed werkt
    "--height", "480", #halveer dit als dit goed werkt
    "--framerate", "10",
    "--nopreview",
    "--timeout", "0",        # eindeloze stream
    "--output", "-"          # naar stdout streamen
]


cmd_main = ["/home/raspberry/apriltag_env/bin/python",
             "/home/raspberry/main.py"]


TOPIC = "RPITSM2/general"

MQTT_manager = MQTT(topic=TOPIC)

MQTT_manager.connect_client()

file_reader = File()

OLED = Display()




process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

detector = Detector(
    families="tag36h11",
    nthreads=2,
    quad_decimate=2.0,   
    quad_sigma=0.0
)

#Popen = process kan gelezen, en geterminate worden vanaf python zelf
# subprocess.PIPE = hiermee kan python het zelf lezen met
# process.stdout.read()

# process.stdout.read(1) = leest eerste byte en zet pointer verder met 1

jpeg_identifier = b'\xff' # -> die \ zegt dat we over hexadecimalen praten
start_jpeg = b'\xd8'
end_jpeg = b'\xd9'

def get_jpeg(stream):
    
    jpeg_data = b''
    first_byte = stream.read(1)

    if first_byte == jpeg_identifier:

        second_byte = stream.read(1)

        if second_byte == start_jpeg:
            
            previous_byte = second_byte
            jpeg_data = (first_byte + second_byte)
            while True:

                current_byte = stream.read(1)


                if current_byte == end_jpeg and previous_byte == jpeg_identifier:
                    jpeg_data += current_byte
                    break
                jpeg_data += current_byte
                previous_byte = current_byte
            
            return jpeg_data
    return None

                    


#----------------------------


scanned_april = None

def show_you_are_running(patience=False):
    
    OLED.wipe_all_lines()

    if patience:
        OLED.write_text("Please be patient!")
    else:
        OLED.write_text("Please scan the")
        OLED.write_text("the battery to retire")


    

def check_validity(tag_id):
    global scanned_april

    if not (tag_id <= 586 and tag_id >= 200):
        print(f"ERROR: Tag {tag_id} is not a valid battery.")
        return None
    
    scanned_april = tag_id

    return True
    


        
def show_tag_options(tags):

    FLAVOUR_TEXT = "Please pick a tag!"
 
    OLED.wipe_all_lines()

    OLED.write_text(FLAVOUR_TEXT)

    for tag in tags:
        OLED.write_text(str(tag))
    
    scroller = Rotary(OLED=OLED,base_index=1,ceiling_index=0)
    scroller.thread.join()
    scroller.close()

   
    selected_tag = scroller.selected_item

    if selected_tag is None:
        return None
    
    print("donee")
    return int(selected_tag)
        



def skip_to_latest_frame(stream):

    for i in range(60):
        jpeg = get_jpeg(stream=stream)





OLED_WAIT_TIME = 1 # om ons ID te zien op de OLED, anders gingen we het plaatsen en dan direct weg doen

#en nu heeft het nut om onze gpiozero library niet te overbelasten.



show_you_are_running() #laat zien wat we nu moeten scannen eigenlihk




try:

    while True:



        jpeg = get_jpeg(process.stdout)

        if jpeg is None: continue

    
        jpeg_to_array = np.frombuffer(jpeg, dtype=np.uint8)
        # dit verandert de rauwe bytes naar iets wat kan gelezen worden
        # door de cv2
        # uint8 is de manier hoe jpegs hun bytes opslaan

        image = cv2.imdecode(jpeg_to_array,cv2.IMREAD_GRAYSCALE)

        if image is None: continue

        found_results = detector.detect(image)
        
        found_ids = []

        for result in found_results:
            found_id = result.tag_id
            
            found_ids.append(found_id)

        if found_ids == []: continue

    
        amount_found_ids = len(found_ids)
        print(f"The IDs we've found: {found_ids}")

        
        
        if amount_found_ids == 1:
            tag_id = found_ids[0]
            valid = check_validity(tag_id)

            if valid:
                break
        else:
            #hier doen dat ons menu komt voor meerdere
            currently_scanning = True

            tag = show_tag_options(found_ids)
            

            show_you_are_running(patience=True)
            
            if tag is not None:
                skip_to_latest_frame(process.stdout)
                valid = check_validity(tag)

                if valid:
                    
                    break


except KeyboardInterrupt:
        print("stopped")
        
finally:
    
    process.terminate()
    process.wait()

    
OLED.wipe_all_lines()

comments = file_reader.get_list_comment_retirement()

for comment in comments:
    OLED.write_text(comment)

print("rotay boy lmao")

try:

    scroller = Rotary(OLED=OLED,ceiling_index=-1,base_index=0)

    scroller.thread.join() #we laten onze main programma niet lopen TOT de scroller klaar is.

    comment_chosen = scroller.selected_item
except Exception as e:
    print(e)



payload = {"dataType":"retirement","tagId":scanned_april,"comment":comment_chosen}

MQTT_manager.publish_msg(payload)

MQTT_manager.disconnect_client()

os.execv(cmd_main[0],cmd_main)










    
