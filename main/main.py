import requests
from dotenv import load_dotenv
from capture_save_and_post_img.capture_save_and_post_image import CameraHandler

from gradio_client import Client
import os

# Load environment variables from .env file such as the server API
load_dotenv()



if __name__ == "__main__":
    # Create a CameraHandler object
    camera_handler = CameraHandler()
    # Capture an image and send to server for processing
    response = camera_handler.capture_image()
    # Display the server response
    if response:
        print("Server response:")
        print(response)


url = "http://localhost:5000/api/generate"
data = {
    "model": "promptEng",
    "prompt": str(response["text"]) ,
    "stream": False
}

story = requests.post(url, json=data)


# Extract the JSON from the response
story_json = story.json()

# Now you can access the 'response' field
text = str(story_json["response"])
print(text)
client = Client("mrfakename/MeloTTS")
result = client.predict(
    "EN-US",  # Literal['EN-US', 'EN-BR', 'EN_INDIA', 'EN-AU', 'EN-Default'] in 'Speaker' Dropdown component
    text,  # str in 'Text to speak' Textbox component
    1,  # float (numeric value between 0.1 and 10.0) in 'Speed' Slider component
    "EN",  # Literal['EN', 'ES', 'FR', 'ZH', 'JP', 'KR'] in 'Language' Radio component
    api_name="/synthesize"
)



parts = result.split("\\") 

# Replace the last part with "audio.wav"
parts[-1] = "audio.wav"

# Join the parts back together to form the new result
new_result = "\\".join(parts)

# Rename the file
os.rename(result, new_result)

# Open the new file
os.startfile(new_result)

print(new_result, "This is the result ")

