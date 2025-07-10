from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.chat import ChatPromptTemplate
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from pathlib import Path


# Get the current directory
current_dir = Path(__file__).parent

load_dotenv()
app = FastAPI()

# Serve static files (HTML/CSS/JS)
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class TranslationRequest(BaseModel):
    text: str
    input_language: str
    output_language: str
    tone: str

@app.post("/translate")
async def translate(request: TranslationRequest):
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")
        
        chat_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)
        
        system_template = """You are a helpful assistant that translates {input_language} to {output_language} in a {tone} tone.
                            Only output one answer. Don't provide an explanation or any additional information."""
        human_template = "{text}"
        
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("human", human_template),
        ])
        
        messages = chat_prompt.format_messages(
            input_language=request.input_language,
            output_language=request.output_language,
            tone=request.tone,
            text=request.text
        )
        
        result = chat_model.invoke(messages)
        return {"translation": result.content}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})