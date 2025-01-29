# Modules
# -------


class Model:
    
    def __init__(self, modelVersion:str):
        self.modelVersion = modelVersion
        
    def __repr__(self):
        return f"Model: {self.modelVersion}"