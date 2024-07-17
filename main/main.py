import os
import sys
import platform
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import glob 
import socket
app = FastAPI()


class ItemResponse(BaseModel):
    data: str

preprompt = """
    Use a maximum of 50 words.
    No summary, no headlines, no introduction. 
    End every sentence befor a line break with multiple dots ".......". 
    Write an emotional short story about the lifecycle of the following product including these factors.
    Handle the ressources needed and tell how those are most likley won.
    Tell about the production of the product, where was it and how was it produced?
    Then talk about how the product reaches munich in germany, how does it get here is that sustainable?
    Finaly discuss how the products life ends. Is it just thrown away are there smart ways to recycle it?
"""

prompt = ""

# Determine the base path to the globus_repo directory
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"Base path determined: {base_path}\n")

# Add the appropriate path to PYTHONPATH based on the OS
sys.path.append(base_path)
print(f"Added {base_path} to PYTHONPATH\n")

from capture_save_and_post_img.capture_save_and_post_image import CameraHandler
from gradio_client import Client

# Load environment variables from .env file such as the server API
load_dotenv()
print("Environment variables loaded from .env file\n")
print("Loading Camera Handler" )
camera_handler = CameraHandler()

@app.post("/api/placeitem", response_model=ItemResponse)
async def place_item():
    print("Endpoint /api/placeitem called\n")
    # Create a CameraHandler object
    print("CameraHandler object created\n")
   
    
    # Capture an image and send to server for processing
    response = camera_handler.capture_image()
    print(f"Server response (image recognition): {response}\n")
    return {"data": response["text"]}

@app.post("/api/itemanalyzed/{item}", response_model=ItemResponse)
async def item_analyzed(item: str):
    # BG Music 
    playBackgroundMusic(r"C:\Users\Admin\Documents\Team-Globus\main\bgm.mp3")
    #Onboarding starten: 
    onboarding(r"C:\Users\Admin\Documents\Team-Globus\main\onboarding.wav")


    print(f"Endpoint /api/itemanalyzed/{item} called\n")
    prompt = f"{preprompt} /n this is the product: {item}"
    print(f"Prompt created: {prompt}\n")

    url = "https://api.asgard.u7s.de/api/generate"
    data = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    
    story = requests.post(url, json=data)
    print("Request to story generation API sent\n")

    # Extract the JSON from the response
    story_json = story.json()
    print(f"Story as JSON: {story_json}\n")

    # Now you can access the 'response' field
    story_text = str(story_json["response"])
    print(f"Story as text: {story_text}\n")

    split_text = devide_text(story_text)
    print(f"Text divided into {len(split_text)} parts\n")

    #BG Music 


    audioarray = [] 
    #delete_existing() 
    for i in range(len(split_text)): 
        print(f"Loading New Text part {i}: {split_text[i]}\n")
        paragraph = split_text[i] + "........."
        client = Client("mrfakename/MeloTTS")
        result = client.predict(
                text=paragraph,
                speaker="EN-Default",
                speed=0.9,
                language="EN",
                api_name="/synthesize"
        )
        print(f"Audio API response for part {i}: {result}\n")

        audioarray.append(result)
        save_audio(result, i)   
    print("Audio Array: ", audioarray, "\n")
    return {"response": "Audio is saved completely\n"}

def devide_text(text: str):
    tooshort = ""
    new_text = text.strip().split('\n\n')
    finaltext = [] 

    for p in new_text:
        tooshort += p

        if len(tooshort.split() ) > 10:
            finaltext.append(tooshort)
            tooshort = ""
    finaltext.append(tooshort)
    print(finaltext)
    return finaltext

def open_audio_file(new_result: str):
    print(f"Opening audio file: {new_result}\n")
    if platform.system() == 'Windows':
        os.startfile(new_result)
    else:
        os.system(f'open "{new_result}"')
    print("Audio file opened\n")

def delete_existing():
    print("Deleting existing audio files\n")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    processing_dir = os.path.join(script_dir, "../processing/data")
    os.makedirs(processing_dir, exist_ok=True)
    
    wav_files = glob.glob(os.path.join(processing_dir, "*.wav"))
    
    for wav_file in wav_files:
        os.remove(wav_file)
        print(f"Deleted: {wav_file}")

def save_audio(result: str, number: int):
    number = number + 1 
    print(f"Saving audio file part {number}\n")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    processing_dir = os.path.join(script_dir, "../processing/data")
    os.makedirs(processing_dir, exist_ok=True)

    new_result = os.path.join(processing_dir, f"story{number}.wav")

    if os.path.exists(new_result):
        os.remove(new_result)

    os.rename(result, new_result)
    print(f"Saved audio part {number} as: {new_result}\n")

    return new_result

def delte_and_save_audio(result: str):
    print("Saving audio file\n")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    processing_dir = os.path.join(script_dir, "../processing")
    os.makedirs(processing_dir, exist_ok=True)

    new_result = os.path.join(processing_dir, "story.wav")

    if os.path.exists(new_result):
        os.remove(new_result)

    os.rename(result, new_result)
    print(f"Audio file saved as: {new_result}\n")

    return new_result

@app.delete("/stopProcess") 
def stopprocess():

    send_value("false")

    print("Endpoint /stopProcess called\n")
    # Kill all backend processes including the server itself
    os.system("pkill -f 'uvisscorn'")
    os.system("pkill -f 'capture_save_and_post_image.py'")
    print("Killed all backend processes\n")

    # Hier noch Befehl um Audio zu stoppen 
    
    # Restart the server
    os.system("nohup uvicorn main:app --host 0.0.0.0 --port 4000 &")
    print("Server restarted\n")
    
    return {"data": "Process stopped"}

def send_value(value, host='localhost', port=56789):
    print("send_value was trigged with ", value)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(value.encode())
    except Exception as e:
        print(f"An error occurred: {e}")

import os
import platform


def playBackgroundMusic(file_path: str):
    if platform.system() == "Windows":
        os.system(f'start {file_path}')
    elif platform.system() == "Darwin":  # macOS
        os.system(f'open {file_path}')
    elif platform.system() == "Linux":
        os.system(f'xdg-open {file_path}')
    else:
        print("Unsupported OS")

import shutil

def onboarding(result: str):
    print(f"Saving audio file {result}\n")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    processing_dir = os.path.join(script_dir, "../processing/data")
    os.makedirs(processing_dir, exist_ok=True)

    new_result = os.path.join(processing_dir, "story0.wav")

    if os.path.exists(new_result):
        os.remove(new_result)

    shutil.copy2(result, new_result)
    print(f"Saved audio file as: {new_result}\n")

    return new_result

if __name__ == "__main__":
    print("Starting server\n")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4000)
    print("Server started\n")
