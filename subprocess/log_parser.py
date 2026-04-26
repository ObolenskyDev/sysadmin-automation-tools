import sys
import re
import argparse
from collections import defaultdict


def scan_log(filepath, keywords, context=2, case_sensitive=False):
    flags = 0 if case_sensitive else re.IGNORECASE
    patterns = [re.compile(re.escape(kw), flags) for kw in keywords]

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}", file=sys.stderr)
        return 1

    match_lines = set()
    for i, line in enumerate(lines):
        if any(p.search(line) for p in patterns):
            match_lines.add(i)

    if not match_lines:
        print(f"[OK] No matches for {keywords} in {filepath}")
        return 0

    counts = defaultdict(int)
    printed = set()

    for idx in sorted(match_lines):
        start = max(0, idx - context)
        end = min(len(lines) - 1, idx + context)
        block = range(start, end + 1)

        if any(b in printed for b in block):
            continue

        print(f"\n--- match at line {idx + 1} ---")
        for i in block:
            prefix = ">> " if i in match_lines else "   "
            print(f"{prefix}{i + 1:>6}: {lines[i].rstrip()}")
            printed.add(i)

        for p, kw in zip(patterns, keywords):
            if p.search(lines[idx]):
                counts[kw] += 1

    print(f"\n--- summary: {filepath} ---")
    for kw in keywords:
        print(f"  {kw}: {counts[kw]} match(es)")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Scan log files for error keywords with context lines."
    )
    parser.add_argument("file", help="Path to log file")
    parser.add_argument(
        "-k", "--keywords",
        nargs="+",
        default=["ERROR", "CRITICAL", "FATAL"],
        metavar="KW",
        help="Keywords to search for (default: ERROR CRITICAL FATAL)",
    )
    parser.add_argument(
        "-C", "--context",
        type=int,
        default=2,
        metavar="N",
        help="Lines of context around each match (default: 2)",
    )
    parser.add_argument(
        "-s", "--case-sensitive",
        action="store_true",
        help="Case-sensitive search (default: case-insensitive)",
    )
    args = parser.parse_args()

    return scan_log(
        args.file,
        keywords=args.keywords,
        context=args.context,
        case_sensitive=args.case_sensitive,
    )


if __name__ == "__main__":
    sys.exit(main())
