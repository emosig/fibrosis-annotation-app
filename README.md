# Fibrosis Patch Annotation Tool

A Streamlit application for classifying cardiac fibrosis patches to evaluate a clustering algorithm.

**Live App:** https://fibrosis-annotation-app.streamlit.app/

## Overview
* **Randomized:** Image order is randomized per session.
* **Stateful:** Sessions can be paused and resumed using the Expert ID.
* **Cloud Storage:** Annotations are saved directly to a Google Sheets backend.
* **Reference Guide:** Includes a sidebar with visual examples for classification.

## Classification Categories
1. Compact
2. Diffuse
3. Interstitial
4. Leftover

## Repository Files
* `app.py`: Main Streamlit application.
* `analysis.py`: Calculates Cohen's Kappa score to compare expert annotations against algorithm predictions.
* `extract_patches.py`: Local utility to convert `.pickle` files to `.png`.
* `data/`: Directory containing patch images, reference images, and CSV files.

## Running the Analysis
To evaluate agreement metrics:
1. Save algorithm predictions in `data/algo_predictions.csv` (columns: `image_name`, `algo_label`).
2. Export expert results from Google Sheets and save as `data/expert_annotations.csv`.
3. Execute the analysis script:
   ```bash
   python analysis.py