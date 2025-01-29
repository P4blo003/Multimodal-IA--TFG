# Modules
import torch
from prettytable import PrettyTable
# -------


class Model:
    
    def __init__(self, modelVersion:str):
        self.modelVersion = modelVersion
        
    def __repr__(self):
        return f"Model: {self.modelVersion}"     

    @property
    def model_version(self):
        return self.modelVersion