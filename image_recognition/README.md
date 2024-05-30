# ImageProcessor

`ImageProcessor` is a Python class designed for decoding base64-encoded images, verifying the decoded images, and generating descriptive captions using a pre-trained model from the Hugging Face Transformers library.

## Requirements

- Python 3.x
- Pillow
- transformers
- base64

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
   pip install pillow transformers
   ```

## Usage

### Initializing the Class

To use the `ImageProcessor` class, first import it and create an instance:

```python
from image_processor import ImageProcessor

image_processor = ImageProcessor()
```

### Decoding an Image

To decode a base64-encoded image and save it to a specified path:

```python
encoded_image_data = {
    'image': 'your_base64_encoded_image_string_here'
}
save_path = './captured_image.jpg'
image_processor.decode_image(encoded_image_data, save_path)
```

### Generating an Image Description

To generate a description of an image:

```python
description = image_processor.generate_image_description(save_path, text="The only object here is: ")
print(description)
```

## Methods

### `__init__(model_name="Salesforce/blip-image-captioning-large")`

Initializes the `ImageProcessor` with a specified pre-trained model for image captioning. The default model is `Salesforce/blip-image-captioning-large`.

### `load_model(model_name)`

Loads the specified model and processor from the Hugging Face Transformers library.

### `decode_image(data, save_path)`

Decodes a base64-encoded image, saves it to the specified path, and verifies that the image can be opened successfully.

- **Parameters**:
  - `data`: A dictionary containing the base64-encoded image string with the key `'image'`.
  - `save_path`: The file path where the decoded image will be saved.

- **Returns**: The path to the saved image if successful, or `None` if an error occurs.

### `generate_image_description(img_path, text="The only object here is: ")`

Generates a descriptive caption for the image at the specified path using the pre-trained model.

- **Parameters**:
  - `img_path`: The file path to the image.
  - `text`: The initial text prompt for generating the image description.

- **Returns**: A descriptive caption for the image.

## Example

Here’s an example script to decode an image, save it, and generate a description:

```python
from image_processor import ImageProcessor

# Initialize the ImageProcessor
image_processor = ImageProcessor()

# Base64 encoded image string
encoded_image_data = {
    'image': 'your_base64_encoded_image_string_here'
}

# Decode the image and save it as a .jpg file
save_path = './captured_image.jpg'
decoded_image_path = image_processor.decode_image(encoded_image_data, save_path)

# Generate a description of the image
if decoded_image_path:
    description = image_processor.generate_image_description(decoded_image_path)
    print(description)
else:
    print("Failed to decode image.")
```