import requests
from PIL import Image
from io import BytesIO
import os
import hashlib
import random

# Set the save path to the same directory as the script
save_path = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
if not os.path.exists(save_path):
    os.makedirs(save_path)  # Create the directory if it doesn't exist

# List of possible tags
tags = [
    'waifu', 'maid', 'marin-kitagawa', 'mori-calliope', 'raiden-shogun', 
    'oppai', 'selfies', 'uniform', 'kamisato-ayaka'
]

# Randomly select one tag from the list
selected_tag = random.choice(tags)

# Prepare the API request parameters
url = 'https://api.waifu.im/search'
params = {
    'included_tags': [selected_tag],
    'is_nsfw': False,
    'height': '>=2000',
    'Accept-Version': 'v6'
}

response = requests.get(url, params=params)

def get_image_hash(image_content):
    """Generate MD5 hash for the image content."""
    return hashlib.md5(image_content).hexdigest()

if response.status_code == 200:
    data = response.json()
    print(f"Selected Tag: {selected_tag}")  # Print the selected tag
    print(data)  # Print the whole response to check its structure

    # Check if 'images' key exists and if there's at least one image
    if 'images' in data and len(data['images']) > 0:
        image_url = data['images'][0]['url']  # Get the first image URL
        
        # Get the image
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            # Generate hash of the new image
            new_image_hash = get_image_hash(image_response.content)
            
            # Set the file path to save the image (you can use the image filename or any desired name)
            file_path = os.path.join(save_path, 'image.jpg')
            
            # Check if the file already exists and if its content matches the new image
            if os.path.exists(file_path):
                with open(file_path, 'rb') as existing_file:
                    existing_image_hash = get_image_hash(existing_file.read())
                    if existing_image_hash == new_image_hash:
                        print("The image is already saved and is identical. Skipping download.")
                        # Skip the download and saving process
                        image_response = None  # Clear the image_response to prevent further processing
            if image_response:  # Only process the image if it's not already skipped
                # Open the image
                image = Image.open(BytesIO(image_response.content))
                
                # Convert the image to RGB (required for saving as JPEG)
                image = image.convert("RGB")
                
                # Save the image as JPEG, overwriting any existing file with the same name
                image.save(file_path, 'JPEG')
                print(f"Image saved to {file_path}")
        else:
            print('Failed to retrieve the image.')
    else:
        print('No images found or missing "images" key.')
else:
    print('Request failed with status code:', response.status_code)
