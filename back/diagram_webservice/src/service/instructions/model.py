class Model :
    def __init__(self, name, params):
        self.name = name
        self.params = params
    
    def as_json(self):
        return {"name": self.name, "params":self.params }