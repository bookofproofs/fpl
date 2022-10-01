from gid import Guid
from poc.classes.AuxSTBuildingBlockInstanceHandler import AuxSTBuildingBlockInstanceHandler

"""
The class AuxSTBuildingBlockInstanceHandlers provides a storage for building block instances separately from each other
during the evaluation process of their building blocks 'called' or 'referred to' somewhere in the FPL code. 
Each instance gets identified by a Guid and stores internally a AuxInstanceHandler object.
"""


class AuxSTBuildingBlockInstanceHandlers(dict):
    def __init__(self):
        super().__init__()
        # the main instance is the first instance ever created
        self.main_instance = self.add_instance()

    def add_instance(self):
        guid = Guid()
        guid_str = str(guid)
        self[guid_str] = AuxSTBuildingBlockInstanceHandler(guid_str)
        return self[guid_str]
