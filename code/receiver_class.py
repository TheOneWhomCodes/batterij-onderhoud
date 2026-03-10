
from DB import Database

import time



class Receiver:



    def __init__(self):

        self.DB = Database()

        self.not_included = ["_id"] #voor de copy_dict functie, we mogen geen _id veranderen op mongoDB

    
    def decide_group_tag(self,tag_id):

        if not isinstance(tag_id,int):
            print("ERROR: not given an integer tag id:{tag_id}")

        group = None
        if tag_id <= 586 and tag_id >= 200:
            group = "batterij"
        elif tag_id < 200 and tag_id >= 0:
            group = "locatie/auto"
    
        return group
    

    
    def save_to_database(self,tag_id):

        
        database = self.DB

        apriltag_document = self.get_apriltag(tag_id)

        assignment_document = self.get_tag_assignment(tag_id)

        group = self.decide_group_tag(tag_id)

        if group == "batterij":
            UID = assignment_document["assignedId"]
            database.connect_to_collection("BATTERIJEN")
            group_document = database.retrieve_document("batUID",UID)
        else:
            UID = assignment_document["assignedId"]
            database.connect_to_collection("LOCATIES/AUTOS")
            group_document = database.retrieve_document("name",UID)
        
        if group_document == None:
            pass
            #tja hier iets doen zodat we nieuwe records kunnen maken als het nie besta
        return

        
        
    def get_apriltag(self,tag_id):

        database = self.DB

        database.connect_to_collection("APRILTAGS")

        found_document = database.retrieve_document("tagId",tag_id)

        group = self.decide_group_tag(tag_id)
        if found_document == None:
            new_april_document = {"tagId":tag_id,"assignmentType":group,"active":True}
            database.insert_document(new_april_document)
            found_document = new_april_document
        
        return found_document
    
    
    def get_tag_assignment(self,tag_id,assignedId=""):

        database = self.DB

        database.connect_to_collection("TAG_ASSIGNMENTS")

        found_document = database.retrieve_document("tagId",tag_id)

        group = self.decide_group_tag(tag_id)
        current_time = self.get_current_time()

        if found_document == None:
            new_assignment_document = {"tagId":tag_id,"assignmentType":group,"assignedId":assignedId,"validFrom":current_time,"validTo":""}
            database.insert_document(new_assignment_document)
            found_document = new_assignment_document

        return found_document
    
    
    










        
        

        







            
            






























        



    
    #extra functies dat helpen
    #-------------------------------------------------------------------------------------

    def copy_dict(self,dictionairy,not_included=None):
        new_dict = {}
    
        if not_included == None:
            not_included = self.not_included

        for i,v in dictionairy.items():
            if i in not_included: continue
        new_dict[i] = v

        return new_dict
    
    def get_current_time(self):
        t = time.localtime()








    
    



    
