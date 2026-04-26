import sys
import hashlib
import argparse
import json
import os
from pathlib import Path
from datetime import datetime, timezone


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def generate(target: Path, output: Path) -> int:
    if not target.exists():
        print(f"[ERROR] Target not found: {target}", file=sys.stderr)
        return 1

    files = sorted(target.rglob("*")) if target.is_dir() else [target]
    files = [f for f in files if f.is_file()]

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target": str(target.resolve()),
        "files": {},
    }

    for f in files:
        rel = str(f.relative_to(target) if target.is_dir() else f.name)
        manifest["files"][rel] = hash_file(f)
        print(f"  hashed: {rel}")

    output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\n[OK] Manifest written to {output} ({len(files)} files)")
    return 0


def verify(manifest_path: Path) -> int:
    if not manifest_path.exists():
        print(f"[ERROR] Manifest not found: {manifest_path}", file=sys.stderr)
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    base = Path(manifest["target"])

    ok = changed = missing = 0

    for rel, expected in manifest["files"].items():
        full = base / rel
        if not full.exists():
            print(f"  [MISSING]  {rel}")
            missing += 1
            continue

        actual = hash_file(full)
        if actual == expected:
            ok += 1
        else:
            print(f"  [CHANGED]  {rel}")
            changed += 1

    print(f"\n--- verify results ---")
    print(f"  OK:      {ok}")
    print(f"  changed: {changed}")
    print(f"  missing: {missing}")

    return 0 if (changed == 0 and missing == 0) else 1


def main():
    parser = argparse.ArgumentParser(
        description="Generate or verify SHA256 file integrity manifests."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    gen = sub.add_parser("generate", help="Hash files and save manifest")
    gen.add_argument("target", type=Path, help="File or directory to hash")
    gen.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("integrity.json"),
        help="Output manifest file (default: integrity.json)",
    )

    ver = sub.add_parser("verify", help="Check files against existing manifest")
    ver.add_argument("manifest", type=Path, help="Manifest file to verify against")

    args = parser.parse_args()

    if args.cmd == "generate":
        return generate(args.target, args.output)
    elif args.cmd == "verify":
        return verify(args.manifest)


if __name__ == "__main__":
    sys.exit(main())
