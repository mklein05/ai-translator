from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

chat_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)

result = chat_model.predict("Explain the history of Latvia")
print(result)