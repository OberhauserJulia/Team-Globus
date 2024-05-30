# File: main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import uvicorn
import base64
import io

app = FastAPI()

# Load the Hugging Face model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

class ImageData(BaseModel):
    base64_image: str

@app.post("/predict/")
async def predict(image_data: ImageData):
    print("request eneterd")
    try:
        
        # Decode the base64 string
        image_bytes = base64.b64decode(image_data.base64_image)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Preprocess the image
        inputs = processor(images=image, return_tensors="pt")
        
        # Generate text
        outputs = model.generate(**inputs)
        text = processor.decode(outputs[0], skip_special_tokens=True)

        return {"text": text}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


uvicorn.run(app, host="0.0.0.0", port=4455)
