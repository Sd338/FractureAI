from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File
import time
from backend.app.core.api_manager import APIManager
from backend.app.core.helpers import handle_image_upload
import cv2
import numpy as np
import io
from fastapi.responses import StreamingResponse

router = APIRouter()
api_manager = APIManager()
app = FastAPI()

# Add a simple root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FractureAI API!"}

# Rate limits for llama-3.2-11b-text-preview model
REQUESTS_PER_MINUTE = 30
REQUESTS_PER_DAY = 7000

# Request counters for rate limiting
request_counter = {
    'minute': 0,
    'day': 0,
    'start_time': time.time(),
    'start_day': time.time()
}

def reset_request_counters():
    """Reset the request counters based on time elapsed."""
    current_time = time.time()
    
    # Reset minute counter
    if current_time - request_counter['start_time'] >= 60:
        request_counter['minute'] = 0
        request_counter['start_time'] = current_time

    # Reset day counter
    if current_time - request_counter['start_day'] >= 86400:  # 86400 seconds in a day
        request_counter['day'] = 0
        request_counter['start_day'] = current_time

def check_rate_limit():
    """Check if the rate limit has been exceeded."""
    reset_request_counters()  # Reset counters if necessary

    if request_counter['minute'] >= REQUESTS_PER_MINUTE:
        raise HTTPException(status_code=429, detail="Rate limit exceeded for this minute.")
    if request_counter['day'] >= REQUESTS_PER_DAY:
        raise HTTPException(status_code=429, detail="Rate limit exceeded for this day.")

    # Increment the request counters
    request_counter['minute'] += 1
    request_counter['day'] += 1

@router.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """Endpoint to upload an image for processing."""
    check_rate_limit()  # Check rate limits before processing

    try:
        # Handle the image upload and process it
        result, annotated_image = await handle_image_upload(file)

        # Convert the annotated image to bytes
        _, buffer = cv2.imencode('.png', annotated_image)
        image_stream = io.BytesIO(buffer)

        return StreamingResponse(image_stream, media_type="image/png", headers={"Content-Disposition": "attachment; filename=annotated_image.png"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Register the router
app.include_router(router)
