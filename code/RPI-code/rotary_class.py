from gpiozero import RotaryEncoder, Button
import threading
from signal import pause







class Rotary:


    def __init__(self,OLED,max_steps=0,ceiling_index=0,base_index=0):

        #HERHALING:, base_index is waar de scroller start op het scherm van je huidige elementjes,
        #ceiling_index is waar je niet verder naar boven mag scrollen

        self.OLED = OLED
        self.OLED.init_small_scroller(base_index,ceiling_index)

        self.ENCODER = RotaryEncoder(
            a = 17, #CLK, GPIO 17
            b = 27, #DT, GPIO 27
            max_steps = max_steps #hoeveelheid stappen (als op 0 is, dan oneindig hoeveelheid)
        )

        self.SWITCH = Button(22,pull_up=True) #SW, GPIO 22

        self.ENCODER.when_rotated_clockwise = self.scroll_down
        self.ENCODER.when_rotated_counter_clockwise = self.scroll_up
        
        self.SWITCH.when_pressed = self.select_item

        self.selected_item = None

        
        self.wait_event = threading.Event() #Ik maak een event aan

        self.thread = threading.Thread(target=self.pause) #we maken een thread die de pause functie zal laten lopen
        
        self.thread.start() #we starten onze thread
    
    def scroll_down(self):
        self.OLED.scroll_down()
    def scroll_up(self):
        self.OLED.scroll_up()
    def select_item(self):
        selected = self.OLED.select_element_on_scroller()

        self.selected_item = selected
        
        self.wait_event.set() #we vuren onze wait event af
    

    def pause(self):

        

        self.wait_event.wait() #We laten onze thread NIET verder gaan tot dit event is afgevuurd

        self.close()
        #we sluiten alles af
        
    def close(self):
        try:
            self.ENCODER.close()
        except:
            pass

        try:
            self.SWITCH.close()
        except:
            pass

        try:
            self.OLED.disable_small_scroller()
        except:
            pass
        

        #we sluiten alles af
        


    




        


        





    
        




    




















