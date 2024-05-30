import base64
from PIL import Image
import warnings
from transformers import BlipProcessor, BlipForConditionalGeneration

class ImageProcessor:
    def __init__(self, model_name="Salesforce/blip-image-captioning-large"):
        self.processor, self.model = self.load_model(model_name)

    @staticmethod
    def load_model(model_name):
        warnings.filterwarnings('ignore', category=UserWarning, module='transformers')
        processor = BlipProcessor.from_pretrained(model_name)
        model = BlipForConditionalGeneration.from_pretrained(model_name)
        return processor, model

    @staticmethod
    def decode_image(data, save_path):
        try:
            encoded_image = data['image']
            print(f"Encoded image string length: {len(encoded_image)}")
            image_data = base64.b64decode(encoded_image)
            print(f"Decoded image data length: {len(image_data)}")

            # Save decoded data to file to verify
            with open(save_path, 'wb') as file:
                file.write(image_data)

            print(f"Successfully decoded image to {save_path}")

            # Verify the image can be opened
            image = Image.open(save_path)
            image.verify()
            print(f"Image verified successfully: {save_path}")
            return save_path

        except Exception as e:
            print(f"Failed to decode and save image: {e}")

    def generate_image_description(self, img_path, text="The only object here is: "):
        raw_image = Image.open(img_path).convert('RGB')
        inputs = self.processor(raw_image, text, return_tensors="pt")
        output = self.model.generate(**inputs, max_new_tokens=20)
        description = self.processor.decode(output[0], skip_special_tokens=True)
        return description

# Example usage:
# Initialize the ImageProcessor
#image_processor = ImageProcessor()

# Decode the image and save it as a .jpg file
#encoded_image = "your_base64_encoded_image_string_here"
#save_path = './captured_image.jpg'
#decoded_image_path = image_processor.decode_image(encoded_image, save_path)

# Generate a description of the image
#description = image_processor.generate_image_description(decoded_image_path)
#print(description)
