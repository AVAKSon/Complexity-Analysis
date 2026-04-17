from pathlib import Path
import csv
import lizard



ROOT = Path(r"C:/Users/AVAKSon/Desktop/about time/final version")


OUTPUT_DIR = ROOT / "analysis_results"
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


def get_algorithm_name(file_path: Path) -> str:
    return file_path.stem


def analyze_language(lang_name: str, folder: Path):

    exts = EXTENSIONS[lang_name]

    files = [
        p for p in folder.rglob("*")
        if p.is_file() and p.suffix.lower() in exts
    ]

    if not files:
        return []

    file_infos = list(lizard.analyze([str(p) for p in files]))

    rows = []

    for info in file_infos:
        file_path = Path(info.filename)

        row = {
            "language": lang_name,
            "file_name": file_path.name,
            "algorithm_name": get_algorithm_name(file_path),
            "relative_path": str(file_path.relative_to(ROOT)),
            "loc": info.nloc,
            "cyclomatic_complexity": info.CCN,
            "token_count": info.token_count,
        }

        rows.append(row)

    rows.sort(key=lambda x: x["algorithm_name"].lower())
    return rows


def save_csv(file_path: Path, rows: list[dict]):

    if not rows:
        print(f"[WARNING] No data to save for {file_path.name}")
        return

    fieldnames = [
        "language",
        "file_name",
        "algorithm_name",
        "relative_path",
        "loc",
        "cyclomatic_complexity",
        "token_count",
    ]

    with file_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    all_rows = []

    for lang, folder in LANG_DIRS.items():
        if not folder.exists():
            print(f"[WARNING] Folder not found: {folder}")
            continue

        print(f"Analyzing {lang}...")

        rows = analyze_language(lang, folder)
        all_rows.extend(rows)

        safe_lang_name = lang.replace("+", "p")
        output_file = OUTPUT_DIR / f"{safe_lang_name}_metrics.csv"
        save_csv(output_file, rows)

        print(f"Saved {len(rows)} rows to {output_file}")

    if all_rows:
        combined_file = OUTPUT_DIR / "all_languages_metrics.csv"
        save_csv(combined_file, all_rows)
        print(f"Saved combined dataset to {combined_file}")


if __name__ == "__main__":
    main()