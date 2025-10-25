# visualize.py
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) < 2:
        print("Usage: python visualize.py <preprocessed_file>")
        sys.exit(1)

    in_path = sys.argv[1]
    out_dir = "/app/pipeline/results"
    os.makedirs(out_dir, exist_ok=True)

    print(f"📊 Loading preprocessed data: {in_path}")
    df = pd.read_csv(in_path)
    print(f"✅ Loaded {df.shape[0]} rows and {df.shape[1]} columns")

    # -------- Basic Histograms (similar to Lab_03) --------
    plt.figure(figsize=(12, 12))
    df.hist(figsize=(15, 15))
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "all_features_hist.png"))
    plt.close()
    print("📈 Saved histogram for all numeric features")

    # -------- Compare malignant vs benign (if diagnosis column exists) --------
    if "diagnosis" in df.columns:
        df_m = df[df["diagnosis"] == "M"]
        df_b = df[df["diagnosis"] == "B"]

        for feature in ["area", "perimeter", "radius", "texture"]:
            if feature in df.columns:
                plt.figure(figsize=(6, 4))
                df_m[feature].hist(alpha=0.5, label="Malignant")
                df_b[feature].hist(alpha=0.5, label="Benign")
                plt.title(f"Distribution of {feature}")
                plt.xlabel(feature)
                plt.ylabel("Count")
                plt.legend()
                plt.tight_layout()
                plt.savefig(os.path.join(out_dir, f"{feature}_comparison.png"))
                plt.close()
                print(f"🩺 Saved comparison plot for '{feature}'")

    # -------- Correlation Heatmap --------
    try:
        import seaborn as sns
        plt.figure(figsize=(10, 8))
        corr = df.corr(numeric_only=True)
        sns.heatmap(corr, cmap="coolwarm", center=0)
        plt.title("Feature Correlation Heatmap")
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, "correlation_heatmap.png"))
        plt.close()
        print("🔥 Saved correlation heatmap")
    except Exception as e:
        print(f"⚠️ Could not generate heatmap: {e}")

    print("✅ Visualization completed successfully")

    # -------- Run clustering after visualization --------
    print("🤖 Running clustering step...")
    os.system(f"python cluster.py {in_path}")

if __name__ == "__main__":
    main()
