from gradio_client import Client
import os


text = "This is an text example"





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