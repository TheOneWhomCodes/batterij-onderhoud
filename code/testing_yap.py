
from OLED_display import Display

from file_reader import File

from rotary_class import Rotary

from adc_class import ADC


import time

OLED = Display()

file_reader = File()

ADC_reader = ADC()

MINIMUM_VOLT = 6
MAXIMUM_VOLT = 14



OLED.write_text("pizza")
time.sleep(0.5)
OLED.write_text("OOGA")
time.sleep(0.5)

OLED.write_text("chicken nugget")

OLED.write_text("skibidi toilet")

print("laten we zien als scrollen werkt eh")

time.sleep(1)

OLED.write_text("gescroll")
time.sleep(1)
OLED.write_text("scrolled again")







while True:

    inp = input("term: ->> ")

    if inp == "e":
        print(f'lines of text: {OLED.lines_of_text}')
        print(f'current line {OLED.current_line}')
        print(f'current pointer index {OLED.scroll_pointer}')

        print(f"length screen_lines: {len(OLED.lines_on_screen)}")


    elif inp == "up":
        OLED.scroll_up()
    elif inp == "down":
        
        OLED.scroll_down()

    elif inp=="wipe":
        OLED.wipe_all_lines()

    elif inp=="init":
        OLED.init_small_scroller(base_index=1,ceiling_index=1)

    elif inp=="d_page":
        OLED.scroll_down_page()
    elif inp=="u_page":
        OLED.scroll_up_page()
    elif inp=="dis":
        OLED.disable_small_scroller()
    elif inp=="file":
        file_reader.read_file()
        file_reader.clear_file_data()
    elif inp=="rot":
        scroller = Rotary(OLED=OLED)



    
    elif inp=="volt":
        volt = ADC_reader.measure_volt_on_port(0)
        print(volt)
    elif inp=="cal1":
        ADC_reader.calibrate_adc_first(MINIMUM_VOLT)
    elif inp=="cal2":
        ADC_reader.calibrate_adc_second(MAXIMUM_VOLT)
    elif inp=="get_adc_cal":
        ADC_reader.get_adc_calibrated()
    elif inp=="bat_volt":
        bat_volt = ADC_reader.calculate_battery_voltage()
        bat_current = ADC_reader.calculate_battery_current()

        print(f"battery volt:{bat_volt}, battery current:{bat_current}")
    
            
    else:
        OLED.write_text(inp)
        



    

    

    

