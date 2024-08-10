from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import conditioning

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:5500'],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

class TextFromFront(BaseModel):
    text: str

@app.post('/ai/text')
async def text(text:TextFromFront):
    outcomes = conditioning.each_outcome(text.text)
    print(text.text)
    print(outcomes)
    return {"msg":outcomes}