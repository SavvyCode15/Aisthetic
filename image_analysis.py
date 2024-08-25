# image_analysis.py

import google.generativeai as genai
from PIL import Image
import io

# Configure the Gemini API (make sure to set your API key in the environment variables)
genai.configure(api_key="AIzaSyD3kFTAAPuQvos29RBY5n_AtFcuHUpCvN8")

def analyze_image(image_bytes):
    # Convert bytes to PIL Image
    image = Image.open(io.BytesIO(image_bytes))
    
    # Set up the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Prepare the prompt
    prompt = """
    Analyze this image of a clothing item. Describe it in detail, including:
    1. Type of clothing (e.g., shirt, pants, dress)
    2. Color(s)
    3. Pattern (if any)
    4. Style (e.g., casual, formal, sporty)
    5. Material (if identifiable)
    6. Any notable features or details

    Provide the description in a structured format.
    """
    
    # Generate content
    response = model.generate_content([prompt, image])
    
    return response.text

# Example usage:
# with open('path_to_image.jpg', 'rb') as f:
#     image_bytes = f.read()
# description = analyze_image(image_bytes)
# print(description)