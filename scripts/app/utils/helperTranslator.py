import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv('/Users/vikramsingh/Documents/Projects/genAI/scripts/.env')
ky = os.getenv('KY')
genai.configure(api_key=ky)

lm = genai.GenerativeModel("gemini-1.5-flash")

def translateMessage(q):
    response = lm.generate_content(q)
    return response

a = translateMessage('Please translate this to english "Wat is hierdie taal"')
print(a)