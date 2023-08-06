
from openautomatumdronedata.dynamicWorld import *
from openautomatumdronedata.staticWorld import *
import os 


class droneDataset():
    """
        Represents a full automatum data dataset


        :param dataSetFolderPath: Path to a folder containing a valid automatum.data dataset.
    """


    def __init__(self, dataSetFolderPath):
        """
        Creating a automatum drone dataset object, to access the utility functions.

        """
        self.dynWorld = dynamicWorld(os.path.join(dataSetFolderPath, "dynamicWorld.json"))
        self.statWorld = xodrStaticWorld((os.path.join(dataSetFolderPath, "staticWorld.xodr")))
        


