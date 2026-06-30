import os
import random
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURATION ---
IMAGE_DIR = "data/patches"
CLASSES = ["Compact", "Diffuse", "Interstitial"]

st.set_page_config(page_title="Fibrosis Patch Annotator", layout="centered")
st.title("Fibrosis Patch Classification")

# --- INITIALIZE GOOGLE SHEETS CONNECTION ---
# This connects to the sheet defined in your Streamlit secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing data from Google Sheets (clearing cache to ensure it's fresh)
st.cache_data.clear()
try:
    df_existing = conn.read(worksheet="Sheet1", usecols=[0, 1, 2])
    df_existing = df_existing.dropna(how="all") # Clean up empty rows
except Exception as e:
    st.error(f"Could not connect to Google Sheets. Check your setup. Errore dettagliato: {e}")
    st.stop()

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
    all_images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not all_images:
        st.warning(f"No images found in '{IMAGE_DIR}'.")
        st.stop()
        
    # Filter out what THIS expert has already labeled based on the Google Sheet
    if not df_existing.empty:
        labeled_by_user = df_existing[df_existing["expert_id"] == st.session_state.expert_id]["image_name"].tolist()
    else:
        labeled_by_user = []
        
    images_to_label = [img for img in all_images if img not in labeled_by_user]
    random.shuffle(images_to_label)
    
    st.session_state.image_list = images_to_label
    st.session_state.current_index = 0
    st.session_state.initialized = True

# --- STEP 3: ANNOTATION INTERFACE ---
images = st.session_state.image_list
idx = st.session_state.current_index

if idx >= len(images):
    st.success(" 🎉 All done! Thank you for your time. You can safely close this window.")
    if st.button("Log in as a different expert"):
        st.session_state.clear()
        st.rerun()
    st.stop()

current_image_name = images[idx]
image_path = os.path.join(IMAGE_DIR, current_image_name)

st.write(f"Logged in as: **{st.session_state.expert_id}**")
st.progress((idx) / len(images) if len(images) > 0 else 1.0)
st.write(f"Patch {idx + 1} of {len(images)} remaining this session.")

try:
    img = Image.open(image_path)
    st.image(img, use_container_width=True)
except Exception as e:
    st.error(f"Error loading image {current_image_name}: {e}")

# Function to save decision to Google Sheets
def save_choice(label):
    new_row = pd.DataFrame([{
        "expert_id": st.session_state.expert_id,
        "image_name": current_image_name,
        "expert_label": label
    }])
    
    # Re-read the latest sheet data to prevent overwriting if multiple experts are online
    current_df = conn.read(worksheet="Sheet1", usecols=[0, 1, 2]).dropna(how="all")
    updated_df = pd.concat([current_df, new_row], ignore_index=True)
    
    # Push updated table back to Google Sheets
    conn.update(worksheet="Sheet1", data=updated_df)
    
    st.session_state.current_index += 1

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