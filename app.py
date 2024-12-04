import streamlit as st
import requests
import base64
import os
from PIL import Image
import io

# Set page configuration
st.set_page_config(
    page_title="Leaf Disease Identifier",
    page_icon="🍃",
    layout="centered"
)

# Custom CSS for styling
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
    """Analyze leaf image using Claude API"""
    # Replace with your actual API key
    api_key = st.secrets.get("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")
    
    if not api_key:
        st.error("API Key not configured. Please set up Anthropic API key.")
        return None

    headers = {
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
        "X-API-Key": api_key
    }

    payload = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": encode_image(image)
                        }
                    },
                    {
                        "type": "text",
                        "text": """Analyze this leaf image in detail. 
                        Identify:
                        1. Plant species (if possible)
                        2. Specific disease or health condition
                        3. Detailed symptoms
                        4. Potential causes
                        5. Recommended treatment or management strategies
                        
                        Provide a comprehensive and clear explanation."""
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages", 
            headers=headers, 
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        return result['content'][0]['text']
    
    except requests.exceptions.RequestException as e:
        st.error(f"API Request Error: {e}")
        return None
    except KeyError:
        st.error("Unexpected API response format")
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
