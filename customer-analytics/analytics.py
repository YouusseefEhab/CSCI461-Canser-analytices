# analytics.py
import sys
import pandas as pd
import os

def make_insights(df):
    insights = []

    # ---------------------------------------------------------------------
    # Insight 1: Top 3 numeric columns by variance (measure of variability)
    # ---------------------------------------------------------------------
    num = df.select_dtypes(include=['number'])
    if not num.empty:
        var = num.var().sort_values(ascending=False)
        top3 = var.head(3).index.tolist()
        insights.append(f"Top 3 numeric columns by variance: {top3}")
    else:
        insights.append("No numeric columns available for variance analysis.")

    # ---------------------------------------------------------------------
    # Insight 2: Category or bin distribution
    # ---------------------------------------------------------------------
    candidate_bins = [c for c in df.columns if c.endswith('_bin')]
    if candidate_bins:
        col = candidate_bins[0]
        counts = df[col].value_counts().to_dict()
        insights.append(f"Distribution for {col}: {counts}")
    else:
        obj = df.select_dtypes(include=['object', 'category'])
        if not obj.empty:
            c = obj.columns[0]
            counts = df[c].value_counts().head(5).to_dict()
            insights.append(f"Top values in {c}: {counts}")
        else:
            insights.append("No categorical or binned columns found for distribution insight.")

    # ---------------------------------------------------------------------
    # Insight 3: Strongest correlation between numeric features
    # ---------------------------------------------------------------------
    if num.shape[1] >= 2:
        corr = df.corr(numeric_only=True).abs()

        # Remove self-correlations (diagonal = 1.0)
        for i in range(len(corr)):
            corr.iat[i, i] = 0

        # Flatten the correlation matrix and drop duplicates
        corr_unstacked = corr.unstack().drop_duplicates().sort_values(ascending=False)

        if corr_unstacked.empty or corr_unstacked.max() == 0:
            insights.append("No meaningful correlations detected among numeric features.")
        else:
            top_pair = corr_unstacked.head(1)
            (col1, col2), value = top_pair.index[0], top_pair.values[0]
            insights.append(f"Strongest correlation ({value:.3f}) between '{col1}' and '{col2}'.")
    else:
        insights.append("Not enough numeric columns to compute correlations.")

    return insights


def main():
    if len(sys.argv) < 2:
        print("Usage: python analytics.py <preprocessed_csv>")
        sys.exit(1)

    path = sys.argv[1]

    # Load data
    df = pd.read_csv(path)
    print(f"📘 Loaded preprocessed data with shape: {df.shape}")

    insights = make_insights(df)

    # Save insights to /results/
    out_dir = "/app/pipeline/results"
    os.makedirs(out_dir, exist_ok=True)

    for i, text in enumerate(insights[:3], start=1):
        fname = os.path.join(out_dir, f"insight{i}.txt")
        with open(fname, "w") as f:
            f.write(text + "\n")
        print(f"📝 Wrote {fname}")

    # Automatically move to visualization
    print("📊 Running visualization step...")
    os.system(f"python visualize.py {path}")


if __name__ == "__main__":
    main()
