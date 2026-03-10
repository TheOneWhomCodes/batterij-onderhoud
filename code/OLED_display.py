from luma.core.interface.serial import i2c #-> we gebruiken i2c als ons middel van communicatie
from luma.oled.device import sh1106, ssd1306 #-> deze twee chips zijn meestal gevonden in goedkope oleds zoals de onze
from PIL import Image, ImageDraw, ImageFont #-> Deze library gebruiken we om een een virtuelle foto te maken en die dan te sturen op de oled

import time

serial = i2c(port=1,address=0x3C)
#-> Serial is de naam omdat we seriële communicatie gebruiken
#port=1 ->  onze raspberry pi zero 2w gebruikt pin 1 als I2C bus
#address=0x3C -> onze oled heeft als I2C adres 0x3C 


FOUND_DEVICE = None #A FRIET

try:
    FOUND_DEVICE = sh1106(serial) #-> we checken als deze chip aanwezig is om te zien als we ermee kunnen praten
    print("sh1106 is onze control chip!")
except:
    FOUND_DEVICE = ssd1306(serial) #-> aangezien het ander niet werd gevonden moet deze hem zijn
    print("ssd1306 is onze control chip!")

WIDTH = FOUND_DEVICE.width
HEIGHT = FOUND_DEVICE.height

TEXT_FONT = ImageFont.load_default()
#-> ImageFont.load_default() laadt een klein basic text font 

WHITE = 255 #Tja we werken met iets monochroom dus kan onze kleur wit of zwart zijn


SCREEN = Image.new("1", (WIDTH,HEIGHT)) #Ons virtuelle foto waar we op gaan tekenen
#-> param 1. "1" staat voor dat we een monochrome foto willen maken
#-> param 2. (WIDTH,HEIGHT) staat voor onze dimensies van de foto

PEN = ImageDraw.Draw(SCREEN)
#-> onze pen waarmee we gaan tekenen op onze scherm

TEXT_OFFSET_Y = 16 #-> Hoeveel we onze text met y offseten met onze list_text methode
WIDTH_CHAR = 6 # -> 1 character met ImageFont.load_default() is ongeveer 6 pixels

POINTING_SYMBOL = " <<"


