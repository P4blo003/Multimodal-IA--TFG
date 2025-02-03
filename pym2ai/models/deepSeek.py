# Modulos
from pym2ai.exceptions import InvalidModelVersion
from .model import Model

# ----

# Versiones de Deepseek.
DS_R1_Distill_Qwen_1v5B = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
DS_R1_Distill_Qwen_7vB = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
DS_R1_Distill_Qwen_14vB = "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B"
DS_R1_Distill_Qwen_32vB = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"

DS_R1_Distill_LLama_8B = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
DS_R1_Distill_LLama_70B = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"

MODELS = {
    DS_R1_Distill_Qwen_1v5B, DS_R1_Distill_Qwen_7vB, DS_R1_Distill_Qwen_14vB,
    DS_R1_Distill_Qwen_32vB, DS_R1_Distill_LLama_8B, DS_R1_Distill_LLama_70B}
# ----

# Clases
class DeepSeek(Model):
    
    def __init__(self, modelVersion:str):
        
        if modelVersion not in MODELS:
            msg = f"Invalid model. Given: <{modelVersion}>.\nCurrent models:\n"
            for modelVersion in MODELS:
                msg += f"\t- {modelVersion}.\n"
            raise InvalidModelVersion(msg)
        
        super().__init__(modelVersion)
# ----