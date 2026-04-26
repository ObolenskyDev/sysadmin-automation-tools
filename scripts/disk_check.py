import subprocess
import sys
import argparse


def check_disk_usage(paths: list[str], threshold: int) -> int:
    cmd = ["df", "-h"] + paths
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[ERROR] df failed: {result.stderr.strip()}", file=sys.stderr)
        return 1

    lines = result.stdout.strip().split("\n")
    alarms = 0

    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 6:
            continue
        mount = parts[-1]
        usage_str = parts[-2].replace("%", "")
        try:
            usage = int(usage_str)
        except ValueError:
            continue

        if usage >= threshold:
            print(f"🔴 ALARM  {mount:<20} {usage}% (threshold: {threshold}%)")
            alarms += 1
        else:
            print(f"🟢 OK     {mount:<20} {usage}%")

    return 1 if alarms else 0


def main():
    parser = argparse.ArgumentParser(
        description="Check disk usage and alert if threshold is exceeded."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["/",''],
        metavar="PATH",
        help="Mount points to check (default: /)",
    )
    parser.add_argument(
        "-t", "--threshold",
        type=int,
        default=85,
        metavar="PCT",
        help="Alert threshold in percent (default: 85)",
    )
    args = parser.parse_args()
    paths = [p for p in args.paths if p]
    return check_disk_usage(paths or ["/"], args.threshold)


if __name__ == "__main__":
    sys.exit(main())
