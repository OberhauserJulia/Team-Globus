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

preprompt = """Write a really, really short story, with a maximum of 50 words, about the production cycle of a specific product. 
Start with the raw material extraction: discuss where the resources come from, which specific resources are used, and the working conditions of the laborers. 
When transitioning to the manufacturing part, begin with this sentence: 
"Once the Raw materials extracted, they are shipped to factories globally for processing."  
In the manufacturing part, explore the environmental burdens, working conditions, and process methods. 
Also tell how production conditions affect both people and the environment.  
When transitioning to the transportation part, begin with this sentence: 
"With the product assembled, it now travels to consumers worldwide."  
In the transportation part, 
describe the transportation methods commonly used and their environmental impacts, 
including CO2 emissions and other ecological damages.  
When transitioning to the end usage part, begin with this sentence: 
"After reaching consumers, its lifecycle continues until it ends.” 
Explain how some parts are incinerated or deposited, while others are recycled and transformed into new products. 
Discuss the environmental burden of disposal methods.
Please ensure smooth transitions and engage the consumer, incorporating them into the story to some extent.

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
    
    return "Backend processes stopped and server restarted"

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
