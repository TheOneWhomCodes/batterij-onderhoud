import board #ja het echte bordje op onze breadbord
import busio #Ik denk dat dit ons kan laten werken op de bussen zelf
import adafruit_ads1x15.ads1115 as ADS #onze driver voor de ADS1115
from adafruit_ads1x15.analog_in import AnalogIn #hiermee kunnen we tussen die kanalen lezen



from file_reader import File

file_manager = File()


#we maken een I2c bus

i2c = busio.I2C(board.SCL,board.SDA)

#we maken een ads object

ads = ADS.ADS1115(i2c)

gain = 1  #onze gain is een programmeerbare waarde die we kunnen instellen op de adc om te zeggen tussen welke spanningen hij mag meten.
# en 1 laats ons meten tussen 0 en ±4 V

data_rate = 8 # De data rate is hoe snel die kan uitlezen

ads.gain = gain #dit laat ons lezen tussen 0 en 6V
ads.data_rate = data_rate



#channel = AnalogIn(ads,0) #We maken een channel tussen poort 0 en de GND, die we kunnen meten


LIMIT_PORTS = 4 #er zijn maar vier poorten die we kunnen gebruiken

SMALL_RESISTOR_VALUE = 0.05 #Ohm.
#Dit is de waarde van de weesrstand waarmee we onze stroom van de batterij gaan meten




class ADC:

    def __init__(self,i2c=i2c,adc=ads,port_limit=LIMIT_PORTS,current_resistor=SMALL_RESISTOR_VALUE):
        self.port_limit = port_limit
        

        self.ADC = adc



        #---------------- voor de lineaire interpolatie
        self.standard_volt_point_1 = (0,0) #x-as adc, y-as batterij spanning
        self.standard_volt_point_2 = (3.3,14)

        self.resistor_value = current_resistor #current als in stroom, a friet


        
    def measure_volt_on_port(self,port_number=0,gain=1):
        
        adc = self.ADC
        adc.gain = gain # 1 gain laat u lezen tot 4V 

        port_limit = self.port_limit

        if port_number >= port_limit or port_limit < 0:
            print(f"ERROR: Invalid port given. Port:{port_number} does not exist.")
            return None

        current_channel = AnalogIn(adc,port_number)
            
        
        discard_read = current_channel.voltage
        #blijkbaar moet de ADC nog kunnen switchen dus doen we een "dummy" read
        discard_read2 = current_channel.voltage
        #We doen er voor de veiligheid nog één
        
        voltage = current_channel.voltage

        #print(f'discarded:{discard_read}, and:{discard_read2}, true voltage:{voltage}')
        return voltage
    
    def measure_volt_two_ports(self,port_num1,port_num2,gain=16):
        adc = self.ADC
        adc.gain = gain # 16 gain laat u lezen tot 0.256V, met een stap van 7.8125 micro Volt

        port_limit = self.port_limit

        if (port_num1 >= port_limit or port_num1 < 0) or (port_num2 >= port_limit or port_num2 < 0):
            print(f"ERROR: Port or ports given are invalid. Ports:{port_num1},{port_num2}. Your limit is {port_limit}" )
            return None
        
        current_channel = AnalogIn(adc,port_num1,port_num2)
        
        discard_read = current_channel.voltage
        #blijkbaar moet de ADC nog kunnen switchen dus doen we een "dummy" read
        discard_read2 = current_channel.voltage
        #We doen er voor de veiligheid nog één
        

        diff_voltage = current_channel.voltage

        #print(f"Discarded:{discard_read}, and:{discard_read2}, different:{diff_voltage}")

        return diff_voltage

    def calibrate_adc_first(self,minimum_volt):

        print(f"measuring adc on source volt:{minimum_volt}")

        voltage_adc = self.measure_volt_on_port()

        if voltage_adc is None:
            print("ERROR: Couldn't measure adc voltage, maybe check the ports?.")
            return None
        self.standard_volt_point_1 = (voltage_adc,minimum_volt)

        file_manager.save_to_adc_file(0,voltage_adc,minimum_volt)

        return True #ik return True om te zeggen dat het een succes was

    def calibrate_adc_second(self,maximum_volt):

        print(f"measuring adc on source volt:{maximum_volt}")

        voltage_adc = self.measure_volt_on_port()

        if voltage_adc is None:
            print("ERROR: Couldn't measure adc voltage, maybe check the ports?.")
            return None
        
        self.standard_volt_point_2 = (voltage_adc,maximum_volt)

        file_manager.save_to_adc_file(1,voltage_adc,maximum_volt)

        return True

    def get_adc_calibrated(self):

        volt_point_1, volt_point_2 = file_manager.get_adc_file_data()

        if volt_point_1 is None or volt_point_2 is None:
            print(f"ERROR: Couldn't get adc data, point 1:{volt_point_1}, point 2: {volt_point_2}")
            return None
        self.standard_volt_point_1 = volt_point_1
        self.standard_volt_point_2 = volt_point_2

        return True
    
    def calculate_battery_voltage(self):

        x1,y1 = self.standard_volt_point_1
        x2,y2 = self.standard_volt_point_2

        #print(f"x1:{x1},y1:{y1}  x2:{x2},y2:{y2}")


        measured_voltage = self.measure_volt_on_port()

        print(measured_voltage)

        bat_voltage = y1 + ((measured_voltage-x1)/(x2-x1)) * (y2-y1)

        print(bat_voltage)

        return bat_voltage
    
    def calculate_battery_current(self):
        current_resistor_value = self.resistor_value #current als in stroom


        voltage_over_resistor = self.measure_volt_two_ports(2,3)


        if voltage_over_resistor is None:
            print(f"ERROR: Voltage measuring failed. Voltage:{voltage_over_resistor}")


        current = voltage_over_resistor / current_resistor_value

        return current
    
    def calculate_estimation(self,battery_volt):

        calculated_volt = battery_volt - 9 # vor de omzetting naar percent zo 14 - 9 snap je

        percent = (calculated_volt // 5) * 100

        to_string = str(percent)

        percent_piece = to_string[0:5] #Twee getallen na de komma

        new_percent = float(percent_piece)

        return new_percent



        





