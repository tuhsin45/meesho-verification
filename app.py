import streamlit as st
import google.generativeai as genai
from PIL import Image
import re

# Page Configuration
st.set_page_config(
    layout="wide",
    page_title="Product Return Verification"
)

st.title("Product Return Verification System")
st.caption("A two-step process for sellers and delivery partners to verify product returns.")

# Gemini API Configuration
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except (KeyError, AttributeError):
    st.error("Gemini API Key not found. Please add it to your Streamlit secrets.")
    st.stop()

# --- Core Functions ---

def generate_checklist_from_image(image: Image.Image) -> list[str]:
    """
    (SELLER'S FUNCTION)
    Uses Gemini to generate a checklist of physical parameters from the original product image.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt_text = """
    You are an expert product inspector. Analyze the provided image of the product carefully.
    Your task is to identify the top 3 most prominent and verifiable physical characteristics.
    Focus on the most obvious details like main colors, brand logos, and primary design features.
    The output MUST be a numbered list with exactly 3 points. Do not add any other text.
    """
    try:
        response = model.generate_content([prompt_text, image])
        checklist_points = response.text.strip().split('\n')
        cleaned_points = [re.sub(r'^\d+\.\s*', '', point).strip() for point in checklist_points]
        return [point for point in cleaned_points if point]
    except Exception as e:
        st.error(f"Error generating checklist: {e}")
        return []

def verify_product_features(returned_image: Image.Image, original_checklist: list[str]) -> dict:
    """
    (DELIVERY PARTNER'S FUNCTION)
    Verifies if the features from the original_checklist are present in the returned_image.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    formatted_checklist = "\n".join(f"{i+1}. {item}" for i, item in enumerate(original_checklist))
    
    prompt_text = f"""
    You are a product return verifier. I will provide you with an image of a returned product and a checklist of features from the original product.

    Your task is to compare the image of the returned item against EACH point in the original checklist.
    For each point, respond with only "YES" if the feature is clearly and accurately present in the image, or "NO" if it is not.

    ORIGINAL CHECKLIST:
    {formatted_checklist}

    Your response MUST be a numbered list of "YES" or "NO" answers corresponding to each checklist point. Do not add any other text or explanation.
    """
    
    try:
        response = model.generate_content([prompt_text, returned_image])
        verification_results = response.text.strip().split('\n')
        
        match_details = {}
        all_matched = True
        
        for i, item in enumerate(original_checklist):
            is_match = (i < len(verification_results)) and ("yes" in verification_results[i].lower())
            match_details[item] = is_match
            if not is_match:
                all_matched = False
                
        return {"approved": all_matched, "details": match_details}

    except Exception as e:
        st.error(f"Error during verification: {e}")
        return {"approved": False, "details": {item: False for item in original_checklist}}


# --- UI Layout ---
st.markdown("---")

# Initialize session state for data persistence
if "original_checklist" not in st.session_state:
    st.session_state.original_checklist = []
if "verification_result" not in st.session_state:
    st.session_state.verification_result = None

col1, col2 = st.columns(2)

# === COLUMN 1: SELLER'S WORKFLOW ===
with col1:
    st.header("Step 1: Seller Generates Checklist")
    
    original_file = st.file_uploader(
        "Upload Original Product Image",
        type=["png", "jpg", "jpeg"],
        key="original_uploader"
    )

    if original_file is not None:
        img = Image.open(original_file)
        st.image(img, caption="Original Product", use_container_width=True) # <-- FIXED HERE

        if st.button("Generate Verification Checklist", type="primary"):
            with st.spinner("Generating checklist..."):
                st.session_state.original_checklist = generate_checklist_from_image(img)
                st.session_state.verification_result = None # Reset verification on new checklist
                if not st.session_state.original_checklist:
                    st.warning("Could not generate a checklist. Please try another image.")
    
    if st.session_state.original_checklist:
        st.markdown("---")
        st.subheader("Original Product Checklist")
        for point in st.session_state.original_checklist:
            st.markdown(f"- {point}")

# === COLUMN 2: DELIVERY PARTNER'S WORKFLOW ===
with col2:
    st.header("Step 2: Delivery Partner Verifies Return")

    if not st.session_state.original_checklist:
        st.info("Please generate the original product checklist in Step 1 first.")
    else:
        return_file = st.file_uploader(
            "Upload Returned Product Image",
            type=["png", "jpg", "jpeg"],
            key="return_uploader"
        )

        if return_file is not None:
            return_img = Image.open(return_file)
            st.image(return_img, caption="Returned Product", use_container_width=True) # <-- FIXED HERE

            if st.button("Verify Returned Product", type="primary"):
                with st.spinner("Comparing products..."):
                    st.session_state.verification_result = verify_product_features(
                        return_img, st.session_state.original_checklist
                    )

        if st.session_state.verification_result:
            st.markdown("---")
            st.subheader("Verification Results")
            
            result_data = st.session_state.verification_result
            
            for item, is_match in result_data["details"].items():
                emoji = "✅" if is_match else "❌"
                st.markdown(f"{emoji} {item}")
            
            st.markdown("---")
            
            if result_data["approved"]:
                st.success("*RETURN APPROVED:* All features match the original product.")
            else:
                st.error("*RETURN REJECTED:* One or more features do not match.")