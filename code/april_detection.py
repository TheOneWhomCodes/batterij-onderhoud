import subprocess
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


#MQTT_manager = MQTT()
#MQTT_manager.connect_client()

OLED = Display()

file_reader = File()


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

                    
def save_jpeg(jpeg):
    #cur_pic.jpg 
    with open("cur_pic.jpg","wb") as file:
        file.write(jpeg)




def show_you_are_running():

    OLED.write_text("RUN: april detection")
    OLED.write_text("Ready to scan!")
    





def display_tags_found(found_IDs): 

    

    FLAVOUR_TEXT = "Scanned apriltags:"

    OLED.wipe_all_lines()

    OLED.write_text(FLAVOUR_TEXT)
    OLED.write_text(" ")
    


    IDs_in_string = ""


    for ID in found_IDs:
        IDs_in_string += str(ID)

        if IDs_in_string == "": continue
        IDs_in_string += ","


    

    found_id_text = f"IDs:{IDs_in_string}"

    
    OLED.write_text(found_id_text)





def save_found_tags(tags):

    main_string = ""

    for tag in tags:
        main_string += str(tag)
        main_string += ","

    with open("multiple_tags.txt","w") as apriltag_file:
        apriltag_file.write(main_string)






order_operation = 0

def show_track(patience=False):
    global order_operation
    OLED.wipe_all_lines()

    if patience:
        OLED.write_text("Please be patient!")
    elif order_operation == 0:
        OLED.write_text("Please scan location:")
    elif order_operation == 1:
        OLED.write_text("Please scan battery:")
    else:
        OLED.write_text("scan completed!")

    


def keep_track(tag_id):

    global order_operation

    if order_operation == 0: #onze oder of operations begint met onze locatie te scanne (0)
        
        if not (tag_id < 200 and tag_id >= 0):
            print(f"ERROR: Tag {tag_id} is not a valid location.")
            return None
        
        file_reader.save_locatie(tag_id)
        order_operation = 1
        

    elif order_operation == 1:
        
        if not (tag_id <= 586 and tag_id >= 200):
            print(f"ERROR: Tag {tag_id} is not a valid battery.")
            return None
        
        file_reader.save_batterij(tag_id)
        order_operation = None #Ik zet da op None, omdat er geen operaties meer moeten gedaan worden
        
    
        

        
def show_tag_options(tags):

    FLAVOUR_TEXT = "Please pick a tag!"
 
    OLED.wipe_all_lines()

    OLED.write_text(FLAVOUR_TEXT)

    for tag in tags:
        OLED.write_text(str(tag))
    
    scroller = Rotary(OLED=OLED,base_index=1,ceiling_index=0)
    scroller.thread.join()

   
    selected_tag = scroller.selected_item

    if selected_tag is None:
        return None
    
    print("donee")
    return int(selected_tag)
        



def skip_to_latest_frame(stream):

    for i in range(60):
        jpeg = get_jpeg(stream=stream)





OLED_WAIT_TIME = 1 # om ons ID te zien op de OLED, anders gingen we het plaatsen en dan direct weg doen





show_track() #laat zien wat we nu moeten scannen eigenlihk



currently_scanning = False

try:

    while True:


        if currently_scanning:
            continue
        
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
            keep_track(found_ids[0])
        else:
            #hier doen dat ons menu komt voor meerdere
            currently_scanning = True

            tag = show_tag_options(found_ids)
            

            show_track(patience=True)
            
            if tag is not None:
                skip_to_latest_frame(process.stdout)
                keep_track(tag)
                
            currently_scanning = False
            
            
        show_track()

        if order_operation is None:
            break


except KeyboardInterrupt:
        print("stopped")
        
finally:
    
    process.terminate()
    process.wait()
    
    
    #MQTT_manager.disconnect_client()






time.sleep(OLED_WAIT_TIME) 

file_reader.save_to_file()
process.terminate()
process.wait()
#MQTT_manager.disconnect_client()








    
