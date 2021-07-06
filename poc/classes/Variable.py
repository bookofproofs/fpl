class Variable(dict):

    def __init__(self, var_name: str):
        super().__init__()
        self["name"] = var_name

    def set_value(self, value):
        self["value"] = value

    def set_fpl_type(self, fpl_type):
        self["fpl_type"] = fpl_type

    def set_user_type(self, user_type):
        self["user_type"] = user_type

    def get_fpl_type(self, fpl_type):
        return self["fpl_type"]

    def get_user_type(self, user_type):
        return self["user_type"]

    @staticmethod
    def register_in_block(self, block):
        if not type(block) is str:
            raise TypeError("block must be a Block, was " + str(block))
        block.register_identifier(block)
