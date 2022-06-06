from poc.classes.AuxSTInstance import AuxSTInstance
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTFunctionalTermInstance(AuxSTInstance):

    def __init__(self, i):
        super().__init__(i)
        self.def_type = AuxSymbolTable.functionalTermInstance
        self.zfrom = i.corrected_position('FunctionalTermHeader')
        self.zto = i.last_positions_by_rule['FunctionalTermInstance'].pos_to_str()
        self.keyword = ""

    def clone(self):
        new_class_instance = self._copy(AuxSTFunctionalTermInstance(self._i))
        new_class_instance.id = self.id
        new_class_instance.def_type = self.def_type
        new_class_instance.keyword = self.keyword
        new_class_instance.zfrom = self.zfrom
        new_class_instance.to = self.zto
        new_class_instance.mandatory = self.mandatory
        new_class_instance._is_inherited = True
        return new_class_instance

    def get_type_signature(self):
        type_child = AuxSymbolTable.get_child_by_outline(self, AuxSymbolTable.type)
        return type_child.id
