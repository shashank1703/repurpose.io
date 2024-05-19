from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import openai

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

openai.api_key = "YOUR_OPENAI_API_KEY"

class PostData(BaseModel):
    url: str
    platform: str
    content: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/fetch")
async def fetch_content(url: str = Form(...)):
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text
        return {"content": content}
    except requests.RequestException as e:
        return {"error": str(e)}

@app.post("/generate")
async def generate_result(platform: str = Form(...), content: str = Form(...)):
    try:
        prompt = f"Create a {platform} post based on the following content:\n\n{content}"
        openai_response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        result_content = openai_response.choices[0].text.strip()
        return {"result_content": result_content}
    except Exception as e:
        return {"error": str(e)}

@app.post("/post")
async def post_to_social_media(platform: str = Form(...), content: str = Form(...)):
    # Placeholder function for posting to social media
    # Implement actual API calls for LinkedIn and Twitter
    return {"message": f"Content posted to {platform} successfully!"}
