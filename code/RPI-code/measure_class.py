
from gpiozero import Button, LED

import threading



from adc_class import ADC




TRANSISTOR = LED(16) #We gebruiken het LED Object om de transistor aan en uit te kunnen doen.
#De 6 staat ook voor GPIO6 en niet pin 6

BUTTON = Button(12,pull_up=True) #We sluiten de knop aan op GPIO 12.

ADC_reader = ADC()



class Measure:


    def __init__(self,button=BUTTON,transistor=TRANSISTOR):


        self.battery_voltage = None
        self.battery_voltage_load = None
        self.battery_current = None
        self.estimation = None


        self.BUTTON = button
        self.TRANSISTOR = transistor

        

        self.BUTTON.when_pressed = self.measure_on_press

        self.wait_event = threading.Event() #Ik maak een event aan

        self.thread = threading.Thread(target=self.main) #we maken een thread die de pause functie zal laten lopen

        self.thread.start() #we starten onze thread

        

    
    def measure_on_press(self):
        self.wait_event.set() #we vuren onze wait event af

        #we mogen niet te veel werk geven aan de callback functie

        
    
    def main(self):

        self.wait_event.wait() #We laten onze thread NIET verder gaan tot dit event is afgevuurd

        battery_voltage = ADC_reader.calculate_battery_voltage()
        self.battery_voltage = battery_voltage

        self.TRANSISTOR.on()

        battery_voltage_load = ADC_reader.calculate_battery_voltage()
        battery_current = ADC_reader.calculate_battery_current()


        self.battery_current = battery_current

        self.TRANSISTOR.off()
        
        estimation = ADC_reader.calculate_estimation(battery_voltage)

        self.estimation = estimation

        self.battery_voltage_load = battery_voltage_load

        self.BUTTON.close()
        
        #we sluiten alles af


    













        
    
        
        

