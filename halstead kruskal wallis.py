from pathlib import Path
import csv
from scipy import stats

# =========================
# CONFIG
# =========================

INPUT_FILE = Path(r"C:/Users/AVAKSon/Desktop/about time/final version/halstead_results/all_halstead_metrics.csv")
OUTPUT_FILE = INPUT_FILE.parent / "halstead_kruskal_results.csv"

LANGUAGES = ["C", "C++", "Java", "Python"]

METRICS = [
    "n1_distinct_operators",
    "n2_distinct_operands",
    "N1_total_operators",
    "N2_total_operands",
    "vocabulary",
    "length",
    "volume",
    "difficulty",
    "effort",
]

# =========================
# HELPERS
# =========================

def read_csv_rows(file_path: Path):
    rows = []
    with file_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def extract_metric_values(rows, metric_name, language):
    values = []

    for row in rows:
        if row.get("language") != language:
            continue

        value = str(row.get(metric_name, "")).strip()
        if value == "":
            continue

        try:
            values.append(float(value))
        except ValueError:
            continue

    return values


def interpret_p_value(p_value):
    if p_value < 0.05:
        return "Statistically significant"
    return "Not statistically significant"


# =========================
# MAIN ANALYSIS
# =========================

def main():
    if not INPUT_FILE.exists():
        print(f"[ERROR] Input file not found: {INPUT_FILE}")
        return

    rows = read_csv_rows(INPUT_FILE)
    if not rows:
        print("[ERROR] CSV file is empty.")
        return

    results = []

    print("=" * 80)
    print("KRUSKAL–WALLIS TEST RESULTS FOR HALSTEAD METRICS")
    print("=" * 80)

    for metric in METRICS:
        grouped_values = []

        counts_by_language = {}
        for lang in LANGUAGES:
            values = extract_metric_values(rows, metric, lang)
            counts_by_language[lang] = len(values)
            grouped_values.append(values)

        # check that every group has data
        if any(len(group) == 0 for group in grouped_values):
            print(f"[WARNING] Metric '{metric}' skipped because one or more language groups are empty.")
            continue

        stat, p_value = stats.kruskal(*grouped_values)

        result_row = {
            "metric": metric,
            "H_statistic": round(stat, 6),
            "p_value": p_value,
            "interpretation": interpret_p_value(p_value),
            "count_C": counts_by_language["C"],
            "count_Cpp": counts_by_language["C++"],
            "count_Java": counts_by_language["Java"],
            "count_Python": counts_by_language["Python"],
        }
        results.append(result_row)

        p_display = "< 0.001" if p_value < 0.001 else f"{p_value:.6f}"
        print(f"{metric}: H = {stat:.6f}, p = {p_display} -> {result_row['interpretation']}")

    # save CSV
    if results:
        fieldnames = [
            "metric",
            "H_statistic",
            "p_value",
            "interpretation",
            "count_C",
            "count_Cpp",
            "count_Java",
            "count_Python",
        ]

        with OUTPUT_FILE.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print("\nSaved results to:")
        print(OUTPUT_FILE)
    else:
        print("\n[WARNING] No results were produced.")


if __name__ == "__main__":
    main()