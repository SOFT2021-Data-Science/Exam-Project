input_enums = ["any_number", "enum", "range"]


class Param:
    def __init__(self, values, input_type):

        if input_type not in input_enums:
            raise Exception("Invalid enum in param. Must be one of: ", input_enums)

        self.values = values
        self.input_type = input_type

    def as_json(self):
        return {"values": self.values, "input_type": self.input_type}
