# analyzer/utils.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("3ZW726RSIvFfCPG3dzvXS0NSsF2dQDcezuzY2BLmPy2I1aWII3blJQQJ99BDACYeBjFXJ3w3AAALACOGsu1H")

def generate_embedding(text):
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response["data"][0]["embedding"]
