# CameraHandler

`CameraHandler` is a Python class that handles capturing images from a webcam, encoding the images in base64 format, and sending the encoded images to a server. This class uses OpenCV for camera handling and image processing, and it integrates with an external server via HTTP requests.

## Requirements

- Python 3.x
- OpenCV
- NumPy
- Requests
- python-dotenv

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install opencv-python numpy requests python-dotenv
   ```

4. Create a `.env` file in the root directory of the project and add your server API URL:

   ```env
   SERVER_API=<your_server_api_url>
   ```

## Usage

### Initializing the Class

To use the `CameraHandler` class, first import it and create an instance:

```python
from camera_handler import CameraHandler

camera_handler = CameraHandler()
```

### Testing Cameras

You can test the available cameras using the `test_cameras` method:

```python
camera_index = camera_handler.test_cameras()
if camera_index is not None:
    print(f"Camera found at index {camera_index}")
else:
    print("No available camera found.")
```

### Capturing an Image

To capture an image from the webcam:

```python
camera_handler.capture_image()
```

### Encoding an Image

To encode an image in base64 format:

```python
encoded_image = camera_handler.encode_image('path/to/your/image.jpg')
```

### Sending Image to Server

To send an encoded image to the server:

```python
response = camera_handler.send_to_server(encoded_image)
if response:
    print("Image sent successfully:", response)
else:
    print("Failed to send image to the server.")
```

### Capturing, Saving, and Posting an Image

To capture an image, save it, encode it, and send it to the server in one step:

```python
encoded_image = camera_handler.capture_save_and_post_image()
if encoded_image:
    response = camera_handler.send_to_server(encoded_image['image'])
    if response:
        print("Image sent successfully:", response)
    else:
        print("Failed to send image to the server.")
```

## Methods

### `test_cameras()`

Tests for available cameras and returns the index of the first found camera.

### `capture_image()`

Captures an image from the webcam, displays it, and saves it when 's' is pressed.

### `encode_image(image_path)`

Encodes the specified image in base64 format and returns the encoded string.

### `send_to_server(encoded_image)`

Sends the encoded image to the server specified in the `.env` file.

### `capture_save_and_post_image()`

Captures an image, saves it, encodes it, and returns the encoded image.

## Example

Here's an example script to capture, encode, and send an image to the server:

```python
from camera_handler import CameraHandler

camera_handler = CameraHandler()
encoded_image = camera_handler.capture_save_and_post_image()
if encoded_image:
    response = camera_handler.send_to_server(encoded_image['image'])
    if response:
        print("Image sent successfully:", response)
    else:
        print("Failed to send image to the server.")
```