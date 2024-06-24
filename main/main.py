import os
import sys
import platform
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import glob 
app = FastAPI()

class ItemResponse(BaseModel):
    data: str

preprompt = """Write a short story, with a maximum of 750 words, about the production cycle of a specific product.
Start with the raw material extraction: discuss where the resources come from, which specific resources are used, and the working conditions of the laborers, including any environmental impacts.
When transitioning to the manufacturing part, begin with this sentence: "Once the raw materials have been extracted, they are transported to factories around the world for processing and assembly."
In the manufacturing part, explore the environmental burdens, working conditions, and process methods. Highlight differences between factories in various regions and how production conditions affect both people and the environment.
When transitioning to the transportation part, begin with this sentence: "With the product assembled, it now begins its journey to consumers across the globe."
In the transportation part, describe the transportation methods commonly used and their environmental impacts, including CO2 emissions and other ecological damages.
When transitioning to the end usage part, begin with this sentence: "After the product reaches the hands of consumers, its lifecycle continues through daily use until it reaches the end of its useful life."
In the end usage part, investigate the product’s lifespan, disposal, and recycling possibilities. Explain how some parts are incinerated or deposited, while others are recycled and transformed into new products. Discuss the environmental burden of disposal methods.
Please ensure smooth transitions and engage the consumer, incorporating them into the story to some extent.

"""

prompt = ""

# Determine the base path to the globus_repo directory
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the appropriate path to PYTHONPATH based on the OS
sys.path.append(base_path)

from capture_save_and_post_img.capture_save_and_post_image import CameraHandler
from gradio_client import Client

# Load environment variables from .env file such as the server API
load_dotenv()

@app.post("/api/placeitem", response_model=ItemResponse)
async def place_item():
    # Create a CameraHandler object
    camera_handler = CameraHandler()
    # Capture an image and send to server for processing
    response = camera_handler.capture_image()
    # Display the server response
    print(f"Server response (image recognition):\n{response}\n")
    print(response)
    return {"data": response["text"]}

@app.post("/api/itemanalyzed/{item}", response_model=ItemResponse)
async def item_analyzed(item: str):
    prompt = f"{preprompt} /n this is the product: {item}"

    url = "https://api.asgard.u7s.de/api/generate"
    data = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    
    story = requests.post(url, json=data)

    # Extract the JSON from the response
    story_json = story.json()
    print(f"Story as JSON:\n{story_json}\n")

    # Now you can access the 'response' field
    story_text = str(story_json["response"])
    print(f"Story as text:\n{story_text}\n")

    split_text =devide_text(story_text)
    print(len(split_text) )
    audioarray = [] 
    delete_existing() 
    for i in range(len(split_text)): 
        print("Loading New Text: ", "...") 

        client = Client("mrfakename/MeloTTS")
        result = client.predict(
                text=split_text[i],
                speaker="EN-BR",
                speed=0.8,
                language="EN",
                api_name="/synthesize"
        )
        print(f"\nAudio API response:\n{result}\n")

        audioarray.append(result)
        save_audio(result, i)   
    print("Audio Array: ", audioarray)
    return {"response" : "Audio is safed completly"}


    # Save the audio file and return the path
    # new_result = delte_and_save_audio(result) 

    # Open the new file
    #open_audio_file(new_result)

    # Print the path of the saved audio file
    # print("The audio file was saved to: \n", new_result)
    # return("The audio file was saved to: \n", new_result)

def devide_text(text : str ):
    new_text = text.strip().split('\n\n')


    
    return new_text

def open_audio_file(new_result : str ) :
    
    # Open the new file
    if platform.system() == 'Windows':
        os.startfile(new_result)
    else:
        os.system(f'open "{new_result}"')

    # Print the path of the saved audio file
    print("The audio file was saved to: \n", new_result)

def delete_existing():
    # Modify the path to save as audio.wav in the processing directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    processing_dir = os.path.join(script_dir, "../processing")
    os.makedirs(processing_dir, exist_ok=True)  # Ensure the directory exists
    
    # Find all .wav files in the processing directory
    wav_files = glob.glob(os.path.join(processing_dir, "*.wav"))
    
    # Delete each .wav file
    for wav_file in wav_files:
        os.remove(wav_file)
        print(f"Deleted: {wav_file}")


def save_audio(result : str, number : int ) : 
     # Modify the path to save as audio.wav in the processing directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    processing_dir = os.path.join(script_dir, "../processing")
    os.makedirs(processing_dir, exist_ok=True)  # Ensure the directory exists

    # Construct the full new path
    new_result = os.path.join(processing_dir, f"story{number}.wav")

    # Delete the existing file if it exists
    if os.path.exists(new_result):
        os.remove(new_result)

    # Rename the file to move it to the new directory
    os.rename(result, new_result)

    return new_result


def delte_and_save_audio(result : str ) : 
    # Modify the path to save as audio.wav in the processing directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    processing_dir = os.path.join(script_dir, "../processing")
    os.makedirs(processing_dir, exist_ok=True)  # Ensure the directory exists

    # Construct the full new path
    new_result = os.path.join(processing_dir, "story.wav")

    # Delete the existing file if it exists
    if os.path.exists(new_result):
        os.remove(new_result)

    # Rename the file to move it to the new directory
    os.rename(result, new_result)

    return new_result

    





@app.delete("/stopProcess") 
def stopprocess():
    # Kill all backend processes including the server itself
    os.system("pkill -f 'uvicorn'")
    os.system("pkill -f 'capture_save_and_post_image.py'")

    #Hier noch Befehl um Audio zu stoppen 
    
    # Restart the server
    os.system("nohup uvicorn main:app --host 0.0.0.0 --port 4000 &")
    
    return "Backend processes stopped and server restarted"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4000)
