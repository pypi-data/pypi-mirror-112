import os
import json


class dynamicWorld():
    """
        Represents all dynamic objects in a dataset

        
    """
    def __init__(self, path2JSON):
        """
            Loads the dataset

            :param dataSetFolderPath: Path to a folder containing a valid automatum.data dataset.
        """        
        if(not os.path.isfile(path2JSON)):
            raise FileNotFoundError("The dynamic world json couldn't be found - Path: %s"%path2JSON)

        with open(path2JSON) as f:
            dynamicWorldData = json.load(f) 

        self.UUID = dynamicWorldData["UUID"]

        self.frame_count = dynamicWorldData["videoInfo"]["frame_count"]
        self.fps = dynamicWorldData["videoInfo"]["fps"]
        self.delta_t = 1/self.fps
        self.environmental = dynamicWorldData["EnvironmentInfo"]
        self.utm_referene_point = dynamicWorldData["UTM-ReferencePoint"]
        self.dynamicObjects =  dict()
        self.maxTime  = 0
        for dynObjData in dynamicWorldData["objects"]:
            dynObj = dynamicObject.dynamic_object_factory(dynObjData, self.delta_t)
            self.dynamicObjects[dynObjData["UUID"]] = dynObj
            self.maxTime = max(self.maxTime, dynObj.get_last_time())


    def get_length_of_dataset_in_seconds(self):
        return self.maxTime 

    def __len__(self):
        """
            Overwrite the length operator 
        """
        return len(self.dynamicObjects)

    def __str__(self):
        """
            Overwrite the string Method
        """
        dataSetString = "Dataset %s consits of the %d objects:\n"%(self.UUID, len(self))
        for dynObj in self.dynamicObjects.values():
            dataSetString += "'--> %s [%s] with %d entries from %0.2f s to %0.2f s\n"%(str(type(dynObj)), dynObj.UUID, len(dynObj), dynObj.get_first_time(), dynObj.get_last_time())

        return dataSetString

    def get_dynObj_by_UUID(self, UUID):
        """
            Returns the dynamic object with the given UUID string. 
            If no object is found, None is returned. 
        """
        if(UUID in self.dynamicObjects):
            return self.dynamicObjects[UUID]
        else:
            return None

    def get_list_of_dynamic_objects(self):
        """
            Returns the list of dynamic objects.
        """
        return list(self.dynamicObjects.values())

    def get_list_of_dynamic_objects_for_specific_time(self, time):
        """
            Returns the list of dynamic objects that are visitable at the given time.
        """
        objList = list()
        for obj in self.dynamicObjects.values():
            if(obj.is_visible_at(time)):
                objList.append(obj)
        return objList
               

class dynamicObject():
    """
        Base Class for all dynmaic objects
    """
    def __init__(self, movement_dynamic, delta_t):
        self.x_vec = movement_dynamic["x_vec"]
        self.y_vec = movement_dynamic["y_vec"]
        self.vx_vec = movement_dynamic["vx_vec"]
        self.vy_vec = movement_dynamic["vy_vec"]
        self.psi_vec = movement_dynamic["psi_vec"]
        self.ax_vec = movement_dynamic["ax_vec"]
        self.ay_vec = movement_dynamic["ay_vec"]
        self.length = movement_dynamic["length"]
        self.width = movement_dynamic["width"]
        self.time = movement_dynamic["time"]
        self.UUID = movement_dynamic["UUID"]
        self.delta_t = delta_t
        
    def __len__(self):
        """
            Overwrite the length operator 
        """
        return len(self.x_vec)

    def get_first_time(self):
        """
            Returns the time the object occurs the first time
        """
        return self.time[0]

    def get_last_time(self):
        """
            Returns the time the object occurs the last time
        """
        return self.time[-1]

    def is_visible_at(self, time):
        """
            Checks if the object is visible at the given time
        """
        return (time > self.get_first_time() and time < self.get_last_time())

    def next_index_of_specific_time(self, time):
        """
            Returns the index that is next to the given time. 
            If the object is not visible in that time step. 
            The function returns None.
        """
        if(not self.is_visible_at(time)):
            return None
        return max(0,min(len(self),round((time - self.get_first_time())/self.delta_t)))



    @staticmethod
    def dynamic_object_factory(obj_data_dict, delta_t):
        """
            Object factory to decode the objects that are 
            specified in the json right into the corresponding objects.
        """
        obj_factory_dict = {
            "car":carObject,
            "van":carObject,
            "truck":truckObject,
            "carWithTrailer":carWithTrailerObject,
            "motorcycle":motorcycleObject
        }
        return obj_factory_dict[obj_data_dict["objType"]](obj_data_dict, delta_t)


class carObject(dynamicObject):
    """
        Class for representing a car object
    """
    
    def __init__(self, movement_dynamic, delta_t):
        dynamicObject.__init__(self, movement_dynamic, delta_t)
        

class truckObject(dynamicObject):
    """
        Class for representing a track object
    """
    def __init__(self, movement_dynamic, delta_t):
        dynamicObject.__init__(self, movement_dynamic, delta_t)
        

class carWithTrailerObject(dynamicObject):
    """
        Class for representing a trailer object
    """
    def __init__(self, movement_dynamic, delta_t):
        dynamicObject.__init__(self, movement_dynamic, delta_t)
        

class motorcycleObject(dynamicObject):
    """
        Class for representing a trailer object
    """
    def __init__(self, movement_dynamic, delta_t):
        dynamicObject.__init__(self, movement_dynamic, delta_t)
            