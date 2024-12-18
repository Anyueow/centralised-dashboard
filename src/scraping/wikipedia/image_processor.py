from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO

class ImageProcessor:
    @staticmethod
    def extract_image_url(page):
        if page and page.images:
            # Filter for common image formats
            valid_extensions = ('.jpg', '.jpeg', '.png', '.gif')
            for image_url in page.images:
                if image_url.lower().endswith(valid_extensions):
                    return image_url
        return None

    @staticmethod
    def fetch_and_resize_image(url, width=80):
        headers = {
            'User-Agent': 'SEO Project (the.e.sapien@gmail.com)'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensure the request was successful
        image = Image.open(BytesIO(response.content))
        aspect_ratio = image.height / image.width
        new_height = int(width * aspect_ratio)
        resized_image = image.resize((width, new_height))
        return resized_image
