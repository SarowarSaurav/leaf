import streamlit as st
import requests
import base64
from PIL import Image
import io

# Set page configuration
st.set_page_config(
    page_title="Leaf Disease Identifier",
    page_icon="🍃",
    layout="centered"
)

# Custom CSS (same as before)
st.markdown("""
<style>
.main-title {
    font-size: 36px;
    color: #2C5F2D;
    text-align: center;
    margin-bottom: 20px;
}
.subtitle {
    font-size: 18px;
    color: #4A6741;
    text-align: center;
    margin-bottom: 30px;
}
.stButton>button {
    background-color: #2C5F2D;
    color: white;
    width: 100%;
    border: none;
    padding: 10px;
    border-radius: 5px;
}
.stButton>button:hover {
    background-color: #4A6741;
}
</style>
""", unsafe_allow_html=True)

# Title and Description
st.markdown('<h1 class="main-title">🍃 Leaf Disease Identifier</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload a leaf image and get instant disease analysis</p>', unsafe_allow_html=True)

def encode_image(image):
    """Encode image to base64"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def analyze_leaf_disease(image):
    """Analyze leaf image using backend proxy"""
    # Backend proxy URL - replace with your actual backend URL
    BACKEND_URL = "https://render-036z.onrender.com/analyze_leaf"

    try:
        # Encode the image
        base64_image = encode_image(image)

        # Send request to backend proxy
        response = requests.post(
            BACKEND_URL, 
            json={"image": base64_image},
            headers={"Content-Type": "application/json"}
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Check if analysis is in the response
        if 'analysis' in result:
            return result['analysis']
        elif 'error' in result:
            st.error(f"Analysis Error: {result['error']}")
            return None
        
    except requests.exceptions.RequestException as e:
        st.error(f"Network Error: {e}")
        return None

def main():
    # Image upload
    uploaded_file = st.file_uploader(
        "Upload a leaf image", 
        type=["jpg", "jpeg", "png"],
        help="Upload a clear image of a leaf for disease analysis"
    )

    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Leaf Image', use_column_width=True)

        # Analysis button
        if st.button('Analyze Leaf Disease'):
            with st.spinner('Analyzing image... This might take a moment'):
                analysis = analyze_leaf_disease(image)
                
                if analysis:
                    st.success('Analysis Complete!')
                    st.markdown("### 🔬 Leaf Disease Analysis")
                    st.write(analysis)
                else:
                    st.error("Failed to analyze the image. Please try again.")

if __name__ == "__main__":
    main()
