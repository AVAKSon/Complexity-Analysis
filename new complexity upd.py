from pathlib import Path
from statistics import mean, median, stdev
from scipy import stats
import math
import re
import csv

# =========================
# CONFIG
# =========================

ROOT = Path(r"C:/Users/AVAKSon/Desktop/about time/final version")

LANG_DIRS = {
    "C": ROOT / "C",
    "C++": ROOT / "C++",
    "Java": ROOT / "Java",
    "Python": ROOT / "Python",
}

EXTENSIONS = {
    "C": {".c", ".h"},
    "C++": {".cpp", ".cc", ".cxx", ".hpp", ".hh", ".hxx"},
    "Java": {".java"},
    "Python": {".py"},
}

# =========================
# OPERATORS
# =========================

C_LIKE_BASE_OPERATORS = {
    "=", ">", "<", "!", "~", "?",
    "->", "==", ">=", "<=", "!=", "&&", "||",
    "++", "--", "+", "-", "*", "/", "&", "|", "^", "%",
    "<<", ">>",
    "+=", "-=", "*=", "/=", "&=", "|=", "^=", "%=", "<<=", ">>=",
    "(", ")", "[", "]", "{", "}", ".", ",", ":", ";"
}

JAVA_EXTRA_OPERATORS = {
    ">>>", ">>>=", "instanceof"
}

CPP_EXTRA_OPERATORS = {
    "::", ".*", "->*", "new", "delete", "sizeof"
}

C_EXTRA_OPERATORS = {
    "sizeof"
}

PYTHON_OPERATORS = {
    "+", "-", "*", "/", "//", "%", "**",
    "=", "==", "!=", "<", ">", "<=", ">=",
    "+=", "-=", "*=", "/=", "//=", "%=", "**=",
    "&", "|", "^", "~", "<<", ">>", "&=", "|=", "^=", "<<=", ">>=",
    ":=", "and", "or", "not", "is", "in",
    "(", ")", "[", "]", "{", "}", ".", ",", ":", ";"
}

# multi-word Python operators
PYTHON_MULTIWORD_OPERATORS = {
    "is not",
    "not in"
}

# keywords that should be treated as operators in Halstead-like counting
CONTROL_KEYWORDS_BY_LANG = {
    "C": {"if", "else", "for", "while", "switch", "case", "return", "break", "continue", "do", "goto"},
    "C++": {"if", "else", "for", "while", "switch", "case", "return", "break", "continue", "do", "goto", "catch", "throw", "try"},
    "Java": {"if", "else", "for", "while", "switch", "case", "return", "break", "continue", "do", "catch", "throw", "try", "finally"},
    "Python": {"if", "elif", "else", "for", "while", "return", "break", "continue", "try", "except", "finally", "with", "lambda", "yield", "pass"}
}

# constants / literals patterns
IDENTIFIER_RE = re.compile(r'^[A-Za-z_]\w*$')
NUMBER_RE = re.compile(r'^\d+(\.\d+)?([eE][+-]?\d+)?$')

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
        return None

    shapiro_stat, shapiro_p = stats.shapiro(values)

    norm_values = normalize(values)
    ks_stat, ks_p = stats.kstest(norm_values, "norm")

    return {
        "shapiro_stat": shapiro_stat,
        "shapiro_p": shapiro_p,
        "ks_stat": ks_stat,
        "ks_p": ks_p,
    }

# =========================
# COMMENT / STRING REMOVAL
# =========================

def strip_c_like_comments_and_strings(code):
    pattern = r'''
        //.*?$                           |   # single-line comments
        /\*.*?\*/                       |   # multi-line comments
        "(?:\\.|[^"\\])*"               |   # double-quoted strings
        '(?:\\.|[^'\\])*'                   # char literals / single strings
    '''
    return re.sub(pattern, ' ', code, flags=re.MULTILINE | re.DOTALL | re.VERBOSE)

