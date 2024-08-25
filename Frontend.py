# frontend.py

import streamlit as st
import io
from PIL import Image
from image_analysis import analyze_image
from database import store_item, get_all_items
from recommendation import get_outfit_recommendation

def main():
    st.title("AI Wardrobe Assistant")

    # Sidebar for navigation
    page = st.sidebar.selectbox("Choose a page", ["Upload Clothes", "View Wardrobe", "Get Outfit Recommendations"])

    if page == "Upload Clothes":
        upload_clothes()
    elif page == "View Wardrobe":
        view_wardrobe()
    elif page == "Get Outfit Recommendations":
        get_recommendations()

def upload_clothes():
    st.header("Upload Clothes")
    uploaded_file = st.file_uploader("Choose an image of a clothing item", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Analyze and Store Item"):
            # Convert image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()
            
            # Analyze image
            description = analyze_image(img_bytes)
            st.write("Item Description:", description)
            
            # Store item
            store_item(description, img_bytes)
            st.success("Item stored in your virtual wardrobe!")

def view_wardrobe():
    st.header("Your Wardrobe")
    items = get_all_items()
    for item in items:
        st.write(item['description'])
        st.image(item['image'], width=200)

def get_recommendations():
    st.header("Get Outfit Recommendations")
    prompt = st.text_input("Describe the occasion or style you're looking for")
    if st.button("Get Recommendation"):
        recommendation = get_outfit_recommendation(prompt)
        st.write(recommendation)

if __name__ == "__main__":
    main()