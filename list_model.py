from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

models = client.models.list()

print("\nAvailable Groq Models:\n")

# models.data is a list of Model objects
for model in models.data:
    print(model.id)