class Display:

    def __init__(self,screen=SCREEN,pen=PEN,device=FOUND_DEVICE,width=WIDTH,height=HEIGHT,font=TEXT_FONT,TEXT_OFFSET_Y=TEXT_OFFSET_Y,width_char=WIDTH_CHAR,pointing_symbol=POINTING_SYMBOL):
        self.SCREEN = screen #-> Het scherm waarop je gaat tekenen
        self.WIDTH = width #-> Width van het scherm
        self.HEIGHT = height #-> Height van het scherm
        self.TEXT_FONT = font#-> font van onze textke


        self.Device = device #-> onze oled display opzich
        self.Pen = pen #Dit is het Draw object om te tekenen/schrijven

        self.pointer_text = 0 #-> de y-as pointer basically, stel we hebben text gezet op
        #coordinate 0,0 dan willen we bv de y coordinate standaard opschuiven met 16 naar beneden
        #om er mooi terug text te kunnen zetten

        self.TEXT_OFFSET_Y = TEXT_OFFSET_Y # is de waarde waarmee onze text offseten
        #op de y-as elke keer als we text toevoegen

        

        self.MAX_LINES = height // self.TEXT_OFFSET_Y # ja 64 delen door 16 geeft ons 4 lijnen
        self.MAX_CHARS_PER_LINE = self.WIDTH // width_char #met 128 pixels wide kunnen we ong. 21 characters hebben per lijn

        self.current_line = 0 #onze houdige lijn waarop we tekst willen schrijven

        self.lines_of_text = {} #houdt alle lijnen bij om ons systeem scrollable te maken

        self.lines_on_screen = [] # dit zal de laatste 4 lijnen van tekst hebben om te laten zien op de OLED

        self.scroll_pointer = 0 #de lijn waarvan we gaan scrollen

        self.scroll_screen_pointer = 0 #de pointer dat echt scrolled tussen de elementen op de huidige screen
        #dit gaat tussen 0 en max aantal lijnen die je kan zien
        
        self.enabled_screen_scrolling = False #Dit zegt als we mogen scrollen op de elementen op de huidige screen

        self.POINTING_SYMBOL = pointing_symbol
        self.LEN_SYMBOL = len(self.POINTING_SYMBOL) 

        self.ceiling_pointer_index = -1 #dus vanaf hier mag NIET meer naar boven gescrolled worden of anders, dood straf
        #en ja das standaard op -1, want standaard willen we tot het bovenste elementje scrollen


    def text_setter(self,text): #checked hoeveel karakters van de tekst die we hebben en zet die dan op de onderste lijn 
        length_text = len(text) #als er meer dan 20 karakters zijn
        MAX_LENGTH = self.MAX_CHARS_PER_LINE

        while length_text > MAX_LENGTH:
            new_text = text[0:MAX_LENGTH]

            self.lines_of_text[self.current_line] = new_text


            self.current_line += 1

            text = text[MAX_LENGTH:]
            length_text = len(text)
        if length_text == 0: return

        self.lines_of_text[self.current_line] = text
        self.current_line += 1
        

    
    def write_text(self,text): #hiermee schrijven we onze tekst
        

        MAX_LINES = self.MAX_LINES
        
        self.text_setter(text) #eerst zetten we die in onze dict van teksten
        self.show_screen() #we veranderen onze virtuelle foto om de laatste vier teksten te zien

        self.scroll_pointer = self.current_line - MAX_LINES  #reset de scroll pointer terug naar de eerste lijn die we zien

        if self.enabled_screen_scrolling:
            self.disable_small_scroller()

    

    def show_screen(self,refresh=True): # we itereren over een lijst van vier elementen van tekst om die te laten zien


        self.clear_screen()

        if refresh: #refresh is er omdat tijdens scrollen ik al refresh, en tja tijdens writen moet da refreshen automatisch
            self.refresh_screen()


        FONT = self.TEXT_FONT
        FILL = 255

        current_lines = self.lines_on_screen
        amount_lines = len(current_lines) 
        

        current_line = 0 
        while current_line < amount_lines:

            Y_coords = current_line * self.TEXT_OFFSET_Y
            coords =  (0,Y_coords)
            text = current_lines[current_line]

            self.Pen.text(coords,text,font=FONT,fill=FILL)

            self.Device.display(self.SCREEN) #we laten het op onze scherm zien

            current_line += 1 #we moven up dichter naar het laatste
       

                


    
    def refresh_screen(self,given_index=None): # refreshed onze laatste vier elementen die we graag willen zien op onze OLED

        self.lines_on_screen = []
        final_line = len(self.lines_of_text) - 1

        
        start_index = (final_line - self.MAX_LINES ) + 1
     
        if start_index < 0: start_index = 0

        if not given_index is None: start_index = given_index


        for line in range(start_index,final_line+1):

            text = self.lines_of_text[line]
            self.lines_on_screen.append(text)
        


    
    def clear_screen(self): #tja cleared de screen gewoon 

        self.SCREEN = Image.new("1",(self.WIDTH,self.HEIGHT))
        self.Pen = ImageDraw.Draw(self.SCREEN)

        self.Device.display(self.SCREEN)

    

    def init_small_scroller(self,base_index=None,ceiling_index=None):

        if base_index == None:
            base_index = 0
        #base_index staat voor waar we deze pointer standaard zetten
        #normaal is die 0, maar stel we scrollen naar boven dan staat hij op het dan "laatste" element

        if ceiling_index == None:
            ceiling_index = self.ceiling_pointer_index
        

        POINTING_SYMBOL = self.POINTING_SYMBOL
        

        screen_lines = self.lines_on_screen

        length_screen_lines = len(screen_lines) 

        self.enabled_screen_scrolling = True #We zetten deze op true 

        self.scroll_screen_pointer = base_index #we zetten hem op een elementske

        self.ceiling_pointer_index = ceiling_index

        

        current_screen_pointer = self.scroll_screen_pointer

        if length_screen_lines <= 0:
            print("ERROR: Nothing written on screen, can't put scroller")
        
        self.lines_on_screen[current_screen_pointer] += POINTING_SYMBOL

        #nu nog showen

        self.show_screen(refresh=False)


    def select_element_on_scroller(self):
        POINTING_SYMBOL = self.POINTING_SYMBOL
        LENGTH_SYMBOL = self.LEN_SYMBOL
        screen_lines = self.lines_on_screen 

        current_screen_pointer = self.scroll_screen_pointer
        current_pointing_line = screen_lines[current_screen_pointer]

        last_three_chars = current_pointing_line[-LENGTH_SYMBOL:]

        if last_three_chars == POINTING_SYMBOL: 
            current_pointing_line = current_pointing_line[:-LENGTH_SYMBOL]

        return current_pointing_line





    def disable_small_scroller(self):
        POINTING_SYMBOL = self.POINTING_SYMBOL
        LENGTH_SYMBOL = self.LEN_SYMBOL

        current_screen_pointer = self.scroll_screen_pointer

        self.enabled_screen_scrolling = False #We zetten deze op false, want ja we willen hem nie meer 

        screen_lines = self.lines_on_screen

        

        current_pointing_line = screen_lines[current_screen_pointer]

        last_three_chars = current_pointing_line[-LENGTH_SYMBOL:]

        if last_three_chars == POINTING_SYMBOL: 
            current_pointing_line = current_pointing_line[:-LENGTH_SYMBOL]

            self.lines_on_screen[current_screen_pointer] = current_pointing_line

        

        #nu nog showen

        self.show_screen(refresh=False)



    def scroll_up(self):
       
       #FIX THE CEILING THING BEFORE WORKING
       
        scrolling_enabled = self.enabled_screen_scrolling
        #------------------------------------------------------------- check statements
        if not scrolling_enabled:
            print("ERROR: Tried scrolling while not enabled")
            return None
        

        ceiling_index = self.ceiling_pointer_index

        if ceiling_index < 0:
            ceiling_index = None
            ceiling_element = None
        else:
            ceiling_element = self.lines_of_text[ceiling_index]

        MAX_LINES = len(self.lines_on_screen) #ja de max lijnen we nu hebben op scherm

        
        loop_back_position = MAX_LINES - 1 #ja len telt het nulde element als 1, en onze indexen starten van 0 dus -1

        POINTING_SYMBOL = self.POINTING_SYMBOL
        LENGTH_SYMBOL = self.LEN_SYMBOL

        current_screen_pointer = self.scroll_screen_pointer #mag alleen tussen 0 en max aantal lijnen

        
        current_pointing_line = self.lines_on_screen[current_screen_pointer] #de huidige lijn waar we nu naar wijzen

        last_three_chars = current_pointing_line[-LENGTH_SYMBOL:] #laatste drie karakters

        if last_three_chars == POINTING_SYMBOL: #we checken als de pointer symbool erbij staat
            current_pointing_line = current_pointing_line[:-LENGTH_SYMBOL] #we verwijderen die

            self.lines_on_screen[current_screen_pointer] = current_pointing_line #we saven die verandering


        

        current_screen_pointer -= 1 #we scrollen met 1 elementje boven on de huidige scherm

        current_pointing_line = self.lines_on_screen[current_screen_pointer] #ons gescrolled element

    

        if current_pointing_line == ceiling_element: #we checken als het gelijk is aan onze ceil element
            self.lines_on_screen[current_screen_pointer + 1] += POINTING_SYMBOL #we geven het oorspronkelijke element zijn symbool terug
            print("ERROR: Can't scroll up on screen, reached ceiling element")

            return #en we scrollen niet!!



        if current_screen_pointer < 0:
            
            self.scroll_up_page()

            return

        self.lines_on_screen[current_screen_pointer] += POINTING_SYMBOL #nu krijgt het gescrolled element het pointer symbool

        self.scroll_screen_pointer = current_screen_pointer


        #nu nog showen
        
        self.show_screen(refresh=False)

        
    def scroll_down(self):
        
        scrolling_enabled = self.enabled_screen_scrolling
        if not scrolling_enabled:
            print("ERROR: Tried scrolling while not enabled")
            return None

        MAX_LINES = self.MAX_LINES#ja de max lijnen we nu hebben op scherm

        total_lines = len(self.lines_on_screen)

        POINTING_SYMBOL = self.POINTING_SYMBOL
        LENGTH_SYMBOL = self.LEN_SYMBOL


        loop_back_index = total_lines - 1 #ja len telt het nulde element als 1, en onze indexen starten van 0 dus -1

        current_screen_pointer = self.scroll_screen_pointer

        current_pointing_line = self.lines_on_screen[current_screen_pointer] #de huidige lijn waar we nu naar wijzen

        last_three_chars = current_pointing_line[-LENGTH_SYMBOL:] #laatste drie karakters

        if last_three_chars == POINTING_SYMBOL: #we checken als de pointer symbool erbij staat
            current_pointing_line = current_pointing_line[:-LENGTH_SYMBOL] #we verwijderen die

            self.lines_on_screen[current_screen_pointer] = current_pointing_line #we saven die verandering

        

        

        if current_screen_pointer >= MAX_LINES-1: #ja -1 want uhh als we bij index 3 zijn willen we ook scrollen naar beneden

            self.scroll_down_page()

            return
        

        current_screen_pointer += 1 #we scrollen met 1 elementje beneden on de huidige scherm
        
        if current_screen_pointer >= total_lines:
            print("ERROR: Tried to scroll down to an element out of range.")
            return
        
        self.lines_on_screen[current_screen_pointer] += POINTING_SYMBOL #nu krijgt het gescrolled element het pointer symbool

        self.scroll_screen_pointer = current_screen_pointer

        #nu laten zien
        #loop_back_position HIER IETS DOEN ERMEE A FRIETTTTTTTTTTTT
        self.show_screen(refresh=False)

        
    def scroll_up_page(self):

        #---------------------------------------------- safety check, zodat we niet scrollen boven de ceiling
        ceiling_index = self.ceiling_pointer_index

        if ceiling_index < 0:
            ceiling_index = None
            ceiling_element = None
        else:
            ceiling_element = self.lines_of_text[ceiling_index]

        #-------------------------------------------------


        
        lines_of_text = self.lines_of_text #ja pakt de hele geheugen

        total_lines = len(lines_of_text) #we pakken de lengte

        pointer_index = self.scroll_pointer

        #------------------------------------------------- safety check availability scrolling up in general
        if pointer_index <= 0:
            print(f"ERROR: cannot scroll up anymore, scroll pointer:{pointer_index} lines:{total_lines}")
            return
        #-------------------------------------------------

        
        pointer_index -= 1 #we zetten onze pointer met eentje achter

        #-------------------------------------------------safety check ceiling
        pointing_line = self.lines_of_text[pointer_index]
        if pointing_line == ceiling_element:
            print("ERROR: Can't scroll up page, reached ceiling element")
            return
        #-------------------------------------------------

        
        self.scroll_pointer = pointer_index #we saven da

        self.refresh_screen(pointer_index) # refresh de lines die we willen zien



        if self.enabled_screen_scrolling:
            
            first_index_el = 0 #we beginnen dan met het eerste eh, type e in het testing scriptje om te begrijpen.
            self.init_small_scroller(base_index=first_index_el) #we init onze scroller op onze nieuwe page
        else:
            self.show_screen(False) #we laten het echt zien


    def scroll_down_page(self):

        MAX_LINES = self.MAX_LINES

        lines_of_text = self.lines_of_text #ja pakt de hele geheugen

        total_lines = len(lines_of_text) #we pakken de lengte

        pointer_index = self.scroll_pointer

        

        if pointer_index >= total_lines - MAX_LINES:
            print(f"ERROR: cannot scroll down anymore, scroll pointer:{pointer_index} lines:{total_lines}")
            return
        
        pointer_index += 1
    
        self.scroll_pointer = pointer_index
 
        self.refresh_screen(pointer_index) # refresh de lines die we willen zien

        if self.enabled_screen_scrolling:
            last_index_el = MAX_LINES - 1 #Onze max_lines die we kunnen hebben is 4, maar onze indexen starten met 0
            self.init_small_scroller(base_index=last_index_el)
            print("okey dokey we shall eat")
            #TEMP FIX
        else:
            self.show_screen(refresh=False) #we laten het echt zien, zonder de kleine scroller


    def modify_line(self,new_text,index_line=None,show=False):
        
        #index_line=None, ja als er geen index wordt gegeven dan moeten we een dikke error terug geven
        #show=False, als we direct al onze modificaties willen laten zien dan kunnen we show meegeven als True, maar standaard is die uit

        lines_of_text = self.lines_of_text

        amount_lines = len(lines_of_text) - 1 #ja len geeft ons alle elementen en telt vanaf 1, ja en wij tellen vanaf 0 dus moeten we -1 doen

        length_text =  len(new_text)

        MAX_CHARS = self.MAX_CHARS_PER_LINE

        if index_line == None:
            print("ERROR: No index given for method: modify_line")
            return
        

        elif index_line > amount_lines or index_line < 0:
            print(f"ERROR: Index not between 0 and {amount_lines}")
            return
        
        if length_text > MAX_CHARS:
            print(f"ERROR: Text given is longer than {MAX_CHARS}")
            return

        lines_of_text[index_line] = new_text

        if show:
            self.show_screen()

    def wipe_all_lines(self):

        self.clear_screen()

        self.lines_of_text = {}
        self.lines_on_screen = []

        self.current_line = 0

        self.scroll_pointer = 0


        
    







