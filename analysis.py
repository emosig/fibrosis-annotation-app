import pandas as pd
from sklearn.metrics import cohen_kappa_score, classification_report

EXPERT_FILE = "data/expert_annotations.csv"
ALGO_FILE = "data/algo_predictions.csv"

def analyze_agreement():
    try:
        df_expert = pd.read_csv(EXPERT_FILE)
        df_algo = pd.read_csv(ALGO_FILE)
    except FileNotFoundError as e:
        print(f"Error: Missing data file. {e}")
        return

    # Merge tables based on image name
    merged_df = pd.merge(df_expert, df_algo, on="image_name")
    
    if merged_df.empty:
        print("No matching image rows found between expert annotations and algorithm predictions.")
        return

    print(f"Analyzing {len(merged_df)} completed matches...\n")

    # Group by expert if you have multiple experts
    for expert, group in merged_df.groupby("expert_id"):
        print(f"=== Report for {expert} ===")
        
        # Calculate Cohen's Kappa
        kappa = cohen_kappa_score(group["expert_label"], group["algo_label"])
        print(f"Cohen's Kappa Score: {kappa:.3f}")
        
        # Qualitative rating
        if kappa < 0:
            print("Agreement rating: Poor (Less than chance agreement)")
        elif kappa <= 0.20:
            print("Agreement rating: Slight")
        elif kappa <= 0.40:
            print("Agreement rating: Fair")
        elif kappa <= 0.60:
            print("Agreement rating: Moderate")
        elif kappa <= 0.80:
            print("Agreement rating: Substantial")
        else:
            print("Agreement rating: Almost Perfect")
            
        print("\nClassification Report:")
        print(classification_report(group["expert_label"], group["algo_label"]))
        print("-" * 40)

if __name__ == "__main__":
    analyze_agreement()