def strip_python_comments_and_strings(code):
    pattern = r'''
        \#.*?$                              |   # comments
        """(?:.|\n)*?"""                    |   # triple double quoted
        ''' + "'''(?:.|\\n)*?'''" + r'''    |   # triple single quoted
        "(?:\\.|[^"\\])*"                   |   # double quoted strings
        '(?:\\.|[^'\\])*'                       # single quoted strings
    '''
    return re.sub(pattern, ' ', code, flags=re.MULTILINE | re.DOTALL | re.VERBOSE)

# =========================
# TOKENIZATION
# =========================

def build_operator_list(lang):
    if lang == "C":
        ops = set(C_LIKE_BASE_OPERATORS) | set(C_EXTRA_OPERATORS) | set(CONTROL_KEYWORDS_BY_LANG[lang])
    elif lang == "C++":
        ops = set(C_LIKE_BASE_OPERATORS) | set(CPP_EXTRA_OPERATORS) | set(CONTROL_KEYWORDS_BY_LANG[lang])
    elif lang == "Java":
        ops = set(C_LIKE_BASE_OPERATORS) | set(JAVA_EXTRA_OPERATORS) | set(CONTROL_KEYWORDS_BY_LANG[lang])
    elif lang == "Python":
        ops = set(PYTHON_OPERATORS) | set(PYTHON_MULTIWORD_OPERATORS) | set(CONTROL_KEYWORDS_BY_LANG[lang])
    else:
        ops = set()
    return sorted(ops, key=len, reverse=True)

def preprocess_code(lang, code):
    if lang == "Python":
        code = strip_python_comments_and_strings(code)
        # normalize multi-word operators so they are caught as single tokens
        code = re.sub(r'\bis\s+not\b', ' is_not ', code)
        code = re.sub(r'\bnot\s+in\b', ' not_in ', code)
    else:
        code = strip_c_like_comments_and_strings(code)
    return code

def tokenize(lang, code):
    code = preprocess_code(lang, code)

    operators = build_operator_list(lang)

    if lang == "Python":
        operator_aliases = {
            "is not": "is_not",
            "not in": "not_in"
        }
    else:
        operator_aliases = {}

    escaped_ops = []
    for op in operators:
        alias = operator_aliases.get(op, op)
        escaped_ops.append(re.escape(alias))

    operator_pattern = "|".join(escaped_ops)

    token_pattern = rf"""
        {operator_pattern}
        |
        [A-Za-z_]\w*
        |
        \d+(?:\.\d+)?(?:[eE][+-]?\d+)?
    """

    raw_tokens = re.findall(token_pattern, code, flags=re.VERBOSE)

    # convert aliases back
    final_tokens = []
    for token in raw_tokens:
        if token == "is_not":
            final_tokens.append("is not")
        elif token == "not_in":
            final_tokens.append("not in")
        else:
            final_tokens.append(token)

    return final_tokens

# =========================
# HALSTEAD
# =========================

def classify_token(lang, token):
    operators = set(build_operator_list(lang))

    if token in operators:
        return "operator"

    if NUMBER_RE.match(token):
        return "operand"

    if IDENTIFIER_RE.match(token):
        return "operand"

    return None

def halstead_metrics_for_code(lang, code):
    tokens = tokenize(lang, code)

    operators = []
    operands = []

    for token in tokens:
        kind = classify_token(lang, token)

        if kind == "operator":
            operators.append(token)
        elif kind == "operand":
            operands.append(token)

    n1 = len(set(operators))
    n2 = len(set(operands))
    N1 = len(operators)
    N2 = len(operands)

    vocabulary = n1 + n2
    length = N1 + N2

    if vocabulary > 0:
        volume = length * math.log2(vocabulary)
    else:
        volume = 0.0

    if n2 > 0:
        difficulty = (n1 / 2) * (N2 / n2)
    else:
        difficulty = 0.0

    effort = difficulty * volume

    return {
        "n1_distinct_operators": n1,
        "n2_distinct_operands": n2,
        "N1_total_operators": N1,
        "N2_total_operands": N2,
        "vocabulary": vocabulary,
        "length": length,
        "volume": volume,
        "difficulty": difficulty,
        "effort": effort,
    }

