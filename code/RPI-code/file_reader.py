

#HET ENIGE NUT HIERVAN IS OM DE FILE TE LEZEN ENZO:

FILENAME_DATA = "data_to_keep"
FILENAME_USERS = "list_of_names"

FILENAME_ADC = "adc_calibration"

FILENAME_COMMENTS = "comment_retirement_list"

class File:

    def __init__(self,file_name_data=FILENAME_DATA,file_of_names=FILENAME_USERS,file_adc_calc=FILENAME_ADC,file_comments=FILENAME_COMMENTS):

        self.FILENAME_DATA = file_name_data
        self.locatie = None #kan ook een auto zijn, want we nemen ze samuhhh
        self.batterij = None
        self.user = None

        self.FILENAME_USERS = file_of_names #De namen van de gebruikers!!

        self.FILENAME_COMMENTS = file_comments

        self.FILENAME_ADC = file_adc_calc #File dat de calibratie punten bijhoudt

    def clear_file_data(self):

        with open(self.FILENAME_DATA,"r") as file:
            lines = file.readlines()
        
        lines[0] = "locatie:\n"
        lines[1] = "batterij:\n"
        
        with open(self.FILENAME_DATA,"w") as file:
            lines = file.writelines(lines)

    def read_file(self):

        with open(self.FILENAME_DATA,"r") as file:
            content = file.read()

        counter = 0 #houd bij welke lijn we nu op zitte

        for line in content.strip():
            tag_id_read = line.split(":")[1]
            if counter == 0:
                self.locatie = tag_id_read
            elif counter == 1:
                self.batterij = tag_id_read
            else:
                break
            counter += 1

    def save_locatie(self,tag_id):
        self.locatie = tag_id

    def save_batterij(self,tag_id):
        self.batterij = tag_id

    def save_user(self,username):
        self.user = username

        with open(self.FILENAME_DATA,"r") as file:
            lines = file.readlines()
        
        lines[2] = f"user:{username}"

        with open(self.FILENAME_DATA,"w") as file:
            file.writelines(lines)
    
    def save_to_file(self):

        locatie = self.locatie
        batterij = self.batterij
        user = self.user

        if locatie == None or batterij == None:
            print(f"ERROR: Couldn't save, not all data was saved!: Locatie:{locatie}, Batterij:{batterij}")
            return None
        with open(self.FILENAME_DATA,"r") as file:
            lines = file.readlines()
        lines[0] = f"locatie:{locatie}\n"
        lines[1] = f"batterij:{batterij}\n"

        with open(self.FILENAME_DATA,"w") as file:
            file.writelines(lines)




    def get_list_names(self):

        name_list = []

        with open(self.FILENAME_USERS,"r") as file:
            content = file.read()
        
        for line in content.strip().splitlines():
            name_list.append(line)
        

        return name_list
    
    def get_list_comment_retirement(self):

        comment_list = []

        with open(self.FILENAME_COMMENTS,"r") as file:
            lines = file.readlines()

        for line in lines:
            comment_list.append(line.strip())

        return comment_list

    def save_to_adc_file(self,line,volt_adc,volt_bat):

       
        with open(self.FILENAME_ADC,"r") as file:
            lines = file.readlines()
        if line == 0:
            lines[0] = f"volt_point1:{volt_adc},{volt_bat}\n"
        elif line == 1:
            lines[1] = f"volt_point2:{volt_adc},{volt_bat}\n"
        else:
            print("ERROR: Not a valid line given, line:{line}")
            return None
        
        with open(self.FILENAME_ADC,"w") as file:
            file.writelines(lines)

    def get_adc_file_data(self):

        with open(self.FILENAME_ADC,"r") as file:
            lines = file.readlines()

        first_point_string = lines[0].split(":")[1]
        x1,y1 = first_point_string.split(",")

        second_point_string = lines[1].split(":")[1]
        x2,y2 = second_point_string.split(",")

        first_point = (float(x1),float(y1))
        second_point = (float(x2),float(y2))

        return first_point,second_point
    
    def get_data_aprils_and_user(self):

        with open(self.FILENAME_DATA,"r") as file:
            lines = file.readlines()
        
        locatie = lines[0].split(":")[1]
        batterij = lines[1].split(":")[1]
        user = lines[2].split(":")[1]

        return locatie,batterij,user


        





        



            

    
    
        















    






