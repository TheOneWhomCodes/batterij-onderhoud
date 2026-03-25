

from pymongo import MongoClient
#from bson import ObjectId


#import json


#------------------------------------------------------------------- MONGODB SETUP
connection_string = "mongodb://admin:2560K3ss3l@89.167.92.181:27017/?authSource=admin"

NAME_MAIN_DATABASE = "collected_data"

mongo_client = MongoClient(connection_string)
main_database = mongo_client[NAME_MAIN_DATABASE]



class Database:
    
    def __init__(self,main_database=main_database,client=mongo_client,connection_string=connection_string):
        
        self.main_database = main_database
        self.client = client
        self.connection_string = connection_string
        
        self.current_collection = None
        
        self.cached_collections = None
        
    def connect_to_collection(self,name_collection):
        main_db = self.main_database
        
        if self.cached_collections is None:
            self.cached_collections = main_db.list_collection_names()
        

        list_collection_names = self.cached_collections
        if not name_collection in list_collection_names:
            print(f"ERROR: Collection named {name_collection} does not exist!")
            return False #tonen aan dat het faalde
        
        self.current_collection = main_db[name_collection]
        return True #tonen aan dat de connectie werkte
        
    def retrieve_document(self,field,value):
        data_to_find = {field:value}
        
        connected_collection = self.current_collection
        
        if connected_collection == None:
            print("ERROR: you're not connected to a collection yet!")
            return None
        
        found_document = connected_collection.find_one(data_to_find)
        
        if found_document == None:
            print(f"Could not find data: {data_to_find} in collection {connected_collection.name}")
            return None
        
        return found_document
    def retrieve_document_multiple_fields(self,data_to_find):

        connected_collection = self.current_collection
        
        if connected_collection == None:
            print("ERROR: you're not connected to a collection yet!")
            return None
        
        found_document = connected_collection.find_one(data_to_find)
        
        if found_document == None:
            print(f"Could not find data: {data_to_find} in collection {connected_collection.name}")
            return None
        
        return found_document
    
    def insert_document(self,data):
        
        valid_dictionairy_check = isinstance(data,dict)
        
        #-------------------------------------------------------------------------------- safety checks
        if not valid_dictionairy_check:
            print(f"ERROR: trying to insert data: {data} that isn't a dictionairy")
            return None
        
        #--------------------------------------------------------------------------------
        connected_collection = self.current_collection
        
        if connected_collection == None:
            print("ERROR: you're not connected to a collection yet!")
            return None
        #--------------------------------------------------------------------------------
        
        result = connected_collection.insert_one(data)
        
        return result
    
    def update_document(self,data_to_match,data_to_update,mongodb_operator="$set"):
        
        valid_match_data_check = isinstance(data_to_match,dict)
        valid_update_data_check = isinstance(data_to_update,dict)
        
        #-------------------------------------------------------------------------------- safety checks
        if not valid_match_data_check or not valid_update_data_check:
            print(f"ERROR: check if you passed dictionairies: match_data:{data_to_match}, update_data:{data_to_update}")
            return None
        #--------------------------------------------------------------------------------
        connected_collection = self.current_collection
        
        if connected_collection == None:
            print("ERROR: you're not connected to a collection yet!")
            return None
        #--------------------------------------------------------------------------------
        
        if "_id" in data_to_update:
            print("ERROR: can't change an immutable id")
            return None
        #--------------------------------------------------------------------------------

        operation = connected_collection.update_one(data_to_match,{mongodb_operator:data_to_update})
        #mongodb_operator is een operator ingebouwd in mongodb die ik mee geef om te zeggen dat ik nu een document
        #overwriten, namelijk het document die matched met data_to_match
        
        raw_result = operation.raw_result #we krijgen de rauwe gegevens van wat mongoDB heeft uitgevoerd
        
        result_update = raw_result["updatedExisting"] #we checken als het updaten een success was
        
        if result_update == False:
            print(f"ERROR: kon niet updaten, check als je parameters goed zitten: data_to_match:{data_to_match}, data_to_update:{data_to_update}")
        
        return result_update
    
    def remove_document(self,field,value):
        
        data_match = {field:value}
        #--------------------------------------------------------------------------------
        connected_collection = self.current_collection
        
        if connected_collection == None:
            print("ERROR: you're not connected to a collection yet!")
            return None
        #--------------------------------------------------------------------------------
        
        
        operation = connected_collection.delete_one(data_match)
        raw_result = operation.raw_result
        
        result = raw_result["n"]
        
        if result == 0:
            result = False
        else:
            result = True
    
        return result
    
    def refresh_cached_collections(self):
        
        main_db = self.main_database
        
        self.cached_collections = main_db.list_collection_names()
        

        
        
        
        
        
        
        
        
    