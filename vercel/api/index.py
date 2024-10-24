from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_URL = os.getenv('API_URL', 'http://127.0.0.1:7860')

@app.get("/")
@app.post("/")
async def root(request: Request):
    return {
        "message": "Welcome to the Image Processing API.",
        "method": request.method,
        "instructions": "Use the /process-image/ endpoint with a POST request to process images."
    }

@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File uploaded is not an image")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{API_URL}/api/process",
                files={'file': (file.filename, await file.read(), file.content_type)},
                timeout=10
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"Error from Gradio API: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=500, detail="Failed to process image")
        except httpx.RequestError as e:
            print(f"Request to Gradio API failed: {e}")
            raise HTTPException(status_code=500, detail="Request to Gradio API failed")

    return response.json()

import uvicorn

if __name__ == "__main__":
    uvicorn.run("index:app", host="127.0.0.1", port=5000, reload=True)