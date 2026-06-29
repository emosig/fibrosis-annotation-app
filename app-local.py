import os
import random
import pandas as pd
import streamlit as st
from PIL import Image

# --- CONFIGURATION ---
IMAGE_DIR = "data/patches"
OUTPUT_FILE = "data/expert_annotations.csv"
CLASSES = ["Compact", "Diffuse", "Interstitial"]

# Ensure directories and output file exist
os.makedirs(IMAGE_DIR, exist_ok=True)
if not os.path.exists(OUTPUT_FILE):
    df = pd.DataFrame(columns=["expert_id", "image_name", "expert_label"])
    df.to_csv(OUTPUT_FILE, index=False)

st.set_page_config(page_title="Fibrosis Patch Annotator", layout="centered")
st.title("Fibrosis Patch Classification")

# --- STEP 1: EXPERT LOGIN ---
if "expert_id" not in st.session_state:
    st.subheader("Welcome. Please enter your identifier to begin.")
    expert_input = st.text_input("Expert ID (e.g., Expert_A):").strip()
    if st.button("Start Session"):
        if expert_input:
            st.session_state.expert_id = expert_input
            st.rerun()
        else:
            st.error("Please enter a valid ID.")
    st.stop()

# --- STEP 2: SESSION INITIALIZATION ---
if "initialized" not in st.session_state:
    # Fetch all patch images
    all_images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not all_images:
        st.warning(f"No images found in '{IMAGE_DIR}'. Please add images and refresh.")
        st.stop()
        
    # Filter out what THIS expert has already labeled in past sessions
    df_existing = pd.read_csv(OUTPUT_FILE)
    labeled_by_user = df_existing[df_existing["expert_id"] == st.session_state.expert_id]["image_name"].tolist()
    images_to_label = [img for img in all_images if img not in labeled_by_user]
    
    # Randomize the remaining images for this session
    random.shuffle(images_to_label)
    
    st.session_state.image_list = images_to_label
    st.session_state.current_index = 0
    st.session_state.initialized = True

# --- STEP 3: ANNOTATION INTERFACE ---
images = st.session_state.image_list
idx = st.session_state.current_index

# Check if there are any images left to label
if idx >= len(images):
    st.success(" 🎉 All done! Thank you for your time. You can safely close this window.")
    if st.button("Log in as a different expert"):
        st.session_state.clear()
        st.rerun()
    st.stop()

current_image_name = images[idx]
image_path = os.path.join(IMAGE_DIR, current_image_name)

# Progress indicator
st.write(f"Logged in as: **{st.session_state.expert_id}**")
st.progress((idx) / len(images) if len(images) > 0 else 1.0)
st.write(f"Patch {idx + 1} of {len(images)} remaining this session.")

# Display the image alone
try:
    img = Image.open(image_path)
    st.image(img, use_container_width=True)
except Exception as e:
    st.error(f"Error loading image {current_image_name}: {e}")

# Function to save decision and move forward
def save_choice(label):
    # Save to CSV immediately
    new_row = pd.DataFrame([{
        "expert_id": st.session_state.expert_id,
        "image_name": current_image_name,
        "expert_label": label
    }])
    new_row.to_csv(OUTPUT_FILE, mode='a', header=False, index=False)
    
    # Move to next image
    st.session_state.current_index += 1

# Display evaluation buttons side by side
col1, col2, col3 = st.columns(3)

with col1:
    if st.button(CLASSES[0], use_container_width=True):
        save_choice(CLASSES[0])
        st.rerun()

with col2:
    if st.button(CLASSES[1], use_container_width=True):
        save_choice(CLASSES[1])
        st.rerun()

with col3:
    if st.button(CLASSES[2], use_container_width=True):
        save_choice(CLASSES[2])
        st.rerun()

st.info("Your progress is saved automatically after every click. You can stop whenever you get tired.")