import cv2
import base64
import numpy as np
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file such as the server API
load_dotenv()

class CameraHandler:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.save_dir = os.path.join(current_dir, 'image_captured')
        self.save_path = os.path.join(self.save_dir, 'image.jpg')
        self.server_api = os.getenv('SERVER_API')

    def test_cameras(self):
        index = 0
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                print(f"No camera found at index {index}")
            else:
                print(f"Camera found at index {index}!")
                cap.release()
                return index  # Return the index of the first found camera
            index += 1
            cap.release()
            if index > 10:  # Adjust the range as needed
                break
        return None

    def capture_image(self):
        camera_index = self.test_cameras()
        if camera_index is None:
            print("No available camera found.")
            return

        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            print("Error: Cannot open webcam")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            cv2.imshow('Press "s" to save the image and "q" to quit', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                # Ensure the save directory exists
                os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
                cv2.imwrite(self.save_path, frame)
                print("Image saved to:", self.save_path)
                break
            elif key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def encode_image(self, image_path):
        try:
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
                encoded_image = base64.b64encode(image_data).decode('utf-8')
            data = {'image': encoded_image}
            print(f"Successfully encoded image from {image_path}")
            print(f"Encoded image string length: {len(encoded_image)}")
            return data
        except Exception as e:
            print(f"Error encoding image: {e}")
            return None

    def send_to_server(self, encoded_image):
        if not self.server_api:
            print("Server API URL not found in environment variables")
            return None
        headers = {'Content-Type': 'application/json'}
        data = {'image': encoded_image}
        try:
            response = requests.post(self.server_api, json=data, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending image to server: {e}")
            return None

    def capture_encode_and_post_image(self):
        self.capture_image()
        encoded_image = self.encode_image(self.save_path)
        if encoded_image:
            self.send_to_server(encoded_image)
            return encoded_image
        

# Example usage
#camera_handler = CameraHandler()
#encoded_image = camera_handler.capture_save_and_post_image()
