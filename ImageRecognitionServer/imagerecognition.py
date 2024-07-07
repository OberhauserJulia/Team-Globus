from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import uvicorn
import base64
import io

print("ModelBackend is starting\n")
app = FastAPI()

# Load the Hugging Face model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

class ImageData(BaseModel):
    base64_image: str

@app.post("/predict/")
async def predict(image_data: ImageData):
    print("Request entered\n")
    try:
        # Decode the base64 string
        image_bytes = base64.b64decode(image_data.base64_image)
        image = Image.open(io.BytesIO(image_bytes))
        print("Image decoded and loaded\n")

        # Preprocess the image
        inputs = processor(images=image, return_tensors="pt")
        print("Image preprocessed\n")
        
        # Generate text
        outputs = model.generate(**inputs)
        text = processor.decode(outputs[0], skip_special_tokens=True)
        print(f"Generated text: {text}\n")
        return {"text": text}

    except Exception as e:
        print(f"Error: {str(e)}\n")
        raise HTTPException(status_code=400, detail=str(e))

print("Starting server\n")
uvicorn.run(app, host="0.0.0.0", port=4455)
print("Server started\n")
