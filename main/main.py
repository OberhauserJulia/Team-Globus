import os
import sys
import platform
import requests
from dotenv import load_dotenv

# Determine the base path to the globus_repo directory
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the appropriate path to PYTHONPATH based on the OS
sys.path.append(base_path)

from capture_save_and_post_img.capture_save_and_post_image import CameraHandler
from gradio_client import Client

# Load environment variables from .env file such as the server API
load_dotenv()

preprompt = """Write a short story, with a maximum of 750 words, about the production cycle of a specific product. Dive into the world of raw material extraction and learn about the challenges and impacts on the environment and the working conditions of the laborers, as well as the resources required and where they can be found.
Moving on to the manufacturing of the product, explore the differences between factories in various regions and how the production conditions affect both people and the environment and please tell more about the conditions under that the workers go through and how it affects them mentally if there is something to tell about it. Also, delve into the countries where this product is manufactured and discuss the working conditions.
During the transportation of the product, discover how they are transported and explore the environmental impacts, including CO2 emissions and other ecological damages.
Lastly, in the end cycle, investigate the possibilities of disposal or recycling of the product. Learn about how some parts are incinerated or deposited, while others are recycled and transformed into new products. Conclude the story by reiterating that this is the complete cycle.
Please ensure smooth transitions and engage the consumer, incorporating them into the story to some extent."""

if __name__ == "__main__":
    # Create a CameraHandler object
    camera_handler = CameraHandler()
    # Capture an image and send to server for processing
    response = camera_handler.capture_image()
    # Display the server response
    print("Server response:")
    print(response)

    prompt = f"{preprompt} /n this is the product:{str(response['text'])} "

    url = "https://api.asgard.u7s.de/api/generate"
    data = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    
    story = requests.post(url, json=data)

    # Extract the JSON from the response
    story_json = story.json()
    print(story_json)

    # Now you can access the 'response' field
    story_text = str(story_json["response"])
    print(story_text)

    client = Client("mrfakename/MeloTTS")
    result = client.predict(
            text=story_text,
            speaker="EN-US",
            speed=1,
            language="EN",
            api_name="/synthesize"
    )
    print(result)

    # Modify the path to save as audio.wav in the processing directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    processing_dir = os.path.join(script_dir, "../processing")
    os.makedirs(processing_dir, exist_ok=True)  # Ensure the directory exists

    # Construct the full new path
    new_result = os.path.join(processing_dir, "song.wav")

    # Rename the file to move it to the new directory
    os.rename(result, new_result)

    # Open the new file
    if platform.system() == 'Windows':
        os.startfile(new_result)
    else:
        os.system(f'open "{new_result}"')

    # Print the path of the saved audio file
    print(new_result, "This is the result")
