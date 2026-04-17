from pathlib import Path
import pandas as pd
import scikit_posthocs as sp

# =========================
# CONFIG
# =========================

HALSTEAD_FILE = Path("C:/Users/AVAKSon/Desktop/about time/final version/all_halstead_metrics.csv")
GENERAL_FILE = Path("C:/Users/AVAKSon/Desktop/about time/final version/all_languages_metrics.csv")

OUTPUT_DIR = Path("posthoc_no_correction")
OUTPUT_DIR.mkdir(exist_ok=True)

LANG_ORDER = ["C", "C++", "Java", "Python"]

# =========================
# LOAD DATA
# =========================

df_halstead = pd.read_csv(HALSTEAD_FILE, encoding="utf-8-sig")
df_general = pd.read_csv(GENERAL_FILE, encoding="utf-8-sig")

df = pd.concat([df_halstead, df_general], ignore_index=True)

# =========================
# DETECT METRICS
# =========================

exclude_cols = {"language", "file", "file_name", "algorithm_name", "relative_path"}

metric_columns = [
    col for col in df.columns
    if col not in exclude_cols
    and pd.api.types.is_numeric_dtype(df[col])
]

print("\nDetected metrics:")
for m in metric_columns:
    print(" -", m)

# =========================
# PRINT FUNCTION
# =========================

def print_matrix(matrix: pd.DataFrame, metric_name: str):
    print("\n" + "=" * 80)
    print(f"DUNN POST-HOC MATRIX (NO CORRECTION): {metric_name}")
    print("=" * 80)

    print(matrix.round(6).to_string())

# =========================
# ANALYSIS
# =========================

for metric in metric_columns:

    print(f"\nProcessing: {metric}")

    temp_df = df[["language", metric]].dropna()

    try:
        p_matrix = sp.posthoc_dunn(
            temp_df,
            val_col=metric,
            group_col="language"
        )

        p_matrix = p_matrix.reindex(index=LANG_ORDER, columns=LANG_ORDER)

        print_matrix(p_matrix, metric)

        output_file = OUTPUT_DIR / f"dunn_no_correction_{metric}.csv"
        p_matrix.to_csv(output_file, encoding="utf-8-sig")

        print(f"\nSaved CSV: {output_file}")

    except Exception as e:
        print(f"[ERROR] metric {metric} failed: {e}")

print("\nDONE")