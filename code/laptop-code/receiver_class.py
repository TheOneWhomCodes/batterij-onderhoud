
from DB import Database


import time



class Receiver:



    def __init__(self):

        self.DB = Database()

        self.not_included = ["_id"] #voor de copy_dict functie, we mogen geen _id veranderen op mongoDB

    
    def decide_group_tag(self,tag_id,show_type=False):

        if not isinstance(tag_id,int):
            print(f"ERROR: not given an integer tag id:{tag_id}")
            return

        group = None
        type = None
        if tag_id <= 586 and tag_id >= 200:
            group = "batterijen"
            type = "batterij"
        elif tag_id < 200 and tag_id >= 0:
            group = "locaties/autos"

            if tag_id < 99:
                type = "locatie"
            else:
                type = "kart"

        return group,type
    

    
    def update_all_collections(self,tag_id):

        
        database = self.DB

        apriltag_document = self.get_apriltag(tag_id)

        database.update_document({"tagId":tag_id},{"active":True})

        fields = ["tagId","validTo"]
        values = [tag_id,"/"]
        assignment_document = self.get_tag_assignment_multiple_fields(fields,values)


        group,type = self.decide_group_tag(tag_id)

        
        collection_name = group.upper()


        UID = assignment_document["assignedId"]
        database.connect_to_collection(collection_name)
        

        group_document = self.get_specific_group_document(group,type,assignment_document,UID)
        #stel dat hij nie besta, wordt hij dan gemaakt

       
        return True
    
    def save_adc_data(self,raw_data,estimation,tag_bat,tag_locatie_auto,user):

        database = self.DB

        current_time = self.get_current_time()


        database.connect_to_collection("TAG_ASSIGNMENTS")
        
        
        assignment_document = database.retrieve_document("tagId",tag_bat)

        if assignment_document is None:
            print(f"ERROR: assignedment document van tagid:{tag_bat} is NONE")

        
        batUID = assignment_document["assignedId"]

        
        assignment_document = database.retrieve_document("tagId",tag_locatie_auto)
        
        if assignment_document is None:
            print(f"ERROR: assignedment document van tagid:{tag_locatie_auto} is NONE")

        name = assignment_document["assignedId"]


        print(assignment_document)

        database.connect_to_collection("MEETDATA_STATISCH")

        data_to_string = str(raw_data)

        meting_document = {"batUID":batUID,"timestamp":current_time,"rawData":data_to_string,"estimation":estimation,"user":user,"autoUID":name,"comment":"/"}

        database.insert_document(meting_document)


        
    def get_apriltag(self,tag_id,insertable=True):

        database = self.DB

        database.connect_to_collection("APRILTAGS")

        found_document = database.retrieve_document("tagId",tag_id)

        group,type = self.decide_group_tag(tag_id)

        if found_document is None:
            if insertable:
                new_april_document = {"tagId":tag_id,"assignmentType":type,"active":True}
                database.insert_document(new_april_document)
                found_document = new_april_document
        
        return found_document
    
    
    def get_tag_assignment(self,tag_id,assignedId="/"):

        database = self.DB

        database.connect_to_collection("TAG_ASSIGNMENTS")

        found_document = database.retrieve_document("tagId",tag_id)

        group,type = self.decide_group_tag(tag_id)
        current_time = self.get_current_time()

        if found_document is None:
            new_assignment_document = {"tagId":tag_id,"validFrom":current_time,"validTo":"/","type":type,"assignedId":assignedId}
            database.insert_document(new_assignment_document)
            found_document = new_assignment_document

        
        return found_document
    
    def get_tag_assignment_multiple_fields(self,fields,values,insertable=True,assignedId="/"):

        database = self.DB

        current_time = self.get_current_time()

        database.connect_to_collection("TAG_ASSIGNMENTS")

        length_fields = len(fields)
        length_values = len(values)
        if length_fields != length_values:
            print(f"ERROR: Not an even number of fields/values given! Fields:{fields}, Values:{values}")
            return None
        
        data_to_match = {}
        for i in range(length_fields):
            field = fields[i]
            value = values[i]
            data_to_match[field] = value
            
        found_document = database.retrieve_document_multiple_fields(data_to_match)

        
        if found_document is None:
            if insertable:
                tag_id = values[0]

                group,type = self.decide_group_tag(tag_id)

                new_assignment_document = {"tagId":tag_id,"validFrom":current_time,"validTo":"/","type":type,"assignedId":assignedId}
                database.insert_document(new_assignment_document)
                found_document = new_assignment_document            



        return found_document


    
    def get_specific_group_document(self,group,type,assignment_document,name_uid="/",comment="/"):

        database = self.DB

        UID = assignment_document["assignedId"]

        collection_name = group.upper()


        database.connect_to_collection(collection_name)

        UID_field_name = "batUID"
        if group == "locaties/autos":
            UID_field_name = "name"

        if UID_field_name == "batUID":
            data_to_find = {"batUID":UID,"retiredAt":"/"}
            group_document = database.retrieve_document_multiple_fields(data_to_find)
            
        else:
            group_document = database.retrieve_document(UID_field_name,UID)

        print(UID)
        if group_document is None:
            current_time = self.get_current_time()

            if group == "batterijen":
                new_bat_document = {"createdAt":current_time,"retiredAt":"/","batUID":name_uid,"comment":comment}
                database.insert_document(new_bat_document)
                group_document = new_bat_document
            else:
                new_loc_auto_document = {"type":type,"name":name_uid,"comment":comment}
                database.insert_document(new_loc_auto_document)
                group_document = new_loc_auto_document

        
        return group_document
    
    def retire_battery(self,bat_id,comment):

        database = self.DB

        current_time = self.get_current_time()



        group, type = self.decide_group_tag(bat_id)

        if group != "batterijen":
            print(f"ERROR: Trying to retire a battery with tag id:{bat_id} in group:{group} with type:{type}")
            return False
        
        apriltag_document = self.get_apriltag(bat_id,insertable=False)

        if apriltag_document is None:
            print(f"ERROR: Trying to retrieve the ID:{bat_id} in apriltag collection but it failed.")
            return
        
        database.update_document({"tagId":bat_id},{"active":False})

        fields = ["tagId","validTo"]
        values = [bat_id,"/"]

        assignment_document = self.get_tag_assignment_multiple_fields(fields=fields,values=values)

        copied_document = self.copy_dict(assignment_document)

        UID = assignment_document["assignedId"]

        copied_document["validTo"] = current_time

        database.update_document(assignment_document,copied_document)

        collection_name = group.upper()

        database.connect_to_collection(collection_name)


        data_to_find = {"batUID":UID,"validTo":"/"}
        battery_document = database.retrieve_document_multiple_fields(data_to_find)

        copied_battery_document = self.copy_dict(battery_document)
        copied_battery_document["validTo"] = current_time

        database.update_document(battery_document,copied_battery_document)










        

        
        





    
    
    










        
        

        



    
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

        day = t.tm_mday
        month = t.tm_mon
        year = t.tm_year

        hour = t.tm_hour

        if hour < 10:
            hour = f"0{hour}"

        min = t.tm_min

        if min < 10:
            min = f"0{min}"

        time_string = f"{day}-{month}-{year}, {hour}:{min}"

        return time_string
        

