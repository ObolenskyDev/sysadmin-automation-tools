# Sysadmin Automation Tools

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat&logo=python)

Python scripts for routine sysadmin tasks. No external dependencies — standard library only.

## Scripts

**`log_parser.py`** — scan log files for error keywords with context lines and a per-keyword match summary. Supports multiple keywords, case-insensitive search, and configurable context lines (`-C`).

**`disk_check.py`** — check disk usage on one or more mount points and alert when usage exceeds a threshold. Useful as a pre-flight check before backups or deployments.

**`data_integrity.py`** — generate and verify SHA256 file integrity manifests. `generate` hashes all files in a directory and saves a JSON manifest; `verify` re-hashes and reports any changed or missing files.

## Usage

```bash
# Scan a log for errors (default: ERROR, CRITICAL, FATAL)
python3 scripts/log_parser.py /var/log/syslog

# Custom keywords with 3 lines of context
python3 scripts/log_parser.py /var/log/app.log -k WARN TIMEOUT -C 3

# Check disk usage (alert at 85%)
python3 scripts/disk_check.py / /var/log --threshold 85

# Generate integrity manifest for a directory
python3 scripts/data_integrity.py generate /etc/nginx -o nginx_manifest.json

# Verify files against saved manifest
python3 scripts/data_integrity.py verify nginx_manifest.json
```

No external libraries required — Python 3.8+.
