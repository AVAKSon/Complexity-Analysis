from pathlib import Path
import csv
import math
import re

# =========================
# CONFIG
# =========================

ROOT = Path(r"C:/Users/AVAKSon/Desktop/about time/final version")
OUTPUT_DIR = ROOT / "halstead_results"
OUTPUT_DIR.mkdir(exist_ok=True)

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

PYTHON_MULTIWORD_OPERATORS = {
    "is not",
    "not in"
}

CONTROL_KEYWORDS_BY_LANG = {
    "C": {"if", "else", "for", "while", "switch", "case", "return", "break", "continue", "do", "goto"},
    "C++": {"if", "else", "for", "while", "switch", "case", "return", "break", "continue", "do", "goto", "catch", "throw", "try"},
    "Java": {"if", "else", "for", "while", "switch", "case", "return", "break", "continue", "do", "catch", "throw", "try", "finally"},
    "Python": {"if", "elif", "else", "for", "while", "return", "break", "continue", "try", "except", "finally", "with", "lambda", "yield", "pass"}
}

IDENTIFIER_RE = re.compile(r'^[A-Za-z_]\w*$')
NUMBER_RE = re.compile(r'^\d+(\.\d+)?([eE][+-]?\d+)?$')

# =========================
# HELPERS
# =========================

def get_algorithm_name(file_path: Path) -> str:
    return file_path.stem

# =========================
# COMMENT / STRING REMOVAL
# =========================

def strip_c_like_comments_and_strings(code: str) -> str:
    pattern = r'''
        //.*?$                           |
        /\*.*?\*/                       |
        "(?:\\.|[^"\\])*"               |
        '(?:\\.|[^'\\])*'
    '''
    return re.sub(pattern, ' ', code, flags=re.MULTILINE | re.DOTALL | re.VERBOSE)


def strip_python_comments_and_strings(code: str) -> str:
    pattern = r'''
        \#.*?$                              |
        """(?:.|\n)*?"""                    |
        ''' + "'''(?:.|\\n)*?'''" + r'''    |
        "(?:\\.|[^"\\])*"                   |
        '(?:\\.|[^'\\])*'
    '''
    return re.sub(pattern, ' ', code, flags=re.MULTILINE | re.DOTALL | re.VERBOSE)

# =========================
# TOKENIZATION
# =========================

def build_operator_list(lang: str):
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


def preprocess_code(lang: str, code: str) -> str:
    if lang == "Python":
        code = strip_python_comments_and_strings(code)
        code = re.sub(r'\bis\s+not\b', ' is_not ', code)
        code = re.sub(r'\bnot\s+in\b', ' not_in ', code)
    else:
        code = strip_c_like_comments_and_strings(code)

    return code


def tokenize(lang: str, code: str):
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

def classify_token(lang: str, token: str):
    operators = set(build_operator_list(lang))

    if token in operators:
        return "operator"

    if NUMBER_RE.match(token):
        return "operand"

    if IDENTIFIER_RE.match(token):
        return "operand"

    return None


def halstead_metrics_for_code(lang: str, code: str):
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

def analyze_language(lang: str, folder: Path):
    exts = EXTENSIONS[lang]

    files = [
        p for p in folder.rglob("*")
        if p.is_file() and p.suffix.lower() in exts
    ]

    rows = []

    for file_path in files:
        try:
            code = file_path.read_text(encoding="utf-8", errors="ignore")
            metrics = halstead_metrics_for_code(lang, code)

            row = {
                "language": lang,
                "file_name": file_path.name,
                "algorithm_name": get_algorithm_name(file_path),
                "relative_path": str(file_path.relative_to(ROOT)),
                **metrics
            }

            rows.append(row)

        except Exception as e:
            print(f"[ERROR] Could not process {file_path}: {e}")

    rows.sort(key=lambda x: x["algorithm_name"].lower())
    return rows

# =========================
# CSV OUTPUT
# =========================

def save_csv(file_path: Path, rows: list[dict]):
    if not rows:
        print(f"[WARNING] No data to save for {file_path.name}")
        return

    fieldnames = [
        "language",
        "file_name",
        "algorithm_name",
        "relative_path",
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

    with file_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# =========================
# MAIN
# =========================

def main():
    all_rows = []

    for lang, folder in LANG_DIRS.items():
        if not folder.exists():
            print(f"[WARNING] Folder not found: {folder}")
            continue

        print("\n" + "=" * 60)
        print(f"Analyzing {lang}")
        print("=" * 60)

        rows = analyze_language(lang, folder)
        all_rows.extend(rows)

        safe_lang_name = lang.replace("+", "p")
        output_file = OUTPUT_DIR / f"{safe_lang_name}_halstead_metrics.csv"
        save_csv(output_file, rows)

        print(f"Saved {len(rows)} rows to {output_file}")

    if all_rows:
        combined_file = OUTPUT_DIR / "all_halstead_metrics.csv"
        save_csv(combined_file, all_rows)
        print(f"\nSaved combined dataset to {combined_file}")


if __name__ == "__main__":
    main()