# =========================
# ANALYSIS
# =========================

def analyze_language(lang, folder):
    exts = EXTENSIONS[lang]
    files = [
        p for p in folder.rglob("*")
        if p.is_file() and p.suffix.lower() in exts
    ]

    metrics_per_file = []

    for file_path in files:
        try:
            code = file_path.read_text(encoding="utf-8", errors="ignore")
            metrics = halstead_metrics_for_code(lang, code)
            metrics["file"] = str(file_path)
            metrics_per_file.append(metrics)
        except Exception as e:
            print(f"[ERROR] Could not process {file_path}: {e}")

    metric_names = [
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

    result = {
        "file_count": len(metrics_per_file),
        "metrics": {}
    }

    for metric_name in metric_names:
        values = [m[metric_name] for m in metrics_per_file]
        result["metrics"][metric_name] = {
            "values": values,
            "summary": summarize(values),
            "tests": normality_tests(values)
        }

    return result

# =========================
# PRINTING
# =========================

def print_metric_results(lang, metric_name, data):
    s = data["summary"]
    t = data["tests"]

    print(f"\n{lang} — {metric_name}")
    print("-" * 60)
    print("Descriptive statistics:")
    print(f"Mean:      {s['mean']:.2f}")
    print(f"Median:    {s['median']:.2f}")
    print(f"Std. Dev.: {s['std_dev']:.2f}")
    print(f"Minimum:   {s['min']:.2f}")
    print(f"Maximum:   {s['max']:.2f}")

    if t:
        print("\nNormality tests:")
        print(f"Shapiro-Wilk:       stat={t['shapiro_stat']:.3f}, p={t['shapiro_p']:.5f}")
        print(f"Kolmogorov-Smirnov: stat={t['ks_stat']:.3f}, p={t['ks_p']:.5f}")

def save_results_to_csv(all_results, output_file):
    header = [
        "Language",
        "Metric",
        "Mean",
        "Median",
        "StdDev",
        "Min",
        "Max",
        "Shapiro_p",
        "KS_p",
        "Distribution"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for lang, result in all_results.items():
            for metric_name, data in result["metrics"].items():

                s = data["summary"]
                t = data["tests"]

                if t:
                    shapiro_p = t["shapiro_p"]
                    ks_p = t["ks_p"]

                    if shapiro_p < 0.05 or ks_p < 0.05:
                        distribution = "Non-normal"
                    else:
                        distribution = "Normal"
                else:
                    shapiro_p = ""
                    ks_p = ""
                    distribution = ""

                writer.writerow([
                    lang,
                    metric_name,
                    round(s["mean"], 5),
                    round(s["median"], 5),
                    round(s["std_dev"], 5),
                    round(s["min"], 5),
                    round(s["max"], 5),
                    shapiro_p,
                    ks_p,
                    distribution
                ])

def main():

    all_results = {}

    for lang, folder in LANG_DIRS.items():

        if not folder.exists():
            print(f"[WARNING] Folder not found: {folder}")
            continue

        print("\n" + "=" * 60)
        print(f"{lang}")
        print("=" * 60)

        result = analyze_language(lang, folder)

        all_results[lang] = result

        print(f"Files analyzed: {result['file_count']}")

        for metric_name, data in result["metrics"].items():
            print_metric_results(
                lang,
                metric_name,
                data
            )

    output_file = ROOT / "halstead_statistics.csv"

    save_results_to_csv(
        all_results,
        output_file
    )

    print("\nResults saved to:")
    print(output_file)

if __name__ == "__main__":
    main()