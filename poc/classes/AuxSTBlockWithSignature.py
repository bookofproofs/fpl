from poc.classes.AuxST import AuxSTBlock


class AuxSTBlockWithSignature(AuxSTBlock):
    def __init__(self, property_type: str, i):
        super().__init__(property_type, i)
        # If the signature of the block has no parameters at all, the constant value
        # will be set after the evaluate method of the block will be called the very first time.
        # This is to prevent the block being re-evaluated each time whenever it is referred to in the FPL code.
        # The evaluate method will check if the static value is not None and simply return its value
        self._constant_value = None

    def constant_value(self):
        return self._constant_value

    def set_constant_value(self, value):
        if self._constant_value is None:
            self._constant_value = value
        else:
            raise AssertionError("Constant value already set.")


