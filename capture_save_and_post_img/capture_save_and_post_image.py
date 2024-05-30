import cv2
import base64
import numpy as np
import requests
import os


class CameraHandler:
    def __init__(self, save_path='./image_captured/captured_image.jpg'):
        self.save_path = save_path
        self.server_api = "http://localhost:4455/predict/"

    def test_cameras(self):
        index = 0
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                print(f"No camera found at index {index}")
            else:
                print(f"Camera found at index {index}!")
                cap.release()
                break
            index += 1
            cap.release()
            if index > 10:  # Adjust the range as needed
                break

    def capture_image(self):
        self.test_cameras()
        # Attempt to open the first available camera
        camera_index = 0  # Change this if the default isn't correct
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
                cv2.imwrite(self.save_path, frame)
                print("Image saved!")
                # Encode the image
                encoded_image = self.encode_image(frame)
                # Send to server
                response = self.send_to_server(encoded_image)
                cap.release()
                cv2.destroyAllWindows()
                return response
            elif key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return None

        cap.release()
        cv2.destroyAllWindows()
        return None

    def encode_image(self, frame):
        # Convert image to PNG format
        retval, buffer = cv2.imencode('.png', frame)
        # Encode the image as Base64
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        print(image_base64[:100] ) 
        return image_base64

    def send_to_server(self, encoded_image):
        if not self.server_api:
            print("Server API URL not found in environment variables")
            return None
        headers = {'Content-Type': 'application/json'}
        data = {'base64_image': encoded_image}
        try:
            response = requests.post(self.server_api, json=data, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending image to server: {e}")
            return None



    

