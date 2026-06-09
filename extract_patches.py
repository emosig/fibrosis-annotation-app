import os
import pickle
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# --- CONFIGURATION ---
# The folder where your pickle files currently are
LOAD_DIR = 'C:/ELOY/GIT/fibrosis_tests/patches/no_table2/'

# The target folder inside your new Streamlit app
# Change this path to wherever you initialized your VS Code repo
SAVE_DIR = 'fibrosis-annotation-app/data/patches/'

# Recreate your custom colormap so the saved images look exactly like your notebook
colors = ['white', 'gray', 'black']
cmap = ListedColormap(colors)

# Ensure the save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

def extract_and_save():
    hearts = os.listdir(LOAD_DIR)
    
    total_saved = 0
    for heart in hearts:
        heart_dir = os.path.join(LOAD_DIR, heart)
        if not os.path.isdir(heart_dir):
            continue
            
        print(f"Processing heart: {heart}...")
        slices = [f for f in os.listdir(heart_dir) if f.endswith('no_background.pickle')]
        
        for s in slices:
            slice_idx = s[7:9] # Extracting slice index just like your notebook
            pickle_path = os.path.join(heart_dir, s)
            
            with open(pickle_path, 'rb') as handle:
                slice_patches = pickle.load(handle)
                
            # Filter logic from your notebook (dist between 0 and 1)
            filtered_patches = [p for p in slice_patches if 0 < p['dist'] < 1]
            
            for i, patch in enumerate(filtered_patches):
                # Create a unique, traceable filename
                # Example: E10615_MYH7_slice03_patch0.png
                filename = f"{heart}_slice{slice_idx}_patch{i}.png"
                save_path = os.path.join(SAVE_DIR, filename)
                
                # Save the array as an image using your specific colormap
                plt.imsave(save_path, patch['image'], cmap=cmap)
                total_saved += 1
                
    print(f"🎉 Success! Extracted and saved {total_saved} patches as PNGs to {SAVE_DIR}")

if __name__ == "__main__":
    extract_and_save()