# cluster.py
import sys
import pandas as pd
import os
from sklearn.cluster import KMeans

def main():
    if len(sys.argv) < 2:
        print("Usage: python cluster.py <preprocessed_csv>")
        sys.exit(1)
    path = sys.argv[1]
    df = pd.read_csv(path)

    # Choose subset of numerical features
    num = df.select_dtypes(include=['number'])
    if num.empty:
        print("No numeric columns available for clustering.")
        return

    # For reproducibility choose up to 5 features
    features = num.columns[:5].tolist()
    X = num[features].fillna(0).values

    # Choose K = 3 (example). You can choose better K with elbow method (not required)
    k = 3
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    # Count samples per cluster
    counts = pd.Series(labels).value_counts().sort_index()

    out_dir = "/app/pipeline/results"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "clusters.txt")
    with open(out_path, "w") as f:
        for idx, cnt in counts.items():
            f.write(f"cluster_{idx}: {cnt}\n")
    print(f"Wrote cluster counts to {out_path}")

if __name__ == "__main__":
    main()
