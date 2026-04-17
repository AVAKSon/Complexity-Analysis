from pathlib import Path
import csv
import math
from statistics import mean, median, stdev
from scipy import stats


# =========================
# CONFIG
# =========================

ROOT = Path(r"C:/Users/AVAKSon/Desktop/about time/final version")
INPUT_DIR = ROOT / "analysis_results"
OUTPUT_DIR = ROOT / "statistical_analysis"
OUTPUT_DIR.mkdir(exist_ok=True)

INPUT_FILES = {
    "C": INPUT_DIR / "C_metrics.csv",
    "C++": INPUT_DIR / "Cpp_metrics.csv",
    "Java": INPUT_DIR / "Java_metrics.csv",
    "Python": INPUT_DIR / "Python_metrics.csv",
}

METRICS = [
    "loc",
    "cyclomatic_complexity",
    "token_count",
]


# =========================
# HELPERS
# =========================

def safe_stdev(values):
    return stdev(values) if len(values) > 1 else 0.0


def summarize(values):
    return {
        "mean": mean(values) if values else 0.0,
        "median": median(values) if values else 0.0,
        "std_dev": safe_stdev(values),
        "min": min(values) if values else 0.0,
        "max": max(values) if values else 0.0,
    }


def normalize(values):
    mu = mean(values)
    sigma = safe_stdev(values)

    if sigma == 0:
        return values

    return [(x - mu) / sigma for x in values]


def normality_tests(values):
    if len(values) < 3:
        return {
            "shapiro_stat": None,
            "shapiro_p": None,
            "ks_stat": None,
            "ks_p": None,
        }

    shapiro_stat, shapiro_p = stats.shapiro(values)

    norm_values = normalize(values)
    ks_stat, ks_p = stats.kstest(norm_values, "norm")

    return {
        "shapiro_stat": shapiro_stat,
        "shapiro_p": shapiro_p,
        "ks_stat": ks_stat,
        "ks_p": ks_p,
    }


def kruskal_test(grouped_values):
    """
    grouped_values: dict like
    {
        "C": [...],
        "C++": [...],
        "Java": [...],
        "Python": [...]
    }
    """
    groups = [values for values in grouped_values.values() if values]

    if len(groups) < 2:
        return {
            "kruskal_stat": None,
            "kruskal_p": None,
        }

    stat, p = stats.kruskal(*groups)

    return {
        "kruskal_stat": stat,
        "kruskal_p": p,
    }


def interpret_p_value(p):
    if p is None:
        return "Not enough data"
    if p < 0.05:
        return "Statistically significant"
    return "Not statistically significant"


def read_csv_rows(file_path):
    rows = []

    with file_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    return rows


def load_all_data():
    data = {}

    for language, file_path in INPUT_FILES.items():
        if not file_path.exists():
            print(f"[WARNING] File not found: {file_path}")
            continue

        rows = read_csv_rows(file_path)
        data[language] = rows

    return data


def extract_metric_values(rows, metric_name):
    values = []

    for row in rows:
        value = row.get(metric_name, "").strip()
        if value == "":
            continue

        try:
            values.append(float(value))
        except ValueError:
            continue

    return values


# =========================
# ANALYSIS
# =========================

def analyze_descriptive_and_normality(data):
    output_rows = []

    for language, rows in data.items():
        for metric in METRICS:
            values = extract_metric_values(rows, metric)

            summary = summarize(values)
            tests = normality_tests(values)

            output_rows.append({
                "language": language,
                "metric": metric,
                "mean": round(summary["mean"], 6),
                "median": round(summary["median"], 6),
                "std_dev": round(summary["std_dev"], 6),
                "min": round(summary["min"], 6),
                "max": round(summary["max"], 6),
                "shapiro_stat": None if tests["shapiro_stat"] is None else round(tests["shapiro_stat"], 6),
                "shapiro_p": None if tests["shapiro_p"] is None else round(tests["shapiro_p"], 6),
                "ks_stat": None if tests["ks_stat"] is None else round(tests["ks_stat"], 6),
                "ks_p": None if tests["ks_p"] is None else round(tests["ks_p"], 6),
                "normality_interpretation": (
                    "Non-normal"
                    if tests["shapiro_p"] is not None and tests["shapiro_p"] < 0.05
                    else "Possibly normal"
                ),
            })

    return output_rows


def analyze_kruskal(data):
    """
    Returns row-based results:
    metric, kruskal_stat, kruskal_p, interpretation
    """
    output_rows = []

    for metric in METRICS:
        grouped_values = {}

        for language, rows in data.items():
            grouped_values[language] = extract_metric_values(rows, metric)

        result = kruskal_test(grouped_values)

        output_rows.append({
            "metric": metric,
            "kruskal_stat": None if result["kruskal_stat"] is None else round(result["kruskal_stat"], 6),
            "kruskal_p": None if result["kruskal_p"] is None else round(result["kruskal_p"], 6),
            "interpretation": interpret_p_value(result["kruskal_p"]),
        })

    return output_rows


# =========================
# OUTPUT
# =========================

def save_csv(file_path, rows):
    if not rows:
        print(f"[WARNING] No data to save for {file_path.name}")
        return

    fieldnames = list(rows[0].keys())

    with file_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_descriptive_results(rows):
    print("\n" + "=" * 80)
    print("DESCRIPTIVE STATISTICS AND NORMALITY TESTS")
    print("=" * 80)

    current_language = None

    for row in rows:
        if row["language"] != current_language:
            current_language = row["language"]
            print(f"\n{current_language}")
            print("-" * 80)

        print(
            f"{row['metric']}: "
            f"mean={row['mean']}, median={row['median']}, std={row['std_dev']}, "
            f"min={row['min']}, max={row['max']}, "
            f"Shapiro p={row['shapiro_p']}, KS p={row['ks_p']}, "
            f"{row['normality_interpretation']}"
        )


def print_kruskal_results(rows):
    print("\n" + "=" * 80)
    print("KRUSKAL–WALLIS TEST RESULTS")
    print("=" * 80)

    for row in rows:
        print(
            f"{row['metric']}: "
            f"H={row['kruskal_stat']}, p={row['kruskal_p']} -> {row['interpretation']}"
        )


# =========================
# MAIN
# =========================

def main():
    data = load_all_data()

    if not data:
        print("No input data loaded.")
        return

    descriptive_rows = analyze_descriptive_and_normality(data)
    kruskal_rows = analyze_kruskal(data)

    descriptive_file = OUTPUT_DIR / "descriptive_and_normality.csv"
    kruskal_file = OUTPUT_DIR / "kruskal_results.csv"

    save_csv(descriptive_file, descriptive_rows)
    save_csv(kruskal_file, kruskal_rows)

    print_descriptive_results(descriptive_rows)
    print_kruskal_results(kruskal_rows)

    print("\nSaved files:")
    print(f"- {descriptive_file}")
    print(f"- {kruskal_file}")


if __name__ == "__main__":
    main()