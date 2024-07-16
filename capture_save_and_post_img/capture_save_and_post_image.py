import cv2
import base64
import requests
import time

class CameraHandler:
    def __init__(self, save_path='./image_captured/captured_image.jpg'):
        self.save_path = save_path
        self.server_api = "http://localhost:4455/predict/"
        self.camera_index = 1  # Directly set to the second camera index (usually the webcam)

    def capture_image(self):
        start_time = time.time()

        print(f"Time taken to set camera index: {time.time() - start_time:.2f} seconds")

        # Attempt to open the second camera (index 1)
        cap = cv2.VideoCapture(self.camera_index)

        if not cap.isOpened():
            print("Error: Cannot open webcam at index", self.camera_index)
            return

        # Skip initial frames
        for _ in range(3):
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                cap.release()
                return

        print(f"Time taken to grab frames: {time.time() - start_time:.2f} seconds")

        cv2.imwrite(self.save_path, frame)
        print("Image saved!")

        # Encode the image
        encoded_image = self.encode_image(frame)
        print(f"Time taken to encode image: {time.time() - start_time:.2f} seconds")

        # Send to server
        response = self.send_to_server(encoded_image)
        print(f"Time taken to send image to server: {time.time() - start_time:.2f} seconds")

        cap.release()
        cv2.destroyAllWindows()
        return response

    def encode_image(self, frame):
        # Convert image to PNG format
        retval, buffer = cv2.imencode('.png', frame)
        # Encode the image as Base64
        image_base64 = base64.b64encode(buffer).decode('utf-8')
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


